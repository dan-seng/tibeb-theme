#!/bin/sh
# A profile-local greeting; no changes to your shell startup files.
printf '\033]0;Tibeb / ጥበብ\007'
printf '\n\033[38;2;228;185;111m  ◇ ◆ ◇ ━━━━━━━━━━━━━━━━━━━━━ ◇ ◆ ◇\033[0m\n'
printf '\033[1;38;2;233;226;211m           T I B E B  /  ጥበብ\033[0m\n'
printf '\033[38;2;146;182;151m       Ancient patterns. Modern pixels.\033[0m\n'
printf '\033[38;2;228;185;111m  ◇ ◆ ◇ ━━━━━━━━━━━━━━━━━━━━━ ◇ ◆ ◇\033[0m\n\n'
exec "${SHELL:-/bin/bash}" -l
