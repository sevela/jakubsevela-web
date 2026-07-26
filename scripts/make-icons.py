#!/usr/bin/env python3
"""
Monogramové favicony pro tři weby brandu.

Písmena se berou přímo z obrysů Space Grotesku (favicon nemá k dispozici
webfont, takže se glyfy převádějí na cesty). Tečka se NEsází jako glyf —
Space Grotesk ji kreslí jako zaoblený čtvereček. Kreslí se jako plný kruh
v přesné geometrii sazby, kterou dávají metriky fontu:

  řez 700, velikost 125 % → bbox tečky je 190 × 190 jednotek se středem
  (149, 81), advance 298. Po přeškálování na 125 %:
      poloměr        = 190 * 1.25 / 2  = 118.75 j.
      střed nad účařím = 81 * 1.25      = 101.25 j.
      střed od pera   = 149 * 1.25      = 186.25 j.
      advance         = 298 * 1.25      = 372.50 j.
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity

FONTS = 'fonts/brand/'
UPEM = 1000.0

# geometrie tečky (viz docstring)
DOT_R       = 190 * 1.25 / 2
DOT_CY      = 81 * 1.25
DOT_DX      = 149 * 1.25
DOT_ADVANCE = 298 * 1.25

_cache = {}
def font(path):
    if path not in _cache:
        _cache[path] = TTFont(FONTS + path)
    return _cache[path]

LATIN = 'space-grotesk-latin-500-normal.woff2'
EXT   = 'space-grotesk-latin-ext-500-normal.woff2'

def glyph(char):
    """Vrátí (jméno glyfu, TTFont) pro znak — hledá v latin i latin-ext subsetu."""
    for p in (LATIN, EXT):
        f = font(p)
        name = f.getBestCmap().get(ord(char))
        if name:
            return name, f
    raise KeyError(char)

def layout(chars):
    """
    Poskládá monogram. `chars` je string, kde '.' znamená kreslenou tečku.
    Vrací (list cest, list kruhů, ink bbox).
    """
    paths, circles = [], []
    x = 0.0
    for ch in chars:
        if ch == '.':
            circles.append((x + DOT_DX, DOT_CY, DOT_R))
            x += DOT_ADVANCE
            continue
        name, f = glyph(ch)
        gs = f.getGlyphSet()
        pen = SVGPathPen(gs)
        # y se překlápí až v transformu celé skupiny, tady jen posun v x
        gs[name].draw(TransformPen(pen, Identity.translate(x, 0)))
        paths.append(pen.getCommands())
        x += f['hmtx'][name][0]

    # ink bbox přes glyfy i kruhy
    xs, ys = [], []
    x = 0.0
    for ch in chars:
        if ch == '.':
            xs += [x + DOT_DX - DOT_R, x + DOT_DX + DOT_R]
            ys += [DOT_CY - DOT_R, DOT_CY + DOT_R]
            x += DOT_ADVANCE
            continue
        name, f = glyph(ch)
        gs = f.getGlyphSet()
        bp = BoundsPen(gs); gs[name].draw(bp)
        x0, y0, x1, y1 = bp.bounds
        xs += [x + x0, x + x1]; ys += [y0, y1]
        x += f['hmtx'][name][0]
    return paths, circles, (min(xs), min(ys), max(xs), max(ys))


def icon_svg(chars, accent, size=512, bg='#16161a', fg='#e8e6e3',
             max_w=0.70, max_h=0.62, radius=0.225):
    paths, circles, (x0, y0, x1, y1) = layout(chars)
    ink_w, ink_h = x1 - x0, y1 - y0
    s = min(size * max_w / ink_w, size * max_h / ink_h)

    # ink na střed dlaždice; y se překlápí (font roste nahoru, SVG dolů)
    tx = size / 2 - (x0 + ink_w / 2) * s
    ty = size / 2 + (y0 + ink_h / 2) * s

    body = [f'<g transform="translate({tx:.3f},{ty:.3f}) scale({s:.5f},{-s:.5f})" fill="{fg}">']
    for d in paths:
        body.append(f'<path d="{d}"/>')
    body.append('</g>')
    for cx, cy, r in circles:
        body.append(f'<circle cx="{tx + cx * s:.3f}" cy="{ty - cy * s:.3f}" '
                    f'r="{r * s:.3f}" fill="{accent}"/>')

    rx = round(size * radius, 2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}">\n'
            f'  <rect width="{size}" height="{size}" rx="{rx}" fill="{bg}"/>\n  '
            + '\n  '.join(body) + '\n</svg>\n')


BRANDS = {
    # tři glyfy potřebují víc šířky, jinak by monogram v dlaždici zdrobněl
    'jakubsevela': dict(chars='j.š', accent='#dfa63e', max_w=0.80),
    'ethel':       dict(chars='e.',  accent='#56a8e8'),
    'feedco':      dict(chars='f.',  accent='#9ed455'),
}

if __name__ == '__main__':
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/icons'
    os.makedirs(out, exist_ok=True)
    for name, cfg in BRANDS.items():
        kw = {k: v for k, v in cfg.items() if k not in ('chars', 'accent')}
        open(f'{out}/{name}.svg', 'w', encoding='utf-8').write(
            icon_svg(cfg['chars'], cfg['accent'], **kw))
        # apple-touch: iOS si rohy zaobluje sám, dlaždice musí být plná
        open(f'{out}/{name}-apple.svg', 'w', encoding='utf-8').write(
            icon_svg(cfg['chars'], cfg['accent'], radius=0, **kw))
        print(name, 'ok')
