import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
let source = readFileSync(new URL('./desktop-extension/coffee.js', import.meta.url), 'utf8');
source = source.replace(/^import .*;\n/gm, '');
const rectangles = [];
const colors = [];
let repaint, update, disconnected = false, destroyed = false;
const cr = new Proxy({}, {get: (_, name) => (...args) => {
    if (name === 'rectangle') rectangles.push(args);
    if (name === 'setSourceRGB') colors.push(args);
}});
globalThis.St = {DrawingArea: class {
    connect(_name, callback) { repaint = callback; }
    get_context() { return cr; }
    get_surface_size() { return [20, 20]; }
    queue_repaint() { repaint(); }
    destroy() { destroyed = true; }
}};
globalThis.UPower = {DeviceState: {CHARGING: 1}};
const {attachCoffee} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const icon = {icon_size: 20, visible: true, hide() {this.visible = false;},
    get_parent() {return {insert_child_below() {}};}};
const proxy = {Percentage: 60, IsPresent: true, State: 2,
    connect(_signal, callback) { update = callback; return 1; },
    disconnect(id) { assert.equal(id, 1); disconnected = true; }};
const cleanup = attachCoffee(icon, proxy, 'test');
assert.equal(icon.visible, false);
assert.equal(rectangles.at(-1)[3], 10.2);
proxy.Percentage = 55; update();
assert.ok(Math.abs(rectangles.at(-1)[3] - 9.35) < 1e-10);
proxy.Percentage = 14; update();
assert.ok(colors.some(c => c[0] === .875));
proxy.IsPresent = false; update();
assert.equal(icon.visible, true);
cleanup();
assert.ok(disconnected && destroyed);
assert.equal(icon.visible, true);
console.log('Live proxy update, fill geometry, low color, and cleanup passed.');
