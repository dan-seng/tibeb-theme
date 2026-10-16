import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source = readFileSync(new URL('./desktop-extension/extension.js', import.meta.url), 'utf8')
    .replace(/^import .*;\n/gm, '');
let tick, attached = 0, cleaned = 0, cancelled = false;
globalThis.Extension = class {path = '/tmp/tibeb-test';};
globalThis.InjectionManager = class {overrideMethod() {} clear() {}};
globalThis.UnlockDialog = class {};
globalThis.GLib = {PRIORITY_DEFAULT: 0, SOURCE_REMOVE: false, SOURCE_CONTINUE: true,
    timeout_add(priority, milliseconds, callback) {assert.equal(milliseconds, 250); tick = callback; return 42;},
    source_remove(id) {assert.equal(id, 42); cancelled = true;}};
globalThis.Main = {panel: {statusArea: {quickSettings: {}}}, screenShield: {}};
globalThis.attachCoffee = () => {attached++; return () => cleaned++;};
const {default: Desktop} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const extension = new Desktop();
extension.enable();
assert.equal(attached, 0);
assert.equal(tick(), true);
const icon = {get_parent() {return {};}};
Main.panel.statusArea.quickSettings._system = {_indicator: icon,
    _systemItem: {powerToggle: {_proxy: {}, _icon: icon, _sync() {}}}};
assert.equal(tick(), false);
assert.equal(attached, 2);
extension.disable();
assert.equal(cleaned, 2);
delete Main.panel.statusArea.quickSettings._system;
extension.enable();
extension.disable();
assert.ok(cancelled);
console.log('Delayed GNOME initialization and pending timer cancellation passed.');
