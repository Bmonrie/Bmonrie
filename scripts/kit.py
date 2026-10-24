"""Piezas comunes de las láminas: paleta, tipografía embebida, medida de texto, animación y envoltorio SVG.

Una sola familia, Archivo (variable en peso y anchura, la del perfil del trabajo), recortada a los
caracteres que se usan.
Los pocos glifos japoneses de la maqueta de Kakurega salen de un recorte de Noto Sans JP.
"""
import base64
import io
import re
import string
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "fonts"

# ─── Paleta: la del perfil del trabajo. Índigo de tinta, un azul que marca lo que importa ──
PAPER, INK, BLUE = "#FFFFFF", "#171C8F", "#0072CE"
STONE = "#E7F3F5"  # página de tono: un escalón, nunca una línea
PALE = "#C9DFF2"  # azul claro: subrayados, casillas, caras de los dibujos
NOVA = "#4AA7B7"  # segundo acento, solo donde el azul no se leería
MUTED = "#475569"  # texto secundario sobre papel o tono
ON_INK, ON_INK_SOFT = "#FFFFFF", "#A9AEDB"  # texto sobre el campo índigo
ON_BLUE_SOFT = "#D6E9F8"  # texto secundario sobre el campo azul
W = 1000  # ancho de lámina de escritorio
M = 48  # margen de escritorio
PW, PM = 400, 20  # ancho y margen de las láminas de teléfono

_FONT = FONTS / "archivo.woff2"
_JP = FONTS / "notosansjp-sub.ttf"


def _woff2(path, text=None):
    font = TTFont(path)
    if text is not None:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "tnum", "case"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


_css = None


def set_charset(chars):
    """Recorta la fuente a los caracteres de todas las láminas. Se llama una vez, antes de pintar."""
    global _css
    _css = (
        "@font-face{font-family:'A';src:url(data:font/woff2;base64,%s) format('woff2');"
        "font-weight:100 900;font-stretch:62%% 125%%}"
        "@font-face{font-family:'J';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:100 900}"
        % (_woff2(_FONT, chars + string.printable + "·×—–’“”«»"), _woff2(_JP))
    )


BASE_CSS = (
    "text{font-family:'A','Helvetica Neue',Arial,sans-serif;font-kerning:normal}"
    ".j{font-family:'J',sans-serif}"
    ".n{font-variant-numeric:tabular-nums}"
    # Movimiento: el flujo de las flechas, un pulso, un cursor, un giro y el crecer de una barra
    ".flow{stroke-dasharray:5 11;animation:flow 1.1s linear infinite}"
    "@keyframes flow{to{stroke-dashoffset:-16}}"
    ".pulse{animation:pulse 2.4s ease-in-out infinite}"
    "@keyframes pulse{50%{opacity:.3}}"
    ".blink{animation:blink 1.1s steps(1) infinite}"
    "@keyframes blink{50%{opacity:0}}"
    ".spin{transform-box:view-box;animation:spin 8s linear infinite}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    ".grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.1s cubic-bezier(.16,1,.3,1) backwards}"
    "@keyframes grow{from{transform:scaleY(0)}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}.packet{display:none}}"
)

_metrics = {}


def width(s, size, wght=400, wdth=100, track=0.0):
    key = (wght, wdth)
    if key not in _metrics:
        f = instantiateVariableFont(TTFont(_FONT), {"wght": wght, "wdth": wdth})
        _metrics[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upm = _metrics[key]
    units = sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in s)
    return units * size / upm + len(s) * track * size


def wrap(s, size, maxw, wght=400, wdth=100, track=0.0):
    lines, cur = [], ""
    for word in s.split(" "):
        if not word:
            continue
        test = f"{cur} {word}".strip(" ")
        if cur and width(test, size, wght, wdth, track) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = test
    return lines + [cur] if cur else lines


def fit(s, maxw, sizes, wght, wdth, track, max_lines=2):
    """El tamaño más grande de `sizes` con el que `s` cabe en `max_lines` líneas."""
    for size in sizes:
        lines = wrap(s, size, maxw, wght, wdth, track * 1.0)
        if len(lines) <= max_lines:
            return size, lines
    return sizes[-1], wrap(s, sizes[-1], maxw, wght, wdth, track)


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def text(x, y, s, size, fill=INK, wght=400, wdth=100, anchor="start", track=0.0, cls="", raw=False, halo=None):
    style = f' style="font-stretch:{wdth}%"' if wdth != 100 else ""
    if halo:  # recorta las líneas del dibujo que pasan por detrás del rótulo
        style += f' paint-order="stroke" stroke="{halo}" stroke-width="6" stroke-linejoin="round"'.replace('"', '"')
    ls = f' letter-spacing="{track * size:.2f}"' if track else ""
    c = f' class="{cls}"' if cls else ""
    body = s if raw else esc(s)
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{wght}" fill="{fill}" '
            f'text-anchor="{anchor}"{style}{ls}{c}>{body}</text>')


def block(x, y, s, size, maxw, fill=INK, wght=400, wdth=100, lead=1.4, track=0.0):
    """Párrafo con saltos de línea; devuelve el SVG y la y de la línea siguiente."""
    out = []
    for ln in wrap(s, size, maxw, wght, wdth, track):
        out.append(text(x, y, ln, size, fill, wght, wdth, track=track))
        y += size * lead
    return "".join(out), y


def rich(x, y, s, size, maxw, fill=INK, bold_fill=None, lead=1.45, wght=400, bold=700):
    """Párrafo con tramos **en negrita**. Devuelve el SVG y la y siguiente."""
    bold_fill = bold_fill or fill
    words = []  # (palabra, negrita, pegada a la anterior)
    for i, part in enumerate(re.split(r"\*\*", s)):
        for k, w in enumerate(x for x in part.split(" ") if x):
            words.append((w, i % 2 == 1, k == 0 and i > 0 and part[:1] not in ("", " ")))
    lines, cw = [[]], 0.0
    sp = width(" ", size, wght)
    for w, b, glue in words:
        ww = width(w, size, bold if b else wght)
        gap = 0 if (glue or not lines[-1]) else sp
        if lines[-1] and not glue and cw + gap + ww > maxw:
            lines.append([])
            cw, gap = 0.0, 0
        cw += gap + ww
        lines[-1].append((w, b, glue))
    out = []
    for ln in lines:
        spans = "".join(
            f'<tspan font-weight="{bold if b else wght}" fill="{bold_fill if b else fill}">'
            f'{"" if (i == 0 or glue) else " "}{esc(w)}</tspan>'
            for i, (w, b, glue) in enumerate(ln))
        out.append(text(x, y, spans, size, fill, wght, raw=True).replace("<text ", '<text xml:space="preserve" ', 1))
        y += size * lead
    return "".join(out), y


def flow(x1, y1, x2, y2, color=PAPER, sw=2.2):
    """Trazo animado encima de una flecha: el sentido del flujo, en movimiento."""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="butt" class="flow"/>')


def svg(h, body, title, fill=PAPER, w=W):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<defs><style>{_css}{BASE_CSS}</style></defs>'
            f'<rect width="{w}" height="{h:.0f}" fill="{fill}"/>{body}</svg>')
