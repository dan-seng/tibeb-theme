# Tibeb for Ubuntu GNOME

This version uses Tibeb's original wallpaper and exact terminal palette, with
Ubuntu's native Yaru yellow dark widgets, olive icons, and yellow system accent.
GNOME's native yellow is an approximation of Tibeb gold; this does not replace
every application's colors. Applications that ignore system appearance settings
may need their own dark-mode setting.

Quick Settings has its own Tibeb Shell theme: charcoal surfaces, ivory sans-serif
labels, outlined gold toggles, slim gold sliders, and a vector woven edge. It
keeps GNOME's real controls, submenu buttons, keyboard focus, and live statuses.
The panel is opaque to keep it readable independently of wallpaper blur.
The overlay imports the installed Yaru dark Shell stylesheet for other surfaces.
Prepared for GNOME Shell 50; other versions may need selector adjustments.

The theme also adds red/yellow/green window controls to GTK 3 and GTK 4 apps,
places the controls on the left, and gives the Tibeb terminal profile 8%
background transparency, Ubuntu Mono 12 with comfortable line spacing, a gold
block cursor, and a compact woven greeting in gold, ivory, and sage. Narrow
windows get a one-line signature. The greeting launches
your normal login shell without modifying its startup files.

When Blur My Shell is already installed in your user extensions directory,
the installer enables application blur for all eligible windows, with 92%
window opacity and a blur radius setting of 30. This slightly affects text as
well as backgrounds because GNOME applies opacity to the whole window.
Fullscreen windows are excluded; the extension's existing blacklist is kept,
with both legacy and current Desktop Icons NG application IDs added so the
transparent desktop window cannot blur the wallpaper after login or wake.
Without the extension, Terminal transparency still works but blur does not.

Fully close and reopen apps to load the GTK controls. Apps with custom-drawn
controls (including some Electron apps and browsers) and sandboxed apps that
cannot read host GTK styles may retain their own buttons. This is not a universal
replacement for every application's window decorations.

Requires Ubuntu GNOME, GNOME Terminal, Yaru GTK/icon themes, and the system
Python 3.11+ with PyGObject. Prepared on Ubuntu 26.04. Run from the project root:

```bash
# Read the proposed settings without changing anything:
/usr/bin/python3 ubuntu/theme.py preview

# Save your current settings and apply Tibeb:
/usr/bin/python3 ubuntu/theme.py apply

# Return to your saved settings:
/usr/bin/python3 ubuntu/theme.py restore
```

To install and apply only Quick Settings, preserving the current wallpaper,
terminal, GTK appearance, and application blur settings:

```bash
/usr/bin/python3 ubuntu/theme.py apply-shell
```

To apply only the terminal profile and greeting, use
`/usr/bin/python3 ubuntu/theme.py apply-terminal`. Open a new terminal window
to see the greeting. Your existing shell prompt and startup files stay intact.
The woven motif is a welcome header, not a permanent border around command output.

GNOME Files 50 also has scoped Tibeb styling: charcoal content, a darker sidebar
with a woven edge, ivory labels, and gold selection outlines and breadcrumbs.
Apply it with `/usr/bin/python3 ubuntu/theme.py apply-files`, then fully close
and reopen Files. The GTK 4 import and assets are backed up; other applications
do not receive the Files color overrides. Native file navigation, search,
selection, and transfer controls remain in place.

This requires `yaru-theme-gnome-shell` and GNOME's User Themes extension.
The theme is installed under `~/.local/share/themes/Tibeb/gnome-shell/`, and
User Themes is enabled if needed. Close and reopen the system menu to see it.
Its CSS and vector trim are backed up with the other managed files. If all
extensions are globally disabled, enable them in the Extensions app first.
When Blur My Shell is installed, popup background overrides are turned off and
its preserve-theme option is enabled where supported. This prevents it from
erasing the woven edge and recoloring the toggles. These settings affect popup
surfaces and are included in the restore backup; application blur stays enabled.
The restore command restores the entire saved Tibeb setup, including the
previous Shell theme; it is not limited to the most recent apply operation.

