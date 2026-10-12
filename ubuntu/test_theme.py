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
    def test_shell_plan_preserves_theme_against_popup_overrides(self):
        if not (theme.BLUR_DIR / "schemas/gschemas.compiled").exists():
            self.skipTest("Blur My Shell is not installed")
        popup = theme.settings(theme.BLUR_POPUP)
        popup.set_boolean("override-background", True)
        popup.set_boolean("preserve-shell-theme", False)
        with tempfile.TemporaryDirectory() as directory:
            backup = Path(directory) / "settings.json"
            theme.apply(theme.make_shell_plan(), backup)
            self.assertFalse(popup.get_boolean("override-background"))
            self.assertTrue(popup.get_boolean("preserve-shell-theme"))
            theme.restore(backup)
            self.assertTrue(popup.get_boolean("override-background"))
            self.assertFalse(popup.get_boolean("preserve-shell-theme"))

    def test_shell_only_preserves_files_and_restores_previous_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            css = home / ".local/share/themes/Tibeb/gnome-shell/gnome-shell.css"
            css.parent.mkdir(parents=True)
            css.write_text("/* previous custom theme */")
            backup = home / "files.json"
            theme.install_files(home, backup, shell_only=True)
            first_backup = backup.read_text()
            self.assertIn(".quick-settings", css.read_text())
            self.assertTrue(css.with_name("tibeb-weave.svg").exists())
            self.assertFalse((home / ".config/gtk-3.0/gtk.css").exists())
            theme.install_files(home, backup, shell_only=True)
            self.assertEqual(backup.read_text(), first_backup)
            theme.restore_files(home, backup)
            self.assertEqual(css.read_text(), "/* previous custom theme */")
            self.assertFalse(css.with_name("tibeb-weave.svg").exists())

    def test_shell_and_blur_extension_plans_merge_and_restore(self):
        shell = theme.settings("org.gnome.shell")
        user_theme = theme.settings(theme.SHELL)
        user_theme.set_string("name", "Previous")
        shell.set_strv("enabled-extensions", ["keep@example"])
        shell.set_strv("disabled-extensions", [theme.SHELL_ID, theme.BLUR_ID, "disabled@example"])
        plan = theme.make_plan(Path("/tmp/tibeb-test.png"))
        keys = [(e["schema"], e["path"], e["key"]) for e in plan]
        self.assertEqual(len(keys), len(set(keys)))
        with tempfile.TemporaryDirectory() as directory:
            backup = Path(directory) / "settings.json"
            theme.apply(plan, backup)
            self.assertEqual(user_theme.get_string("name"), "Tibeb")
            self.assertIn("keep@example", shell.get_strv("enabled-extensions"))
            self.assertIn(theme.SHELL_ID, shell.get_strv("enabled-extensions"))
            if (theme.BLUR_DIR / "schemas/gschemas.compiled").exists():
                self.assertIn(theme.BLUR_ID, shell.get_strv("enabled-extensions"))
                self.assertNotIn(theme.BLUR_ID, shell.get_strv("disabled-extensions"))
            self.assertNotIn(theme.SHELL_ID, shell.get_strv("disabled-extensions"))
            self.assertIn("disabled@example", shell.get_strv("disabled-extensions"))
            theme.restore(backup)
            self.assertEqual(user_theme.get_string("name"), "Previous")
            self.assertEqual(shell.get_strv("enabled-extensions"), ["keep@example"])
            self.assertEqual(shell.get_strv("disabled-extensions"),
                             [theme.SHELL_ID, theme.BLUR_ID, "disabled@example"])

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
