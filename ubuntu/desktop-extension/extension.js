import Gio from 'gi://Gio';
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
        this._power = Main.panel.statusArea.quickSettings?._system?._systemItem?.powerToggle;
        this._coffeeCleanup = [];
        if (!this._power?._proxy)
            throw new Error('Tibeb: GNOME battery widget was not found');
        const panelIcon = Main.panel.statusArea.quickSettings._system._indicator;
        this._coffeeCleanup.push(attachCoffee(panelIcon, this._power._proxy, 'panel'));
        this._coffeeCleanup.push(attachCoffee(this._power._icon, this._power._proxy, 'menu'));
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

    disable() {
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
