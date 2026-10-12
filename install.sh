#!/usr/bin/env bash
# Local installer; Omarchy does not execute this when installing from a URL.
set -euo pipefail

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
apply=false
case "${1:-}" in
  --apply) apply=true ;;
  "") ;;
  *) echo "Usage: bash install.sh [--apply]" >&2; exit 2 ;;
esac
if (( $# > 1 )); then
  echo "Usage: bash install.sh [--apply]" >&2
  exit 2
fi

python3 "$source_dir/scripts/validate.py"
if ! command -v omarchy-theme-set-templates >/dev/null 2>&1; then
  echo "A template-based Omarchy installation is required. Run this on your Omarchy desktop after updating Omarchy." >&2
  exit 1
fi
if "$apply" && ! command -v omarchy-theme-set >/dev/null 2>&1; then
  echo "Cannot apply: omarchy-theme-set is not available." >&2
  exit 1
fi

themes_dir="$HOME/.config/omarchy/themes"
destination="$themes_dir/tibeb"
mkdir -p -- "$themes_dir"
staging=$(mktemp -d "$themes_dir/.tibeb-install.XXXXXX")
trap 'rm -rf -- "$staging"' EXIT
mkdir -- "$staging/backgrounds"
cp -- "$source_dir/colors.toml" "$source_dir/icons.theme" "$source_dir/preview.png" "$staging/"
cp -- "$source_dir/backgrounds/tibeb-highlands.png" "$staging/backgrounds/"

if [[ -e $destination || -L $destination ]]; then
  backup_dir="$HOME/.local/state/tibeb/backups"
  mkdir -p -- "$backup_dir"
  backup=$(mktemp -d "$backup_dir/install.XXXXXX")
  mv -- "$destination" "$backup/tibeb"
  echo "Previous installation saved to $backup/tibeb"
  if ! mv -- "$staging" "$destination"; then
    mv -- "$backup/tibeb" "$destination"
    exit 1
  fi
else
  mv -- "$staging" "$destination"
fi

echo "Installed Tibeb in $destination"
if "$apply"; then
  omarchy-theme-set tibeb
else
  echo "Apply it with: omarchy-theme-set tibeb"
fi