No sudo is needed. Open a new GNOME Terminal window after applying; existing
windows keep their current profile. You can also select Tibeb in Terminal's
profile menu. Your existing profiles are not edited. If GNOME's User Themes
extension is installed, the Tibeb Shell theme is selected; your previous
selection is included in the backup. Unrelated extension choices are preserved.

The first backup is kept in `~/.local/state/tibeb/ubuntu-backup.json` until you
restore. Reapplying does not overwrite that original snapshot. Restore resets
only the settings managed by this tool to their saved values, including the
terminal profile list and default. Restore before making unrelated profile-list
changes you want to keep. The wallpaper copy remains in
`~/.local/share/backgrounds/tibeb/` after restoration.

GTK styles and the terminal greeting are separately backed up in
`~/.local/state/tibeb/ubuntu-files.json`. Existing GTK CSS is preserved and
extended; restore reinstates original files or symlinks. Blur settings and the
extension enablement lists are included in the settings backup. Restore before
making unrelated extension-list changes you want to keep.

The Omarchy palette and installation remain available in the project root for
your later migration.

To run the settings and rollback tests without touching your desktop:

```bash
GSETTINGS_BACKEND=memory /usr/bin/python3 ubuntu/test_theme.py
```

## Simple folder and battery icons

Run `/usr/bin/python3 ubuntu/theme.py apply-icons` to install the Tibeb icon
layer. It provides ivory folder outlines with tricolor tabs and coffee-cup
battery levels, including charging and missing-battery states. Templates uses
nested diamonds, with no cross motif. GNOME symbolic icons follow the Shell's
foreground color; full-color versions retain the tricolor and gold fill.

The layer inherits the currently selected icon theme, preserving Wi-Fi and other
unrelated icons. Reopen Files to refresh cached icons; if the top bar still shows
the previous battery, log out and back in. The Projects folder receives its obelisk icon automatically through GNOME folder
metadata, with its previous assignment backed up for restore. Code and Archive
icons are available by name for custom folders; ordinary folders use the generic
design. The rendered `previews/folder-icons.png` shows the actual SVG assets.
Settings and installed assets use the existing Tibeb restore backups. The full
`apply` command selects Yaru-olive again; run `apply-icons` afterwards to reselect
this optional layer. Run icon checks with
`GSETTINGS_BACKEND=memory /usr/bin/python3 ubuntu/test_icons.py`.

## Desktop polish

`/usr/bin/python3 ubuntu/theme.py apply-polish` installs the GNOME Shell 50
extension `tibeb-desktop-v2@local`. Log out and back in after its first installation.
It adds an ivory clock with a gold underline, a live coffee battery with red fill
strictly below 15% and a lightning mark while charging, and the Tibeb wallpaper
with a subtle diamond border on the lock screen. Wi-Fi is unchanged. The lock
screen keeps native authentication, notifications, and background blur. This
styles your session lock screen, not the system login screen.

It also creates Code and Archive in your home directory if absent and assigns
matching icons, alongside Projects. Previous folder metadata is backed up.
Restore removes the icon assignments but leaves these directories and any
contents in place. The terminal greeting reads “Ancient patterns. Modern pixels.
Made in Ethiopia by Daniel G.”; narrow panes retain the compact greeting.

The extension uses GNOME 50 Shell internals and must be reviewed before enabling
it on another major version. Live lock-screen appearance requires checking after
login. Disable it in Extensions to return to the native clock, battery rendering,
and lock background. The existing `restore` command restores managed settings,
files, and folder metadata. The battery is drawn directly in the panel and menu and repaints on UPower
property changes, avoiding icon-image caching and fallback icons. Version 2
replaces the earlier extension and needs a fresh login to load its code.
Tests: `node ubuntu/test_coffee.mjs`, `node ubuntu/test_battery.mjs`, plus the Python
theme and icon tests above.
