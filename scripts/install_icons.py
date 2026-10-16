#!/usr/bin/env python3
"""Install the portable Tibeb icon layer without GNOME or Python GI dependencies."""
import argparse
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'ubuntu'))
import icons

NAME = 'Tibeb-Omarchy'


def choose_parent(home):
    roots = [home / '.local/share/icons', home / '.icons', Path('/usr/local/share/icons'), Path('/usr/share/icons')]
    for name in ('Yaru-olive', 'Papirus-Dark', 'Adwaita', 'hicolor'):
        if any((root / name / 'index.theme').is_file() for root in roots):
            return name
    raise RuntimeError('No base icon theme found. Install adwaita-icon-theme, then retry.')


def install(home, parent=None):
    parent = parent or choose_parent(home)
    directory = home / '.local/share/icons'
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / NAME
    staging = Path(tempfile.mkdtemp(prefix='.tibeb-icons-', dir=directory))
    backup = None
    try:
        prefix = f'.local/share/icons/{icons.NAME}/'
        for relative, content in icons.assets(parent).items():
            path = staging / relative.removeprefix(prefix)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.name == 'index.theme':
                content = content.replace(f'Name={icons.NAME}', f'Name={NAME}')
            path.write_text(content)
        if destination.exists() or destination.is_symlink():
            backups = home / '.local/state/tibeb/backups'
            backups.mkdir(parents=True, exist_ok=True)
            backup = Path(tempfile.mkdtemp(prefix='icons.', dir=backups)) / NAME
            destination.rename(backup)
        try:
            staging.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    print(f'Installed {destination} (inherits {parent})')
    if backup:
        print(f'Previous icons saved to {backup}')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        install(Path.home())
    except (OSError, RuntimeError) as error:
        sys.exit(f'Icon installation failed: {error}')
