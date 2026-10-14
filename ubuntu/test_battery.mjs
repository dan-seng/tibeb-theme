import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source = readFileSync(new URL('./desktop-extension/battery.js', import.meta.url));
const {batterySvg} = await import(`data:text/javascript;base64,${source.toString('base64')}`);
assert.match(batterySvg(14.99, false), /fill="#df675b"/);
assert.match(batterySvg(15, false), /fill="#d5ac42"/);
assert.match(batterySvg(100, true), /m14 5-7 8/);
assert.doesNotMatch(batterySvg(40, false), /m14 5-7 8/);
assert.match(batterySvg(-10, false), /height="0"/);
assert.match(batterySvg(110, false), /height="15"/);
console.log('Battery boundary, clamping, and charging tests passed.');

// Every percentage decrease lowers the liquid surface, even within a 10% bucket.
const geometry = level => {
    const match = batterySvg(level, false).match(/<rect x="5" y="([^"]+)" width="14" height="([^"]+)"/);
    return {y: Number(match[1]), height: Number(match[2])};
};
for (let level = 100; level > 0; level--) {
    const before = geometry(level);
    const after = geometry(level - 1);
    assert.ok(after.y > before.y);
    assert.ok(after.height < before.height);
}
console.log('Coffee fill decreases at every percentage step.');
