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

while IFS= read -r -d '' src; do
    rel="${src#"$files_dir"/}"
    target="$target_home/$rel"

    mkdir -p "$(dirname "$target")"

    if [[ -L "$target" && "$(readlink "$target")" == "$src" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    if [[ -e "$target" || -L "$target" ]]; then
        backup="$(backup_path "$target")"
        mv "$target" "$backup"
        echo "backed up ~/$rel -> $backup"
        backed_up=$((backed_up + 1))
    fi

    ln -s "$src" "$target"
    echo "linked   ~/$rel -> $src"
    installed=$((installed + 1))
done < <(find "$files_dir" \( -type f -o -type l \) -print0)

echo
echo "done: $installed linked, $backed_up backed up, $skipped already up to date"
