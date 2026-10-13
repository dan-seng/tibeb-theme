"""Run with GSETTINGS_BACKEND=memory /usr/bin/python3 ubuntu/test_icons.py."""
import os
if os.environ.get('GSETTINGS_BACKEND') != 'memory':
    raise SystemExit('Use GSETTINGS_BACKEND=memory')
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import icons
import theme

class IconsTest(unittest.TestCase):
    def test_assets_cover_battery_and_exclude_network(self):
        assets = icons.assets('Yaru-olive')
        for name, data in assets.items():
            self.assertNotIn('network', name)
            self.assertNotIn('wireless', name)
            if name.endswith('.svg'):
                ET.fromstring(data)
        for name in Path('/usr/share/icons/Yaru/scalable/status').glob('battery*.svg'):
            self.assertIn(f'.local/share/icons/{icons.NAME}/scalable/status/{name.name}', assets)
        self.assertNotEqual(icons.battery(0), icons.battery(100))
        self.assertNotEqual(icons.battery(50), icons.battery(50, True))

    def test_install_reapply_restore_preserves_inheritance(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            backup = home / 'files.json'
            theme.settings(theme.INTERFACE).set_string('icon-theme', 'Yaru-olive')
            theme.install_files(home, backup, icons_only=True)
            index = home / f'.local/share/icons/{icons.NAME}/index.theme'
            self.assertIn('Inherits=Yaru-olive', index.read_text())
            self.assertFalse((home / '.config/gtk-4.0/gtk.css').exists())
            theme.settings(theme.INTERFACE).set_string('icon-theme', icons.NAME)
            before = backup.read_text()
            theme.install_files(home, backup, icons_only=True)
            self.assertEqual(before, backup.read_text())
            self.assertIn('Inherits=Yaru-olive', index.read_text())
            theme.restore_files(home, backup)
            self.assertFalse(index.exists())

if __name__ == '__main__':
    unittest.main()
