# TIBEB / ጥበብ — Omarchy Theme

**Ancient patterns. Modern pixels.**

TIBEB is an Ethiopian-inspired, dark-first Omarchy theme built around volcanic charcoal, highland gold, the structure of woven *tibeb* borders, and the warmth of natural cotton. It takes inspiration from Ethiopia without resorting to a literal green-yellow-red flag overlay.

![TIBEB theme concept preview](preview.png)

> **Preview disclosure:** `preview.png` is a designed **desktop concept mockup**, not a screenshot from a running Omarchy installation. Actual terminal layout, icons, widgets, and fonts are controlled by the installed system and your configuration.

## Try it on Ubuntu first

The [Ubuntu GNOME edition](ubuntu/README.md) applies the wallpaper, a dedicated
GNOME Terminal profile, and matching native dark desktop colors. It saves your
current settings so you can restore them:

```bash
/usr/bin/python3 ubuntu/theme.py apply
# Undo:
/usr/bin/python3 ubuntu/theme.py restore
```

The Omarchy theme below remains ready for your later switch.

## Included

- `colors.toml` — native dark Omarchy palette. On supported Omarchy builds, this drives colors across Hyprland, shell UI, terminals, editors, and compatible apps.
- `backgrounds/tibeb-highlands.png` — original wallpaper designed for this theme, with Ethiopian-inspired highland atmosphere and abstract geometric motifs.
- `icons.theme` — standard Yaru-olive icons for an earthy look (when available).
- `preview.png` — 16:9 competition/chooser concept preview.

## Install on Omarchy

Run these commands **inside your Omarchy desktop session**, as your normal user.
You need Git, Python 3.11+, and an up-to-date Omarchy installation with
`omarchy-theme-set` and `omarchy-theme-set-templates` on your PATH.

```bash
git clone https://github.com/dan-seng/tibeb-theme.git
cd tibeb-theme
bash install.sh --apply
```

If you already have this checkout, run `bash install.sh --apply` from its root.
Use `bash install.sh` to install without changing the active desktop theme;
select it later with `omarchy-theme-set tibeb` or **Style → Theme → Tibeb**.
No sudo is required by the installer.

The installer validates the assets, installs the palette and wallpaper into
`~/.config/omarchy/themes/tibeb`, and installs the custom SVG icons into
`~/.local/share/icons/Tibeb-Omarchy`. Omarchy selects these icons through the
installed `icons.theme` file. Existing installations are moved to unique backups
under `~/.local/state/tibeb/backups/`; their paths are printed during installation.
Re-running the installer upgrades both parts and retains the previous versions.

The icon layer inherits Yaru-olive, Papirus-Dark, Adwaita, or hicolor, whichever
is available in that order. It includes the approved folder symbols and static
coffee battery icons, with nested diamonds instead of a cross. It supplies no
Wi-Fi overrides. If no base theme is found, install one and retry:

```bash
sudo pacman -S --needed adwaita-icon-theme
bash install.sh --apply
```

Close and reopen your file manager if it retains cached icons. Standard folders
(Home, Documents, Downloads, Pictures, Music, Videos, Templates, and Public)
resolve through their normal icon names. Custom folders can be assigned an icon
using your file manager's folder properties. For file managers supporting GVfs
icon metadata, these commands assign the additional icons:

```bash
mkdir -p ~/Projects ~/Code ~/Archive
gio set ~/Projects metadata::custom-icon-name folder-projects
gio set ~/Code metadata::custom-icon-name folder-code
gio set ~/Archive metadata::custom-icon-name folder-archive
```

These optional commands require `gio` and a running GVfs metadata service. They
are not run automatically, because file managers differ in custom-icon support.

### Terminal greeting

The installer includes a shell-independent greeting helper. Add this line once
to `~/.bashrc` (Bash) or `~/.zshrc` (Zsh), then open a new terminal:

```sh
[ ! -r "$HOME/.config/omarchy/themes/tibeb/greeting.sh" ] || . "$HOME/.config/omarchy/themes/tibeb/greeting.sh"
```

It displays “Ancient patterns. Modern pixels. Made in Ethiopia by Daniel G.”
without replacing your shell, prompt, or terminal configuration. Remove the line
to disable the greeting. Fish users can run
`sh ~/.config/omarchy/themes/tibeb/greeting.sh` from their interactive startup block.

### What is portable

