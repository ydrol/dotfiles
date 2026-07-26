#!/usr/bin/env bash
# Symlinks everything under files/ into the matching path under $HOME,
# backing up anything already there. Safe to re-run.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
files_dir="$script_dir/files"
target_home="${HOME}"
stamp="$(date +%y%m%d)"

if [[ ! -d "$files_dir" ]]; then
    echo "error: $files_dir not found" >&2
    exit 1
fi

backup_path() {
    local target="$1"
    local candidate="${target}.${stamp}.old"
    local n=1
    while [[ -e "$candidate" || -L "$candidate" ]]; do
        candidate="${target}.${stamp}.old.${n}"
        n=$((n + 1))
    done
    printf '%s' "$candidate"
}

installed=0
skipped=0
backed_up=0
declare -a backups=()

while IFS= read -r -d '' src; do
    rel="${src#"$files_dir"/}"
    target="$target_home/$rel"

    dir="$(dirname "$target")"
    # mkdir -p fails with "File exists" when a path component is a dangling
    # symlink (points to a missing/non-dir target). Back it up out of the way.
    if [[ -L "$dir" && ! -d "$dir" ]]; then
        backup="$(backup_path "$dir")"
        mv "$dir" "$backup"
        echo "backed up ~/${dir#"$target_home"/} -> $backup"
        backed_up=$((backed_up + 1))
        backups+=("$backup|$dir")
    fi
    mkdir -p "$dir"

    if [[ -L "$target" ]] && [[ "$(realpath -m "$target")" == "$(realpath -m "$src")" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    if [[ -e "$target" || -L "$target" ]]; then
        backup="$(backup_path "$target")"
        mv "$target" "$backup"
        echo "backed up ~/$rel -> $backup"
        backed_up=$((backed_up + 1))
        backups+=("$backup|$target")
    fi

    ln -s "$src" "$target"
    echo "linked   ~/$rel -> $src"
    installed=$((installed + 1))
done < <(find "$files_dir" \( -type f -o -type l \) -print0)

echo
echo "done: $installed linked, $backed_up backed up, $skipped already up to date"

diverged=()
for pair in "${backups[@]+"${backups[@]}"}"; do
    backup="${pair%%|*}"
    target="${pair#*|}"
    [[ -f "$backup" && -f "$target" ]] || continue
    diff -q "$backup" "$target" >/dev/null 2>&1 || diverged+=("$backup" "$target")
done

if [[ ${#diverged[@]} -gt 0 ]]; then
    echo
    echo "backed-up files whose content differs from what was just installed:"
    for ((i = 0; i < ${#diverged[@]}; i += 2)); do
        echo "  diff \"${diverged[i]}\" \"${diverged[i + 1]}\""
    done
fi
