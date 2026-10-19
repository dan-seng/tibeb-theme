#!/usr/bin/env bash
# Ubuntu GNOME installer: applies the complete Tibeb experience in one command.
# Runs the wallpaper/GTK theme, terminal profile, Quick Settings Shell theme,
# custom icon layer, and the desktop-polish extension. No sudo is required.
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: bash ubuntu/install.sh [--preview | --restore]

  (no option)  Install and apply the full Tibeb theme
  --preview    Print the planned settings without changing anything
  --restore    Return to the settings saved before the last install
EOF
}

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
theme="$source_dir/theme.py"
python=/usr/bin/python3
mode=${1:-}

case "$mode" in
  ""|--preview|--restore) ;;
  -h|--help) usage; exit 0 ;;
  *) usage; exit 2 ;;
esac
if (( $# > 1 )); then
  usage
  exit 2
fi

if [[ ! -x $python || ! -f $theme ]]; then
  echo "This installer must run on Ubuntu with its system Python 3 ($python)." >&2
  exit 1
fi

# The theme targets Ubuntu's GNOME desktop; warn rather than fail so it can
# still run from a fresh TTY before logging in.
if [[ ${XDG_CURRENT_DESKTOP:-} != *GNOME* ]]; then
  echo "Warning: GNOME was not detected in XDG_CURRENT_DESKTOP; applying anyway." >&2
fi

if ! "$python" -c 'import tomllib' >/dev/null 2>&1; then
  echo "Ubuntu's system Python 3.11 or newer is required (needs the tomllib module)." >&2
  exit 1
fi

packages=()
"$python" -c 'import gi' >/dev/null 2>&1 || packages+=(python3-gi)
"$python" - <<'PY' >/dev/null 2>&1 || packages+=(gnome-terminal)
import sys
from gi.repository import Gio
ok = Gio.SettingsSchemaSource.get_default().lookup("org.gnome.Terminal.ProfilesList", True)
sys.exit(0 if ok else 1)
PY
for package in yaru-theme-gtk yaru-theme-icon yaru-theme-gnome-shell; do
  case "$package" in
    yaru-theme-gtk) probe=/usr/share/themes/Yaru-yellow-dark/gtk-3.0/gtk.css ;;
    yaru-theme-icon) probe=/usr/share/icons/Yaru-olive ;;
    yaru-theme-gnome-shell) probe=/usr/share/gnome-shell/theme/Yaru-dark/gnome-shell.css ;;
  esac
  [[ -e $probe ]] || packages+=("$package")
done

if (( ${#packages[@]} )); then
  echo "Missing required packages:" >&2
  printf '  - %s\n' "${packages[@]}" >&2
  echo "Install them with:" >&2
  echo "  sudo apt install ${packages[*]}" >&2
  echo "Then run this installer again." >&2
  exit 1
fi

run() {
  echo "==> tibeb: $*"
  "$python" "$theme" "$@"
}

case "$mode" in
  --preview)
    run preview
    exit 0
    ;;
  --restore)
    run restore
    echo
    echo "Tibeb settings restored. Open a new terminal window to see the change."
    exit 0
    ;;
esac

# apply         -> wallpaper, GTK theme, window controls, terminal, Shell theme
# apply-icons   -> Tibeb folder and battery icons (after apply reselects them)
# apply-polish  -> desktop extension: clock, coffee battery, lock-screen wallpaper
run apply
run apply-icons
run apply-polish

cat <<'EOF'

Tibeb is installed and applied. Finish with these steps:
  1. Open a new GNOME Terminal window to load the Tibeb profile.
  2. Log out and back in to load the desktop extension and refresh the top bar.
  3. Reopen Files to refresh cached folder icons.
If User Themes or the extension is disabled, enable it in the Extensions app.
Restore everything with: bash ubuntu/install.sh --restore
EOF
