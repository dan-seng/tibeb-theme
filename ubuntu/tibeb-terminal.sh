#!/bin/sh
# A profile-local greeting; no changes to your shell startup files.
if [ -t 1 ] && [ "${TERM:-dumb}" != dumb ]; then
    printf '\033]0;Tibeb / ጥበብ\007'
    # Keep the header short; narrower panes receive a single-line signature.
    columns=$(tput cols 2>/dev/null) || columns=80
    case "$columns" in ''|*[!0-9]*) columns=80 ;; esac
    if [ "$columns" -ge 48 ]; then
        printf '\n\033[38;2;228;185;111m  ║◇║  \033[1;38;2;233;226;211mTIBEB  /  ጥበብ\033[0m\n'
        printf '\033[38;2;228;185;111m  ║◆║  \033[38;2;146;182;151mAncient patterns. Modern pixels.\033[0m\n'
        printf '\033[38;2;228;185;111m  ║◇║  ───────────────────────────────\033[0m\n\n'
    else
        printf '\n\033[38;2;228;185;111m  ◇  \033[1;38;2;233;226;211mTIBEB\033[0m\n\n'
    fi
fi
exec "${SHELL:-/bin/bash}" -l
