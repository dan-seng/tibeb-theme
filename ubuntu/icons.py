"""Small native SVG icons for Tibeb; no network icon overrides."""

NAME = 'Tibeb-Icons'
INK = '#eee5cb'
GOLD = '#d5ac42'


def svg(body, size=64):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{body}</svg>\n'


# The approved preview uses broad folder silhouettes and substantial pictograms.
# Motifs use currentColor so symbolic variants retain GNOME's recoloring.
MOTIFS = {
    'folder': '',
    'user-home': '<path fill="currentColor" stroke="none" d="M16 37 32 22 48 37zM20 39h24v14h-8v-6a4 4 0 0 0-8 0v6h-8z"/><circle fill="currentColor" stroke="none" cx="32" cy="23" r="1.6"/>',
    'folder-documents': '<path fill="currentColor" fill-rule="evenodd" stroke="none" d="M23 24h19q5 0 5 5v18q0 5-5 5H23q-6 0-6-6V30q0-6 6-6zm0 3q-3 0-3 3v13q3-2 6 0V30q0-3-3-3zm8 5v2h11v-2zm0 7v2h11v-2zm-8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/>',
    'folder-download': '<path fill="currentColor" stroke="none" d="m28 23 7 3-1 4-4-1-2 7q11 8 5 15-7 7-16 0-7-7 2-14l6-4 3-7z"/><path d="M31 32q9-5 10 2l-1 7"/><path fill="currentColor" stroke="none" d="M45 41h5v7h5l-7.5 7-7.5-7h5z"/>',
    'folder-pictures': '<path d="M17 26h30v26H17z"/><path fill="currentColor" stroke="none" d="m18 50 10-12 7 8 5-6 6 10z"/><circle fill="currentColor" stroke="none" cx="37" cy="33" r="3"/>',
    'folder-music': '<g transform="rotate(-35 32 39)"><ellipse cx="32" cy="27" rx="10" ry="4"/><path d="M22 27v22q10 8 20 0V27M23 30l18 18M23 47l17-16M23 32l3 18m13-18-2 19"/></g>',
    'folder-videos': '<path fill="currentColor" stroke="none" d="M25 27q-2-1-2 2v22q0 3 2 2l20-12q2-1 0-3z"/>',
    'folder-projects': '<path d="m26 53 2-28 4-4 4 4 2 28M22 53h20M28 31h8m-9 7h10m-10 7h10"/>',
    'folder-code': '<path stroke-width="4" d="m24 31-9 9 9 9m16-18 9 9-9 9m-5-23-6 28"/>',
    'user-desktop': '<path d="m13 52 15-17 10 11 5-6 10 12"/><circle fill="currentColor" stroke="none" cx="42" cy="29" r="4"/>',
    'folder-archive': '<path d="M17 37q-2 17 15 17t15-17l-15-8zM28 29v-3q0-4 4-4t4 4v3M18 38q14 6 28 0M19 44q13 5 26 0M23 50h18"/>',
    'folder-templates': '<path d="m32 25 13 14-13 14-13-14zM32 32l7 7-7 7-7-7z"/>',
    'folder-publicshare': '<circle fill="currentColor" stroke="none" cx="24" cy="31" r="4"/><circle fill="currentColor" stroke="none" cx="41" cy="31" r="4"/><path stroke-width="4" d="M15 51a9 9 0 0 1 18 0m0 0a9 9 0 0 1 18 0"/>',
    'folder-favorites': '<path d="M32 53 19 39c-9-12 7-19 13-9 6-10 22-3 13 9z"/>',
    'folder-remote': '<path d="m23 47 9-19 11 19z"/><g fill="currentColor" stroke="none"><circle cx="32" cy="28" r="4.5"/><circle cx="23" cy="47" r="4.5"/><circle cx="43" cy="47" r="4.5"/></g>',
    'user-trash': '<path d="M19 30h26m-23 0 2 23h16l2-23M27 29v-5h10v5m-9 11v12m5-12v12m5-12v12"/>',
}


