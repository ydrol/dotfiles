#!/bin/bash
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd')
HOST=$(hostname -s)
printf '\033]9;%s - %s:%s\033\\' "${1:-Claude Code}" "$HOST" "$CWD"
