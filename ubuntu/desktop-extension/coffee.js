import St from 'gi://St';
import UPower from 'gi://UPowerGlib';

// Draw directly into the actor: no themed-icon fallback or image cache.
export function attachCoffee(icon, proxy, label) {
    const size = icon.icon_size > 0 ? icon.icon_size : 20;
    const area = new St.DrawingArea({width: size, height: size, reactive: false,
        x_align: icon.x_align, y_align: icon.y_align});
    const parent = icon.get_parent();
    parent.insert_child_below(area, icon);
    const originalVisible = icon.visible;
    icon.hide();
    let lastReported = null;
    area.connect('repaint', () => {
        const cr = area.get_context();
        const [width, height] = area.get_surface_size();
        cr.scale(width / 24, height / 24);
        const level = Math.max(0, Math.min(100, Number(proxy.Percentage) || 0));
        const cup = () => {
            cr.moveTo(3, 3); cr.lineTo(21, 3); cr.lineTo(18, 19);
            cr.curveTo(17.5, 22, 16, 22, 14, 22); cr.lineTo(10, 22);
            cr.curveTo(8, 22, 6.5, 22, 6, 19); cr.closePath();
        };
        cr.save();
        cup(); cr.clip();
        if (level < 15) cr.setSourceRGB(.875, .404, .357);
        else cr.setSourceRGB(.835, .675, .259);
        const fillHeight = 17 * level / 100;
        cr.rectangle(4, 21 - fillHeight, 16, fillHeight); cr.fill();
        cr.restore();
        cup(); cr.setSourceRGB(.933, .898, .796); cr.setLineWidth(1.7); cr.stroke();
        if (proxy.State === UPower.DeviceState.CHARGING) {
            cr.moveTo(14, 5); cr.lineTo(7, 13); cr.lineTo(12, 13);
            cr.lineTo(10, 20); cr.lineTo(18, 10); cr.lineTo(13, 10); cr.closePath();
            cr.setSourceRGB(1, .957, .831); cr.fillPreserve();
            cr.setSourceRGB(.078, .102, .102); cr.setLineWidth(1); cr.stroke();
        }
        cr.$dispose();
        if (lastReported !== level) {
            console.log(`Tibeb coffee ${label}: painted ${level}% at ${width}x${height}`);
            lastReported = level;
        }
    });
    const update = () => {
        area.visible = Boolean(proxy.IsPresent);
        if (proxy.IsPresent) icon.hide();
        else icon.visible = originalVisible;
        area.queue_repaint();
    };
    const signal = proxy.connect('g-properties-changed', update);
    update();
    return () => {
        proxy.disconnect(signal);
        area.destroy();
        icon.visible = originalVisible;
    };
}