def folder(motif, symbolic=False):
    color = '#bebebe' if symbolic else INK
    outline = f'<g color="{color}" fill="none" stroke="{color}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 19v-7q0-4 4-4h13q2 0 3 2l5 5h28q5 0 5 5v33q0 4-5 4H7q-4 0-4-4V22q0-4 4-4h12"/>{motif}</g>'
    stripe = '' if symbolic else '<path d="M7 12h3" stroke="#23945c" stroke-width="1.8"/><path d="M11 12h3" stroke="#edcb38" stroke-width="1.8"/><path d="M15 12h3" stroke="#d44c42" stroke-width="1.8"/>'
    return svg(outline + stripe)


def battery(level, charging=False, symbolic=False, missing=False):
    color = '#bebebe' if symbolic else INK
    fill = color if symbolic else (GOLD if level > 10 else '#d27869')
    body = f'<defs><clipPath id="cup"><path d="M5 5h14l-2 13q-.3 2-3 2h-4q-2.7 0-3-2z"/></clipPath></defs>'
    if level:
        height = 15 * level / 100
        body += f'<rect x="5" y="{20-height:g}" width="14" height="{height:g}" fill="{fill}" clip-path="url(#cup)"/>'
    body += f'<path d="M3 3h18l-3 16q-.5 3-4 3h-4q-3.5 0-4-3z" fill="none" stroke="{color}" stroke-width="1.7" stroke-linejoin="round"/>'
    if not symbolic:
        for x, c in [(5, '#23945c'), (10, '#edcb38'), (15, '#d44c42')]:
            body += f'<path d="M{x} 3h5" stroke="{c}" stroke-width="2"/>'
    if charging:
        body += f'<path d="m14 6-6 7h4l-2 6 7-8h-4z" fill="{color}" stroke="#141a1a" stroke-width=".7"/>'
    if missing:
        body += f'<path d="M10 9a2 2 0 1 1 3 2v3m0 2v1" fill="none" stroke="{color}" stroke-width="1.7"/>'
    return svg(body, 24)


def assets(parent='Yaru-olive'):
    if parent == NAME:
        parent = 'Yaru-olive'
    files = {}
    aliases = {'folder-open':'folder', 'folder-drag-accept':'folder', 'folder-visiting':'folder',
               'folder-downloads':'folder-download', 'folder-desktop':'user-desktop',
               'folder-home':'user-home', 'folder-shared':'folder-publicshare',
               'folder-saved-search':'folder-documents', 'user-trash-full':'user-trash'}
    for name, motif in {**MOTIFS, **{a:MOTIFS[b] for a,b in aliases.items()}}.items():
        for symbolic in (False, True):
            suffix = '-symbolic' if symbolic else ''
            files[f'scalable/places/{name}{suffix}.svg'] = folder(motif, symbolic)
    for level in range(0, 101, 10):
        for state in ('', '-charging', '-plugged-in'):
            for symbolic in (False, True):
                suffix = '-symbolic' if symbolic else ''
                files[f'scalable/status/battery-level-{level}{state}{suffix}.svg'] = battery(level, bool(state), symbolic)
    for name, level, charging, missing in [
        ('battery',100,False,False), ('battery-full',100,False,False),
        ('battery-good',70,False,False), ('battery-low',30,False,False),
        ('battery-caution',10,False,False), ('battery-empty',0,False,False),
        ('battery-action',0,False,False), ('battery-missing',0,False,True),
        ('battery-full-charged',100,True,False), ('battery-level-100-charged',100,True,False)]:
        for symbolic in (False, True):
            suffix = '-symbolic' if symbolic else ''
            files[f'scalable/status/{name}{suffix}.svg'] = battery(level,charging,symbolic,missing)
    files['index.theme'] = f'''[Icon Theme]
Name={NAME}
Comment=Simple Ethiopian folders and coffee battery icons
Inherits={parent}
Directories=scalable/places,scalable/status

[scalable/places]
Size=64
MinSize=16
MaxSize=512
Type=Scalable
Context=Places

[scalable/status]
Size=24
MinSize=16
MaxSize=128
Type=Scalable
Context=Status
'''
    return {f'.local/share/icons/{NAME}/{key}': value for key,value in files.items()}
