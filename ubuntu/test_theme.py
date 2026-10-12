"""Run with GSETTINGS_BACKEND=memory /usr/bin/python3 ubuntu/test_theme.py."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

if os.environ.get("GSETTINGS_BACKEND") != "memory":
    raise SystemExit("Tests require GSETTINGS_BACKEND=memory; refusing to change your desktop.")

import theme


class ThemeTest(unittest.TestCase):
    def test_desktop_blur_exclusions_preserve_existing_and_restore(self):
        if not (theme.BLUR_DIR / "schemas/gschemas.compiled").exists():
            self.skipTest("Blur My Shell is not installed")
        blur = theme.settings(theme.BLUR)
        original = ["CustomApp", "com.desktop.ding"]
        blur.set_strv("blacklist", original)
        plan = theme.make_plan(Path("/tmp/tibeb-test.png"))
        plan = [e for e in plan if e["schema"] == theme.BLUR and e["key"] == "blacklist"]
        self.assertEqual(len(plan), 1)
        with tempfile.TemporaryDirectory() as directory:
            backup = Path(directory) / "backup.json"
            theme.apply(plan, backup)
            expected = original + ["com.rastersoft.ding"]
            self.assertEqual(blur.get_strv("blacklist"), expected)
            repeated = theme.make_plan(Path("/tmp/tibeb-test.png"))
            theme.apply([e for e in repeated if e["schema"] == theme.BLUR
                         and e["key"] == "blacklist"], backup)
            self.assertEqual(blur.get_strv("blacklist"), expected)
            theme.restore(backup)
            self.assertEqual(blur.get_strv("blacklist"), original)

    def test_file_backup_preserves_symlink_and_repeated_apply(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original = home / "original.css"
            original.write_text("/* existing theme */\n")
            css = home / ".config/gtk-3.0/gtk.css"
            css.parent.mkdir(parents=True)
            css.symlink_to(original)
            backup = home / "backup.json"
            theme.install_files(home, backup)
            first = css.read_text()
            self.assertIn("#ff6058", first)
            self.assertFalse(css.is_symlink())
            self.assertEqual(original.read_text(), "/* existing theme */\n")
            theme.install_files(home, backup)
            self.assertEqual(css.read_text(), first)
            theme.restore_files(home, backup)
            self.assertTrue(css.is_symlink())
            self.assertFalse((home / ".config/gtk-4.0/gtk.css").exists())

    def test_apply_repeat_and_restore(self):
        original = theme.settings(theme.INTERFACE)
        original.set_string("gtk-theme", "Before Tibeb")
        original.reset("icon-theme")
        profiles = theme.settings(theme.PROFILES)
        previous_profiles = profiles.get_strv("list")
        previous_default = profiles.get_string("default")
        plan = theme.make_plan(Path("/tmp/tibeb-test.png"))
        with tempfile.TemporaryDirectory() as directory:
            backup = Path(directory) / "backup.json"
            theme.apply(plan, backup)
            saved = backup.read_text()
            self.assertEqual(original.get_string("gtk-theme"), "Yaru-yellow-dark")
            self.assertEqual(profiles.get_string("default"), theme.PROFILE_ID)
            self.assertTrue(set(previous_profiles).issubset(profiles.get_strv("list")))
            self.assertEqual(len(theme.settings(theme.PROFILE, theme.PROFILE_PATH).get_strv("palette")), 16)
            theme.apply(theme.make_plan(Path("/tmp/tibeb-test.png")), backup)
            self.assertEqual(backup.read_text(), saved)
            theme.restore(backup)
            self.assertEqual(original.get_string("gtk-theme"), "Before Tibeb")
            self.assertIsNone(original.get_user_value("icon-theme"))
            self.assertEqual(profiles.get_strv("list"), previous_profiles)
            self.assertEqual(profiles.get_string("default"), previous_default)
            self.assertFalse(backup.exists())

    def test_failed_apply_rolls_back(self):
        plan = theme.make_plan(Path("/tmp/tibeb-test.png"))
        original = theme.settings(theme.INTERFACE).get_string("gtk-theme")
        real_write = theme.write
        count = 0

        def fail_once(entry, value):
            nonlocal count
            count += 1
            if count == 3:
                raise RuntimeError("Simulated settings failure")
            real_write(entry, value)

        with tempfile.TemporaryDirectory() as directory:
            with patch.object(theme, "write", side_effect=fail_once):
                with self.assertRaisesRegex(RuntimeError, "Simulated"):
                    theme.apply(plan, Path(directory) / "backup.json")
        self.assertEqual(theme.settings(theme.INTERFACE).get_string("gtk-theme"), original)


if __name__ == "__main__":
    unittest.main()
