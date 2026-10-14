#!/usr/bin/env python3
"""PreToolUse hook: deny Bash calls that would send subtitle or video files to GitHub.

Covers git add, git commit and git push in any repository with a github.com remote,
and gh commands that upload files directly. The user bypasses it by running the
command outside Claude.
"""

import json
import os
import re
import shlex
import subprocess
import sys

BLOCKED_EXTENSIONS = {".srt", ".mp4", ".mkv"}
GUARDED_REMOTE = re.compile(r"github\.com", re.I)
GH_UPLOADS = {("release", "create"), ("release", "upload"), ("gist", "create"), ("gist", "edit")}
WRAPPERS = {"sudo", "env", "time", "nohup", "command", "nice", "stdbuf"}
SHELLS = {"bash", "sh", "zsh", "dash"}
OPERATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")"}


def tokenize(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return command.split()


def segments(tokens):
    current = []
    for tok in tokens:
        if tok in OPERATORS:
            if current:
                yield current
            current = []
        else:
            current.append(tok)
    if current:
        yield current


def strip_prefix(seg):
    while seg and (re.match(r"^\w+=", seg[0]) or os.path.basename(seg[0]) in WRAPPERS):
        seg = seg[1:]
    return seg


def blocked(paths):
    return sorted({p for p in paths if os.path.splitext(p.strip().strip("'\""))[1].lower() in BLOCKED_EXTENSIONS})


def git(cwd, *args):
    try:
        result = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def has_github_remote(cwd):
    return bool(GUARDED_REMOTE.search(git(cwd, "remote", "-v") or ""))


def split_git_globals(seg, cwd):
    args = seg[1:]
    while args and args[0].startswith("-"):
        opt = args.pop(0)
        if opt == "-C" and args:
            cwd = os.path.join(cwd, os.path.expanduser(args.pop(0)))
        elif opt in ("-c", "--git-dir", "--work-tree", "--namespace") and args:
            args.pop(0)
    return cwd, args


def add_files(cwd, args):
    dry_run = git(cwd, "add", "--dry-run", *args) or ""
    return [m.group(1) for m in re.finditer(r"^add '(.+)'$", dry_run, re.M)]


def commit_files(cwd, args):
    files = (git(cwd, "diff", "--cached", "--name-only", "--diff-filter=ACMR") or "").split("\n")
    if any(a == "--all" or re.match(r"^-[a-zA-Z]*a[a-zA-Z]*$", a) for a in args):
        files += (git(cwd, "diff", "--name-only", "--diff-filter=ACMR") or "").split("\n")
    if "--" in args:
        files += args[args.index("--") + 1:]
    return files


def push_files(cwd, args):
    positional = [a for a in args if not a.startswith("-")]
    if "--all" in args or "--mirror" in args:
        tips = ["--branches"]
    elif len(positional) > 1:
        tips = [refspec.lstrip("+").split(":")[0] or "HEAD" for refspec in positional[1:]]
    else:
        tips = ["HEAD"]
    log = git(cwd, "log", "--name-only", "--diff-filter=ACMR", "--format=", *tips, "--not", "--remotes")
    return (log or "").split("\n")


def gh_files(seg):
    words = [t for t in seg[1:] if not t.startswith("-")]
    if tuple(words[:2]) in GH_UPLOADS:
        return [t.split("#", 1)[0] for t in seg[3:]]
    return []


def check(command, cwd):
    reasons = []
    for seg in segments(tokenize(command)):
        seg = strip_prefix(seg)
        if not seg:
            continue
        tool = os.path.basename(seg[0])
        if tool == "cd" and len(seg) > 1:
            cwd = os.path.join(cwd, os.path.expanduser(seg[1]))
        elif tool in SHELLS and "-c" in seg:
            idx = seg.index("-c")
            if idx + 1 < len(seg):
                reasons.extend(check(seg[idx + 1], cwd))
        elif tool == "gh":
            reasons.extend(f"gh {seg[1]} uploads {f}" for f in blocked(gh_files(seg)))
        elif tool == "git":
            repo, args = split_git_globals(seg, cwd)
            if not args or not has_github_remote(repo):
                continue
            sub, rest = args[0], args[1:]
            handlers = {"add": add_files, "commit": commit_files, "push": push_files}
            if sub in handlers:
                reasons.extend(f"git {sub} includes {f}" for f in blocked(handlers[sub](repo, rest)))
    return reasons


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    if event.get("tool_name") != "Bash":
        return
    command = (event.get("tool_input") or {}).get("command") or ""
    reasons = check(command, event.get("cwd") or os.getcwd())
    if not reasons:
        return
    message = (
        f"Blocked: {'; '.join(reasons)}. Subtitle and video files ({', '.join(sorted(BLOCKED_EXTENSIONS))}) "
        "must not be sent to GitHub from this session. Unstage or ignore them and continue without them; "
        "if they genuinely need to go up, tell the user, who will commit and push them outside Claude. "
        "Do not rephrase, split or wrap the call to get past this check."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": message,
        }
    }))


if __name__ == "__main__":
    main()
