#!/usr/bin/env python3
"""PreToolUse hook: deny any tool call that would write to a client ServiceNow instance.

An instance is trusted only when its name matches devoteam* or dev<digits>.
A write whose target cannot be identified from the call is denied as well.
"""

import json
import os
import re
import shlex
import sys

TRUSTED_INSTANCE = re.compile(r"^(devoteam[a-z0-9-]*|dev\d+)$", re.I)
HOSTNAME = re.compile(r"(?<![\w$@{])([a-z0-9-]+)\.service-now\.com\b", re.I)
SN_SHAPED = re.compile(
    r"service-now\.com|/api/now/|/api/sn_|/api/x_|sys\.scripts\.do|xmlhttp\.do|sysparm_|glide", re.I
)
HTTP_WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
CURL_DATA_FLAGS = {
    "--data", "--data-raw", "--data-binary", "--data-urlencode", "--data-ascii",
    "--form", "--form-string", "--upload-file", "--json",
}
WGET_WRITE_FLAGS = ("--post-data", "--post-file", "--method", "--body-data", "--body-file")
INSTANCE_FLAGS = {"-i", "--instance", "--alias", "-p", "--profile", "-a", "--auth", "--host"}
SN_TOOLS = {"snowdrift", "snc", "now-sdk"}
SNC_LOCAL_GROUPS = {"configure", "extension", "help", "version"}
SNC_READ_VERBS = {"query", "get", "list", "describe", "show", "download", "export", "search", "help"}
INLINE_INTERPRETERS = {"python", "python3", "node", "ruby", "perl", "php", "deno", "bun"}
INLINE_WRITE_WORDS = re.compile(
    r"\b(post|put|patch|delete|insert|update|deleteRecord|deleteMultiple|updateMultiple|setValue)\b", re.I
)
WRAPPERS = {"sudo", "env", "time", "nohup", "command", "nice", "stdbuf"}
SHELLS = {"bash", "sh", "zsh", "dash"}
OPERATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")"}

MCP_SN_SERVER = re.compile(r"servicenow|service-now|snow|(^|_)now($|_)|glide|sn_", re.I)
MCP_WRITE_TOOL = re.compile(
    r"create|update|delete|insert|remove|execute|run|import|upload|patch|set|write|deploy|install|commit|apply|add|modify|put|post|script",
    re.I,
)


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


def flag_values(seg, flags):
    for idx, tok in enumerate(seg):
        name, eq, value = tok.partition("=")
        if name in flags:
            if eq:
                yield value
            elif idx + 1 < len(seg):
                yield seg[idx + 1]


def harvest_instances(command, tokens):
    found = set(HOSTNAME.findall(command))
    for seg in segments(tokens):
        seg = strip_prefix(seg)
        if seg and os.path.basename(seg[0]) in SN_TOOLS:
            found.update(flag_values(seg, INSTANCE_FLAGS))
    for tok in tokens:
        match = re.match(r"^\w*INSTANCE\w*=(.+)$", tok, re.I)
        if match:
            found.add(HOSTNAME.sub(r"\1", match.group(1)))
    return {inst for inst in found if inst and not inst.startswith("$")}


def curl_writes(seg):
    method = None
    for idx, tok in enumerate(seg):
        if tok in ("-X", "--request") and idx + 1 < len(seg):
            method = seg[idx + 1].upper()
        elif tok.startswith("--request="):
            method = tok.split("=", 1)[1].upper()
        elif re.match(r"^-[a-zA-Z]*X.+$", tok):
            method = tok.split("X", 1)[1].upper()
        elif tok in CURL_DATA_FLAGS or tok.startswith("-d") and tok != "-D":
            return "curl sends a request body"
        elif tok.startswith("--data") or tok.startswith("--form") or tok.startswith("--upload-file"):
            return "curl sends a request body"
        elif re.match(r"^-[a-zA-Z]+$", tok) and set(tok[1:]) & set("dFT"):
            return "curl sends a request body"
    if method in HTTP_WRITE_METHODS:
        return f"curl -X {method}"
    return None


def wget_writes(seg):
    for tok in seg:
        name = tok.split("=", 1)[0]
        if name in WGET_WRITE_FLAGS:
            if name == "--method":
                method = tok.split("=", 1)[1].upper() if "=" in tok else ""
                if method and method not in HTTP_WRITE_METHODS:
                    continue
            return f"wget {name}"
    return None


