import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Meta from 'gi://Meta';
import St from 'gi://St';
import Shell from 'gi://Shell';
import GDesktopEnums from 'gi://GDesktopEnums';
import {Extension, InjectionManager} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import {UnlockDialog} from 'resource:///org/gnome/shell/ui/unlockDialog.js';
import {attachCoffee} from './coffee.js';

export default class TibebDesktop extends Extension {
    enable() {
        this._injections = new InjectionManager();
        this._coffeeCleanup = [];
        // GNOME 50 builds Quick Settings asynchronously after network imports.
        // Extensions can be enabled before its system indicator is present.
        if (!this._attachBattery()) {
            let attempts = 0;
            this._batteryWait = GLib.timeout_add(GLib.PRIORITY_DEFAULT, 250, () => {
                if (this._attachBattery()) {
                    this._batteryWait = null;
                    return GLib.SOURCE_REMOVE;
                }
                if (++attempts >= 120) {
                    console.error('Tibeb: battery widget unavailable after 30 seconds');
                    this._batteryWait = null;
                    return GLib.SOURCE_REMOVE;
                }
                return GLib.SOURCE_CONTINUE;
            });
        }
        const directory = this.path;
        this._injections.overrideMethod(UnlockDialog.prototype, '_createBackground', () => function (monitorIndex) {
            const monitor = Main.layoutManager.monitors[monitorIndex];
            const widget = new St.Widget({
                x: monitor.x, y: monitor.y, width: monitor.width, height: monitor.height,
                style_class: 'screen-shield-background',
                effect: new Shell.BlurEffect({name: 'blur'}),
            });
            const background = new Meta.Background({meta_display: global.display});
            background.set_file(Gio.File.new_for_path(`${directory}/wallpaper.png`), GDesktopEnums.BackgroundStyle.ZOOM);
            const actor = new Meta.BackgroundActor({meta_display: global.display, monitor: monitorIndex});
            actor.content.background = background;
            actor.set_size(monitor.width, monitor.height);
            widget.add_child(actor);
            this._backgroundGroup.add_child(widget);
            // A separate non-reactive layer keeps the woven edge sharp above the blur.
            this._backgroundGroup.add_child(new St.Widget({
                x: monitor.x, y: monitor.y, width: monitor.width, height: monitor.height,
                reactive: false,
                style: `background-image: url("${directory}/border.svg"); background-size: 100% 100%;`,
            }));
        });
        Main.screenShield._dialog?._updateBackgrounds();
    }

    _attachBattery() {
        const system = Main.panel.statusArea.quickSettings?._system;
        const power = system?._systemItem?.powerToggle;
        if (!power?._proxy || !power._icon?.get_parent() || !system._indicator?.get_parent())
            return false;
        this._power = power;
        try {
            this._coffeeCleanup.push(attachCoffee(system._indicator, power._proxy, 'panel'));
            this._coffeeCleanup.push(attachCoffee(power._icon, power._proxy, 'menu'));
        } catch (error) {
            for (const cleanup of this._coffeeCleanup)
                cleanup();
            this._coffeeCleanup = [];
            throw error;
        }
        console.log('Tibeb: attached live battery renderer');
        return true;
    }

    disable() {
        if (this._batteryWait) {
            GLib.source_remove(this._batteryWait);
            this._batteryWait = null;
        }
        for (const cleanup of this._coffeeCleanup ?? [])
            cleanup();
        this._coffeeCleanup = [];
        this._power?._sync();
        this._power = null;
        this._injections?.clear();
        this._injections = null;
        Main.screenShield._dialog?._updateBackgrounds();
    }
}
