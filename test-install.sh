#!/usr/bin/env bash
# Exercises install.sh against a throwaway fake $HOME. Run after any change
# to install.sh: ./test-install.sh
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
install_sh="$script_dir/install.sh"
fake_home="$(mktemp -d)"
trap 'rm -rf "$fake_home"' EXIT

failures=0

run_install() {
    HOME="$fake_home" bash "$install_sh"
}

pass() { echo "  ok   - $1"; }
fail() { echo "  FAIL - $1"; failures=$((failures + 1)); }

assert_summary() {
    local output="$1" linked="$2" backed_up="$3" skipped="$4" label="$5"
    if grep -q "done: ${linked} linked, ${backed_up} backed up, ${skipped} already up to date" <<<"$output"; then
        pass "$label"
    else
        fail "$label (unexpected summary: $(tail -n1 <<<"$output"))"
    fi
}

file_count=$(find "$script_dir/files" \( -type f -o -type l \) | wc -l)

echo "=== fresh install ==="
out="$(run_install)"
assert_summary "$out" "$file_count" 0 0 "fresh install links every file, backs up nothing"

echo "=== re-run: fully idempotent, including broken symlinks in files/ ==="
out="$(run_install)"
assert_summary "$out" 0 0 "$file_count" "re-run touches nothing"

echo "=== existing symlink written with different (but equivalent) link text is left alone ==="
rm "$fake_home/.zshrc"
ln -s "$(realpath --relative-to="$fake_home" "$script_dir/files/.zshrc")" "$fake_home/.zshrc"
out="$(run_install)"
if grep -q '\.zshrc' <<<"$out"; then
    fail "relative-path symlink to the same target got touched"
else
    pass "relative-path symlink to the same target is recognized as up to date"
fi

echo "=== a real file already at the target gets backed up, not overwritten ==="
rm "$fake_home/.bashrc"
echo "# pre-existing user content" > "$fake_home/.bashrc"
out="$(run_install)"
backup="$(find "$fake_home" -maxdepth 1 -name '.bashrc.*.old*')"
if [[ -n "$backup" ]] && grep -q "pre-existing user content" "$backup" && [[ -L "$fake_home/.bashrc" ]]; then
    pass "pre-existing regular file backed up and replaced with symlink"
else
    fail "pre-existing regular file was not backed up correctly"
fi
if grep -q "diff \"$backup\"" <<<"$out"; then
    pass "divergent backup content surfaced as a diff command"
else
    fail "divergent backup content was not surfaced"
fi

echo "=== a symlink pointing at the wrong target gets backed up, not left alone ==="
rm "$fake_home/.gitconfig"
echo "other content" > "$fake_home/.other_gitconfig"
ln -s "$fake_home/.other_gitconfig" "$fake_home/.gitconfig"
out="$(run_install)"
backup="$(find "$fake_home" -maxdepth 1 -name '.gitconfig.*.old*')"
if [[ -n "$backup" ]] && [[ "$(readlink "$fake_home/.gitconfig")" == "$script_dir/files/.gitconfig" ]]; then
    pass "symlink pointing elsewhere backed up and replaced with correct symlink"
else
    fail "symlink pointing elsewhere was not backed up correctly"
fi

echo "=== steady state after all the above ==="
out="$(run_install)"
assert_summary "$out" 0 0 "$file_count" "converges back to fully idempotent"

echo
if [[ "$failures" -eq 0 ]]; then
    echo "all tests passed"
else
    echo "$failures test(s) failed"
    exit 1
fi