def httpie_writes(seg):
    for tok in seg[1:]:
        if tok.startswith("-"):
            continue
        return f"{seg[0]} {tok}" if tok.upper() in HTTP_WRITE_METHODS else None
    return None


def snc_writes(seg):
    args = [t for t in seg[1:] if not t.startswith("-")]
    values = set(flag_values(seg, {"-p", "--profile", "-o", "--output"}))
    args = [a for a in args if a not in values]
    if not args or args[0] in SNC_LOCAL_GROUPS:
        return None
    if any(a in SNC_READ_VERBS for a in args):
        return None
    return f"snc {' '.join(args[:2])} is not a known read-only command"


def now_sdk_writes(seg):
    args = [t for t in seg[1:] if not t.startswith("-")]
    if args and args[0] in ("install", "deploy") and not ({"-i", "--info"} & set(seg)):
        return f"now-sdk {args[0]}"
    return None


def inline_writes(seg, text):
    if not any(t in ("-c", "-e", "--eval") for t in seg):
        return None
    if SN_SHAPED.search(text) and INLINE_WRITE_WORDS.search(text):
        return f"inline {seg[0]} code performs a write"
    return None


def command_writes(command):
    tokens = tokenize(command)
    reasons = []
    for seg in segments(tokens):
        seg = strip_prefix(seg)
        if not seg:
            continue
        tool = os.path.basename(seg[0])
        text = " ".join(seg)
        reason = None
        if tool in SHELLS and "-c" in seg:
            idx = seg.index("-c")
            if idx + 1 < len(seg):
                reasons.extend(command_writes(seg[idx + 1]))
            continue
        if tool == "now-sdk":
            reason = now_sdk_writes(seg)
        elif tool == "snc":
            reason = snc_writes(seg)
        elif tool == "curl" and SN_SHAPED.search(text):
            reason = curl_writes(seg)
        elif tool == "wget" and SN_SHAPED.search(text):
            reason = wget_writes(seg)
        elif tool in ("http", "https", "xh", "xhs") and SN_SHAPED.search(text):
            reason = httpie_writes(seg)
        elif tool in INLINE_INTERPRETERS:
            reason = inline_writes(seg, text)
        if reason:
            reasons.append(reason)
    return reasons


def mcp_writes(tool_name, tool_input):
    server, _, tool = tool_name[len("mcp__"):].partition("__")
    if not (MCP_SN_SERVER.search(server) or MCP_SN_SERVER.search(tool)):
        return [], set()
    if not MCP_WRITE_TOOL.search(tool):
        return [], set()
    payload = json.dumps(tool_input)
    instances = set(HOSTNAME.findall(payload))
    for key, value in tool_input.items() if isinstance(tool_input, dict) else []:
        if re.search(r"instance|host|alias|profile", key, re.I) and isinstance(value, str):
            instances.add(HOSTNAME.sub(r"\1", value))
    return [f"MCP tool {tool_name} has write capability"], instances


def deny(reason):
    message = (
        f"Blocked: {reason}. Client ServiceNow instances are read-only from this session. "
        "Trusted instances are devoteam* and dev<digits> only, and the target must be visible in the call. "
        "Produce the change as a file (update set XML, import-set data, background script or request body) "
        "for the user to import or run manually. Do not rephrase, split or wrap the call to get past this check."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": message,
        }
    }))


def verdict(reasons, instances):
    if not reasons:
        return None
    untrusted = sorted(i for i in instances if not TRUSTED_INSTANCE.match(i))
    if untrusted:
        return f"{reasons[0]} against client instance {', '.join(untrusted)}"
    if not instances:
        return f"{reasons[0]} and the target instance cannot be identified from the call"
    return None


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    if tool_name == "Bash":
        command = tool_input.get("command") or ""
        reason = verdict(command_writes(command), harvest_instances(command, tokenize(command)))
    elif tool_name.startswith("mcp__"):
        reason = verdict(*mcp_writes(tool_name, tool_input))
    else:
        reason = None
    if reason:
        deny(reason)


if __name__ == "__main__":
    main()
