#!/bin/sh
# Source from an interactive shell's startup file; never replaces that shell.
if [ -t 1 ] && [ "${TERM:-dumb}" != dumb ]; then
    printf '\n\033[1;38;2;233;226;211mTIBEB  /  ጥበብ\033[0m\n'
    printf '\033[38;2;228;185;111m  ║◆║  \033[38;2;146;182;151mAncient patterns. Modern pixels. Made in Ethiopia by Daniel G.\033[0m\n\n'
fi
