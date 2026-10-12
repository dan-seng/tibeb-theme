# Tibeb for Ubuntu GNOME

This version uses Tibeb's original wallpaper and exact terminal palette, with
Ubuntu's native Yaru yellow dark widgets, olive icons, and yellow system accent.
GNOME's native yellow is an approximation of Tibeb gold; this does not replace
every application's colors. Applications that ignore system appearance settings
may need their own dark-mode setting.

The theme also adds red/yellow/green window controls to GTK 3 and GTK 4 apps,
places the controls on the left, and gives the Tibeb terminal profile 18%
background transparency and a woven-pattern greeting. The greeting launches
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

No sudo is needed. Open a new GNOME Terminal window after applying; existing
windows keep their current profile. You can also select Tibeb in Terminal's
profile menu. Your existing profiles are not edited. If GNOME's User Themes
extension is installed, its custom Shell theme is reset to the system theme;
your previous selection is included in the backup. Extensions remain enabled.

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
