#!/usr/bin/python3
"""Apply and restore Tibeb on Ubuntu GNOME; uses the system PyGObject package."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import shlex
import sys
import tomllib
import uuid

from gi.repository import Gio, GLib

ROOT = Path(__file__).resolve().parent.parent
STATE = Path.home() / ".local/state/tibeb/ubuntu-backup.json"
FILE_STATE = Path.home() / ".local/state/tibeb/ubuntu-files.json"
BLUR_ID = "blur-my-shell@aunetx"
BLUR_DIR = Path.home() / ".local/share/gnome-shell/extensions" / BLUR_ID
BLUR = "org.gnome.shell.extensions.blur-my-shell.applications"
DESKTOP_BLUR_EXCLUSIONS = ("com.desktop.ding", "com.rastersoft.ding")
INTERFACE = "org.gnome.desktop.interface"
BACKGROUND = "org.gnome.desktop.background"
PROFILES = "org.gnome.Terminal.ProfilesList"
PROFILE = "org.gnome.Terminal.Legacy.Profile"
SHELL = "org.gnome.shell.extensions.user-theme"
PROFILE_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, "https://tibeb.local/ubuntu-terminal"))
PROFILE_PATH = f"/org/gnome/terminal/legacy/profiles:/:{PROFILE_ID}/"


def settings(schema, path=None):
    source = Gio.SettingsSchemaSource.get_default()
    definition = source.lookup(schema, True)
    if definition is None and (BLUR_DIR / "schemas/gschemas.compiled").exists():
        source = Gio.SettingsSchemaSource.new_from_directory(str(BLUR_DIR / "schemas"), source, False)
        definition = source.lookup(schema, True)
    if definition is None:
        raise RuntimeError(f"Required GNOME settings schema is missing: {schema}")
    return Gio.Settings.new_full(definition, None, path)


def read(entry):
    return settings(entry["schema"], entry["path"]).get_user_value(entry["key"])


def write(entry, value):
    target = settings(entry["schema"], entry["path"])
    if not target.is_writable(entry["key"]):
        raise RuntimeError(f"Setting is locked: {entry['schema']} {entry['key']}")
    if value is None:
        target.reset(entry["key"])
    else:
        parsed = GLib.Variant.parse(None, value, None, None)
        if not target.set_value(entry["key"], parsed):
            raise RuntimeError(f"Could not set {entry['key']}")
    Gio.Settings.sync()


def make_plan(wallpaper):
    with (ROOT / "colors.toml").open("rb") as source:
        colors = tomllib.load(source)
    plan = []

    def add(schema, key, value, path=None):
        target = settings(schema, path)
        if key not in target.props.settings_schema.list_keys():
            raise RuntimeError(f"Required setting is unavailable: {schema} {key}")
        kind = target.get_value(key).get_type_string()
        plan.append(dict(schema=schema, path=path, key=key,
                         value=GLib.Variant(kind, value).print_(True)))

    if not Path("/usr/share/themes/Yaru-yellow-dark/gtk-3.0/gtk.css").exists():
        raise RuntimeError("Install Ubuntu's yaru-theme-gtk package first.")
    if not Path("/usr/share/icons/Yaru-olive").is_dir():
        raise RuntimeError("Install Ubuntu's yaru-theme-icon package first.")
    add(INTERFACE, "gtk-theme", "Yaru-yellow-dark")
    add(INTERFACE, "color-scheme", "prefer-dark")
    add(INTERFACE, "icon-theme", "Yaru-olive")
    add("org.gnome.desktop.wm.preferences", "button-layout", "close,minimize,maximize:")
    if "accent-color" in settings(INTERFACE).props.settings_schema.list_keys():
        add(INTERFACE, "accent-color", "yellow")
    for key in ("picture-uri", "picture-uri-dark"):
        add(BACKGROUND, key, wallpaper.as_uri())
    add(BACKGROUND, "picture-options", "zoom")
    add(BACKGROUND, "primary-color", colors["background"])
    add(BACKGROUND, "secondary-color", colors["background"])
    if Gio.SettingsSchemaSource.get_default().lookup(SHELL, True):
        add(SHELL, "name", "")

    terminal = {
        "visible-name": "Tibeb",
        "use-theme-colors": False,
        "background-color": colors["background"],
        "foreground-color": colors["foreground"],
        "bold-color-same-as-fg": True,
        "cursor-colors-set": True,
        "cursor-background-color": colors["accent"],
        "cursor-foreground-color": colors["background"],
        "highlight-colors-set": True,
        "highlight-background-color": colors["selection"],
        "highlight-foreground-color": colors["bright_foreground"],
        "use-transparent-background": True,
        "background-transparency-percent": 18,
        "use-theme-transparency": False,
        "use-custom-command": True,
        "custom-command": "/bin/sh " + shlex.quote(str(Path.home() / ".local/share/tibeb/tibeb-terminal.sh")),
        "palette": [colors[key] for key in (
            "background", "red", "green", "yellow", "blue", "magenta", "cyan",
            "light_foreground", "dark_foreground", "bright_red", "bright_green",
            "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan", "bright_foreground")],
    }
    for key, value in terminal.items():
        add(PROFILE, key, value, PROFILE_PATH)
    profiles = settings(PROFILES).get_strv("list")
    if PROFILE_ID not in profiles:
        profiles.append(PROFILE_ID)
    add(PROFILES, "list", profiles)
    add(PROFILES, "default", PROFILE_ID)
    if (BLUR_DIR / "schemas/gschemas.compiled").exists():
        # DING's transparent desktop window covers the wallpaper. Its application
        # ID changed; keep both names excluded when enabling blur for all apps.
        blacklist = settings(BLUR).get_strv("blacklist")
        for desktop_id in DESKTOP_BLUR_EXCLUSIONS:
            if desktop_id not in blacklist:
                blacklist.append(desktop_id)
        add(BLUR, "blacklist", blacklist)
        for key, value in {
            "blur": True, "enable-all": True, "sigma": 30,
            "brightness": 0.8, "opacity": 235, "dynamic-opacity": False,
            "unblur-when-fullscreen": True,
        }.items():
            add(BLUR, key, value)
        shell = settings("org.gnome.shell")
        enabled = shell.get_strv("enabled-extensions")
        if BLUR_ID not in enabled:
            enabled.append(BLUR_ID)
        add("org.gnome.shell", "enabled-extensions", enabled)
        add("org.gnome.shell", "disabled-extensions",
            [item for item in shell.get_strv("disabled-extensions") if item != BLUR_ID])
    else:
        print("Blur My Shell is not installed; transparency will work without background blur.", file=sys.stderr)
    return plan


def install_files(home, backup_path):
    """Preserve files and symlinks before installing the GTK controls and greeting."""
    snapshot = json.loads(backup_path.read_text()) if backup_path.exists() else {}
    css = (ROOT / "ubuntu/controls.css").read_text()
    files = {
        ".config/gtk-3.0/gtk.css": css,
        ".config/gtk-4.0/gtk.css": css,
        ".local/share/tibeb/tibeb-terminal.sh": (ROOT / "ubuntu/tibeb-terminal.sh").read_text(),
    }
    for relative, content in files.items():
        path = home / relative
        if relative not in snapshot:
            snapshot[relative] = {
                "data": base64.b64encode(path.read_bytes()).decode() if path.exists() else None,
                "link": str(path.readlink()) if path.is_symlink() else None,
                "mode": path.stat().st_mode & 0o777 if path.exists() else 0o644,
            }
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path.write_text(json.dumps(snapshot, indent=2) + "\n")
    backup_path.chmod(0o600)
    for relative, content in files.items():
        path = home / relative
        previous = snapshot[relative]
        if relative.endswith("gtk.css") and previous["data"] is not None:
            content = base64.b64decode(previous["data"]).decode() + "\n" + content
        path.parent.mkdir(parents=True, exist_ok=True)
        # Replace a symlink itself; never modify its target.
        if path.is_symlink():
            path.unlink()
        path.write_text(content)


def restore_files(home, backup_path):
    if not backup_path.exists():
        return
    for relative, original in json.loads(backup_path.read_text()).items():
        path = home / relative
        path.unlink(missing_ok=True)
        if original["link"] is not None:
            path.symlink_to(original["link"])
        elif original["data"] is not None:
            path.write_bytes(base64.b64decode(original["data"]))
            path.chmod(original["mode"])
    backup_path.unlink()


def apply(plan, backup_path):
    # Preserve the original snapshot across repeated applications.
    if backup_path.exists():
        snapshot = json.loads(backup_path.read_text())
    else:
        snapshot = []
    known = {(e["schema"], e["path"], e["key"]) for e in snapshot}
    before = []
    for entry in plan:
        value = read(entry)
        original = dict(entry, value=value.print_(True) if value is not None else None)
        before.append(original)
        if (entry["schema"], entry["path"], entry["key"]) not in known:
            snapshot.append(original)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = backup_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(snapshot, indent=2) + "\n")
    temporary.chmod(0o600)
    temporary.replace(backup_path)
    try:
        for entry in plan:
            write(entry, entry["value"])
    except Exception:
        for entry in reversed(before):
            write(entry, entry["value"])
        raise


def restore(backup_path):
    snapshot = json.loads(backup_path.read_text())
    for entry in reversed(snapshot):
        write(entry, entry["value"])
    backup_path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preview", "apply", "restore"))
    args = parser.parse_args()
    if args.action == "restore":
        if not STATE.exists():
            raise RuntimeError("No Ubuntu settings backup exists; nothing to restore.")
        restore(STATE)
        restore_files(Path.home(), FILE_STATE)
        print("Restored your previous desktop settings and terminal profile selection.")
        return
    source = ROOT / "backgrounds/tibeb-highlands.png"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    wallpaper = Path.home() / f".local/share/backgrounds/tibeb/highlands-{digest}.png"
    plan = make_plan(wallpaper)
    if args.action == "preview":
        for entry in plan:
            print(f"{entry['schema']} {entry['key']} = {entry['value']}")
        print(f"Backup: {STATE}")
        return
    wallpaper.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, wallpaper)
    install_files(Path.home(), FILE_STATE)
    apply(plan, STATE)
    print(f"Applied Tibeb. Original settings saved to {STATE}")
    print("Open a new GNOME Terminal window to use the Tibeb profile.")
    print(f"Restore with: /usr/bin/python3 {Path(__file__).resolve()} restore")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, GLib.Error) as error:
        sys.exit(f"Tibeb: {error}")