| Feature | Omarchy installation |
| --- | --- |
| Charcoal, gold, and ivory application palette | Native `colors.toml` templates |
| Tibeb highlands wallpaper | Native theme wallpaper |
| Simplified Ethiopian folder icons | Installed SVG icon theme |
| Coffee battery icon assets | Available to apps using standard icon names |
| Terminal greeting | Optional startup line above |
| Live coffee fill, exact 15% warning, clock accent, woven lock-screen overlay | **GNOME-only extension; not installed on Omarchy** |

Omarchy's panel and lock screen use a different runtime. The GNOME extension is
not a Hyprland plugin; this installer does not pretend to enable it, replace the
panel, or overwrite your lock-screen configuration. Omarchy applies its native
clock and lock-screen styling from the palette where supported. A live coffee
widget would require a separate integration with your version's panel.

### Install by theme URL (palette and wallpaper only)

Once these changes are pushed to GitHub, Omarchy can install the base theme with:

```bash
omarchy-theme-install https://github.com/dan-seng/tibeb-theme.git
```

Omarchy clones the repository but does **not** run `install.sh`. This route uses
the repository's Yaru-olive preference and does not install the custom icons or
greeting helper. Use the local installer above for those additions. The local
installer can also be run from the URL-installed checkout:

```bash
bash ~/.config/omarchy/themes/tibeb/install.sh --apply
```

That converts the checkout to an installed asset directory and saves the original
checkout in the printed backup location. Keep a separate clone for development.

## Palette

| Role | Color |
| --- | --- |
| Volcanic Night / Background | `#141A1A` |
| Aksum Gold / Accent | `#E4B96F` |
| Cotton Ivory / Text | `#E9E2D3` |
| Highland Sage / Green | `#92B697` |
| Lake Tana / Cyan | `#7AB6B0` |
| Terracotta / Error | `#D27869` |
| Clay / Orange | `#D99666` |
| Mist / Blue | `#85A9C4` |

## Design rationale

1. **Culture in the geometry, not clichés:** Ethiopian woven textile patterns are referenced in the wallpaper's right-side border and the preview ornament.
2. **Readable for actual work:** A neutral near-black background keeps code and editor panes calm, while ivory provides text contrast.
3. **Distinctive at a glance:** A single amber-gold focus color repeats across window accents, selection, and key brand elements.
4. **Consistent across the OS:** Omarchy auto-generates application palettes using `colors.toml`, reducing bespoke maintenance.
5. **Wallpaper designed for tiled windows:** Large negative space on the left and the visual focal point on the right accommodates real workspaces.

## Competition submission blurb

**TIBEB (ጥበብ)** combines Ethiopian textile geometry, layered highland landscapes, volcanic-dark surfaces, and warm metallic gold into a restrained, developer-friendly Omarchy experience. Its design makes heritage present in shape, rhythm, and texture—not only color—while preserving the speed and clarity of modern Linux desktops.

## Notes

- The artwork was generated with AI assistance and composed specifically for this theme. **Check the contest rules before submission** if AI-assisted visuals are restricted.
- The validator checks TOML syntax, required palette colors, the icon preference, and PNG chunk checksums and compressed data. The theme **has not been run on a live Omarchy installation** in this environment.
- The UI in the preview is conceptual; the actual application and terminal arrangements are up to you.
- The theme assets may be adapted by you for your project or contest entry. Review any applicable contest attribution rules.

Theme reference: [Omarchy theme installation](https://github.com/basecamp/omarchy/blob/master/bin/omarchy-theme-install).

## Validate and troubleshoot

```bash
python3 scripts/validate.py
python3 scripts/test_install.py
```

If the installer reports that Omarchy is missing, run it on your Omarchy desktop.
It does not install Omarchy itself. If Omarchy is present but colors do not apply,
update Omarchy to a version supporting the current semantic palette, then run
`omarchy-theme-set tibeb` again. Restart an application if it retains its old colors.

If the wallpaper is missing, confirm that
`~/.config/omarchy/themes/tibeb/backgrounds/tibeb-highlands.png` exists and reapply
the theme. The preview is a concept image, not an additional wallpaper.

To return to your previous desktop theme, select it in Style > Theme. To restore
an older Tibeb installation, move the current `tibeb` folder aside and move the
backed-up `tibeb` folder printed by the installer into `~/.config/omarchy/themes/`,
then reapply it.

To restore an earlier icon layer, move `~/.local/share/icons/Tibeb-Omarchy` aside
and put the saved `Tibeb-Omarchy` directory printed by the installer back there.
Select another theme before removing Tibeb entirely. The optional greeting is
disabled by removing its startup line. Remove custom folder metadata with
`gio set -t unset ~/Code metadata::custom-icon-name` (repeat for other folders).
