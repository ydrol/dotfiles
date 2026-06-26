# ~/.zshrc: sourced by zsh for interactive shells.
# Converted from a Debian/Ubuntu .bashrc.

# --- History ---------------------------------------------------------------
HISTFILE="$HOME/.zsh_history"
HISTSIZE=1000          # lines kept in memory for the session
SAVEHIST=2000          # lines written to $HISTFILE

setopt HIST_IGNORE_DUPS      # don't record a line identical to the previous one
setopt HIST_IGNORE_SPACE     # don't record lines that start with a space
setopt APPEND_HISTORY        # add to the history file rather than overwrite it
setopt INC_APPEND_HISTORY    # write each command as it finishes
# setopt SHARE_HISTORY       # uncomment to share history live across open shells

# --- Shell options ---------------------------------------------------------
# setopt EXTENDED_GLOB       # zsh's extended globbing (rough equivalent of globstar)

# --- ls / grep colours -----------------------------------------------------
# Run dircolors first so LS_COLORS is set before completion colouring uses it.
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# --- Completion ------------------------------------------------------------
# zsh's native completion system (replaces bash-completion).
autoload -Uz compinit && compinit
# bashcompinit lets bash-style completion scripts (e.g. nvm) work under zsh.
autoload -Uz bashcompinit && bashcompinit
# Colour completion listings using the same palette as ls.
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# --- chroot marker (used in the prompt below) ------------------------------
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# --- Prompt ----------------------------------------------------------------
# PROMPT_SUBST lets $debian_chroot expand at prompt-draw time.
setopt PROMPT_SUBST
# Mirrors the bash default: green user@host, blue cwd, % (or # for root).
PROMPT='${debian_chroot:+($debian_chroot)}%F{green}%n@%m%f:%F{blue}%~%f%# '

# Set the terminal title to user@host: dir on xterm-like terminals.
case "$TERM" in
xterm*|rxvt*)
    precmd() { print -Pn "\e]0;${debian_chroot:+($debian_chroot)}%n@%m: %~\a" }
    ;;
esac

# --- lesspipe --------------------------------------------------------------
# Make less friendlier with non-text input.
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# Make cd act like pushd, adding directories to the stack
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
# Do not print the directory stack every time you change directories
#setopt PUSHD_SILENT
DIRSTACKSIZE=10

source ~/.profile
source ~/.shellrc



