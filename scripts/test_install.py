"""Exercise portable icons in temporary directories without changing the desktop."""
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import install_icons


class InstallerTests(unittest.TestCase):
    def test_install_and_upgrade_preserve_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            installed = install_icons.install(home, 'Adwaita')
            self.assertIn('Inherits=Adwaita', (installed / 'index.theme').read_text())
            self.assertIn('Name=Tibeb-Omarchy', (installed / 'index.theme').read_text())
            self.assertTrue((installed / 'scalable/places/folder-projects.svg').exists())
            for svg in installed.rglob('*.svg'):
                ET.parse(svg)
                self.assertNotIn('wireless', svg.name)
                self.assertNotIn('network', svg.name)
            (installed / 'keep.txt').write_text('previous user asset')
            install_icons.install(home, 'Adwaita')
            saved = list((home / '.local/state/tibeb/backups').glob('icons.*/Tibeb-Omarchy/keep.txt'))
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0].read_text(), 'previous user asset')

    def test_existing_symlink_target_is_not_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            target = home / 'original'
            target.mkdir()
            (target / 'sentinel').write_text('untouched')
            destination = home / '.local/share/icons/Tibeb-Omarchy'
            destination.parent.mkdir(parents=True)
            destination.symlink_to(target)
            install_icons.install(home, 'Adwaita')
            self.assertEqual((target / 'sentinel').read_text(), 'untouched')
            self.assertFalse(destination.is_symlink())
            saved = list((home / '.local/state/tibeb/backups').glob('icons.*/Tibeb-Omarchy'))
            self.assertTrue(saved[0].is_symlink())


if __name__ == '__main__':
    unittest.main()
