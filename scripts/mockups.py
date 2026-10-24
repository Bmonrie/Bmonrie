"""Maquetas de cada producto, redibujadas en plano (no son capturas), a 360 de ancho: lo que cabe en la
pantalla de un teléfono. La tarjeta de cada proyecto las muestra dentro de un marco de dispositivo.

Bordes finos y claros, como los diagramas; el índigo solo para barras y fondos de la propia app. Toda letra
que se lee mide 18 px o más; el relleno se dibuja como barra.
"""
import math

from kit import BLUE, INK, MUTED, NOVA, ON_INK, ON_INK_SOFT, PALE, PAPER, STONE, esc, text, width, wrap

EDGE = "#A9C4E4"  # borde fino, el mismo de las tarjetas de los diagramas
DEEP = "#10146B"  # el fondo de los Shorts: índigo profundo
MW = 360  # ancho de las maquetas

# Siluetas planas de piezas, base en (0, 0), alto 1
PIECES = {
    "rook": "M-0.30 0H0.30V-0.10H0.22L0.18 -0.62H0.26V-0.86H0.16V-0.76H0.06V-0.86H-0.06V-0.76H-0.16V-0.86H-0.26V-0.62H-0.18L-0.22 -0.10H-0.30Z",
    "king": "M-0.30 0H0.30V-0.10H0.20L0.24 -0.58Q0.24 -0.70 0.06 -0.72V-0.80H0.14V-0.88H0.06V-0.96H-0.06V-0.88H-0.14V-0.80H-0.06V-0.72Q-0.24 -0.70 -0.24 -0.58L-0.20 -0.10H-0.30Z",
    "pawn": "M-0.28 0H0.28V-0.10H0.17L0.11 -0.48A0.17 0.17 0 1 0 -0.11 -0.48L-0.17 -0.10H-0.28Z",
    "bishop": "M-0.28 0H0.28V-0.10H0.17L0.13 -0.52Q0.24 -0.66 0 -0.90Q-0.24 -0.66 -0.13 -0.52L-0.17 -0.10H-0.28Z",
    "queen": "M-0.30 0H0.30V-0.10H0.20L0.30 -0.74L0.12 -0.46L0.10 -0.86L0 -0.50L-0.10 -0.86L-0.12 -0.46L-0.30 -0.74L-0.20 -0.10H-0.30Z",
    "knight": "M-0.30 0H0.30V-0.10H0.22Q0.26 -0.50 0.16 -0.72Q0.04 -0.92 -0.14 -0.90L-0.18 -0.98L-0.24 -0.84Q-0.34 -0.72 -0.30 -0.58L-0.20 -0.52Q-0.10 -0.60 -0.02 -0.56Q-0.20 -0.36 -0.20 -0.10H-0.30Z",
}


def _rect(x, y, w, h, fill, sw=1.5, stroke=EDGE, rx=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if sw else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{st}{r}{extra}/>'


def browser(h, url, body):
    """La barra de dirección de un navegador de teléfono y el contenido debajo. Devuelve (svg, ancho, alto)."""
    bar = 54
    return (_rect(0, 0, MW, bar, STONE, 0) + _rect(16, 12, MW - 32, 30, PAPER, 1.2, EDGE, 15)
            + text(32, 33, url, 18, INK, 500) + f'<g transform="translate(0 {bar})">{body}</g>'), MW, h + bar


def jp(x, y, s, size, fill=INK, wght=400, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="j" font-size="{size}" font-weight="{wght}" fill="{fill}" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


def _piece(x, y, kind, size, fill):
    return (f'<path d="{PIECES[kind]}" transform="translate({x:.1f} {y:.1f}) scale({size:.1f})" fill="{fill}" '
            f'stroke="{INK}" stroke-width="{1.8 / size:.4f}" stroke-linejoin="round"/>')


def _arrow2d(x1, y1, x2, y2, fill, w=10, head=24):
    L_ = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L_, (y2 - y1) / L_
    nx, ny = -uy, ux
    qx, qy = x2 - ux * head, y2 - uy * head
    pts = [(x1 + nx * w / 2, y1 + ny * w / 2), (qx + nx * w / 2, qy + ny * w / 2), (qx + nx * head * 0.6, qy + ny * head * 0.6),
           (x2, y2), (qx - nx * head * 0.6, qy - ny * head * 0.6), (qx - nx * w / 2, qy - ny * w / 2),
           (x1 - nx * w / 2, y1 - ny * w / 2)]
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}"/>'


# ─── Kakurega: el lector con el diccionario emergente ────────────────────────
READING = "ある時この男が深い林の中を通りますと、小さな蜘蛛が一匹、路ばたを這って行くのが見えました。"


def kakurega(L):
    m = L["mock"]
    b = [_rect(0, 0, MW, 56, INK, 0), text(20, 37, "Kakurega", 22, ON_INK, 800)]
    for i in range(3):
        b.append(_rect(MW - 46, 18 + i * 8, 26, 3, ON_INK, 0))
    b.append(jp(20, 98, "蜘蛛の糸", 22, INK, 700))
    lines = [READING[i:i + 14] for i in range(0, len(READING), 14)]
    for i, ln in enumerate(lines):
        y = 146 + i * 42
        if "蜘蛛" in ln:
            k = ln.index("蜘蛛")
            b.append(_rect(20 + k * 22 - 3, y - 21, 2 * 22 + 6, 30, PALE, 0, rx=4))
        b.append(jp(20, y, ln, 22))
    # El diccionario emergente
    cx, cy, cw = 20, 146 + len(lines) * 42, MW - 40
    b += [_rect(cx, cy, cw, 360, PAPER, 1.5, EDGE, 10), jp(cx + 22, cy + 40, "くも", 20, MUTED), jp(cx + 22, cy + 92, "蜘蛛", 44, INK, 700)]
    tw = width(m["common"], 18, 600) + 24
    b.append(_rect(cx + 130, cy + 64, tw, 32, STONE, 0, rx=6) + text(cx + 142, cy + 86, m["common"], 18, INK, 600))
    b.append(text(cx + 22, cy + 132, m["noun"], 18, MUTED))
    b.append(text(cx + 22, cy + 162, m["meaning"], 24, INK, 700))
    b.append(text(cx + 22, cy + 198, m["add"], 19, BLUE, 700))
    b.append(f'<path d="M{cx} {cy + 222}H{cx + cw}V{cy + 350}Q{cx + cw} {cy + 360} {cx + cw - 10} {cy + 360}H{cx + 10}'
             f'Q{cx} {cy + 360} {cx} {cy + 350}Z" fill="{STONE}"/>')
    for i, (k, on) in enumerate((("蜘", "ち"), ("蛛", "ちゅ、しゅ"))):
        yy = cy + 238 + i * 60
        b.append(_rect(cx + 22, yy, 50, 50, PAPER, 1.2, EDGE, 8) + jp(cx + 47, yy + 36, k, 30, INK, 700, "middle"))
        b.append(text(cx + 88, yy + 22, m["spider"], 20, INK, 700))
        b.append(text(cx + 88, yy + 46, "On:", 18, MUTED) + jp(cx + 124, yy + 46, on, 18, MUTED))
    return browser(cy + 380, "kakuregalearn.com", "".join(b))


# ─── BlunderLing: un Short ───────────────────────────────────────────────────
# Una Escocesa tras 3...exd4 4.Nxd4: el caballo negro de f6 acaba de saltar a d5 (las dos casillas marcadas)
BLACK = [(0, 0, "rook"), (2, 0, "bishop"), (3, 0, "queen"), (4, 0, "king"), (5, 0, "bishop"), (7, 0, "rook"),
         (2, 2, "knight"), (3, 3, "knight")] + [(c, 1, "pawn") for c in (0, 1, 2, 3, 5, 6, 7)]
WHITE_ = [(0, 7, "rook"), (2, 7, "bishop"), (3, 7, "queen"), (4, 7, "king"), (7, 7, "rook"), (2, 5, "knight"),
          (3, 4, "knight"), (2, 4, "bishop"), (4, 4, "pawn")] + [(c, 6, "pawn") for c in (0, 1, 2, 5, 6, 7)]


def blunderling(L):
    """El Short en su teléfono: la frase, el tablero con la jugada marcada y el título real del vídeo."""
    m = L["mock"]
    pw, cell = 300, 30
    b = []
    hs = min(26, min(26 * (pw - 60) / width(ln, 26, 800) for ln in m["hook"]))
    for i, ln in enumerate(m["hook"]):
        b.append(text(pw / 2, 72 + i * (hs + 8), ln, round(hs, 1), ON_INK, 800, anchor="middle"))
    bx, by = (pw - 8 * cell) / 2, 72 + 2 * (hs + 8) + 14
    for r in range(8):
        for c in range(8):
            f = NOVA if (c, r) in {(3, 3), (5, 2)} else (PAPER if (r + c) % 2 == 0 else PALE)
            b.append(_rect(bx + c * cell, by + r * cell, cell, cell, f, 0))
    b.append(f'<g class="pulse">{_rect(bx + 3 * cell, by + 3 * cell, cell, cell, NOVA, 0)}</g>')
    for (c, r, kind, fill) in [(c, r, k, INK) for c, r, k in BLACK] + [(c, r, k, PAPER) for c, r, k in WHITE_]:
        b.append(_piece(bx + c * cell + cell / 2, by + r * cell + cell - 3, kind, cell * 0.95, fill))
    y = by + 8 * cell + 42
    b.append(text(30, y, "@BlunderLing", 19, ON_INK_SOFT, 600))
    y += 32
    for ln in wrap(m["title"], 19, pw - 60, 600)[:3]:
        b.append(text(30, y, ln, 19, ON_INK, 600))
        y += 26
    ph = y + 22  # el teléfono mide lo que su contenido
    body = _rect(0, 0, pw, ph, INK, 0, rx=40) + _rect(10, 10, pw - 20, ph - 20, DEEP, 0, rx=31) + "".join(b)
    return body, pw, ph


# ─── Template_Agents: el chat que trae la plantilla ──────────────────────────
def agents(L):
    m = L["mock"]
    x0, w = 20, MW - 40
    b = []
    qw = min(w - 30, width(m["question"], 19, 500) + 40)
    b.append(_rect(x0 + w - qw, 24, qw, 52, INK, 0, rx=12) + text(x0 + w - qw + 20, 57, m["question"], 19, ON_INK, 500))
    ty = 104
    lines = wrap(m["approval"], 19, w - 40, 600)
    ch = 150 + (len(lines) - 1) * 25
    b.append(_rect(x0, ty, w, ch, PAPER, 1.5, EDGE, 10))
    b.append(text(x0 + 20, ty + 38, "get_order_status", 21, INK, 700))
    b.append(text(x0 + 20, ty + 68, m["args"], 18, MUTED))
    for i, ln in enumerate(lines):
        b.append(text(x0 + 20, ty + 98 + i * 25, ln, 19, INK, 600))
    by = ty + 108 + (len(lines) - 1) * 25
    aw = width(m["approved"], 19, 700) + 40
    b.append(_rect(x0 + 20, by, aw, 34, BLUE, 0, rx=17) + text(x0 + 20 + aw / 2, by + 23, m["approved"], 19, PAPER, 700, anchor="middle"))
    b.append(text(x0 + 36 + aw, by + 23, m["by"], 18, MUTED))
    y = ty + ch + 40
    for ln in wrap(m["answer"], 21, w):
        b.append(text(x0, y, ln, 21, INK))
        y += 31
    cw = width(m["cite"], 18, 600) + 28
    b.append(_rect(x0, y - 6, cw, 34, STONE, 0, rx=6) + text(x0 + 14, y + 17, m["cite"], 18, INK, 600))
    hb = y + 70
    b.append(_rect(x0, hb, w, 50, PAPER, 1.5, EDGE, 25) + text(x0 + 30, hb + 32, m["input"], 19, MUTED))
    b.append(f'<g class="blink">{_rect(x0 + 18, hb + 12, 3, 26, BLUE, 0)}</g>')
    return browser(hb + 76, "localhost:3000", "".join(b))


# ─── WavesLing: el puzle del día ─────────────────────────────────────────────
def wavesling(L):
    m = L["mock"]
    b = []
    x = 20
    for i, tab in enumerate(m["tabs"]):
        tw = width(tab, 19, 700) + 26
        b.append(_rect(x, 20, tw, 40, INK if i == 0 else PAPER, 0 if i == 0 else 1.5, EDGE, 20)
                 + text(x + tw / 2, 46, tab, 19, ON_INK if i == 0 else INK, 700, anchor="middle"))
        x += tw + 8
    y = 108
    for ln in wrap(m["heading"], 28, MW - 40, 800):
        b.append(text(20, y, ln, 28, INK, 800))
        y += 32
    cell = 56
    bx, by = (MW - 5 * cell) / 2, y + 12
    for r in range(5):
        for c in range(5):
            b.append(_rect(bx + c * cell, by + r * cell, cell, cell, PAPER if (r + c) % 2 == 0 else PALE, 0))
    b.append(_rect(bx, by, 5 * cell, 5 * cell, "none", 1.5, EDGE, 0))
    cx, cy = bx + 2.5 * cell, by + 2.5 * cell
    k = cell / 64
    for i, (dx, dy) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
        b.append(f'<g class="pulse" style="animation-delay:{i * 0.6:.1f}s">'
                 f'{_arrow2d(cx + dx * 40 * k, cy + dy * 40 * k, cx + dx * 140 * k, cy + dy * 140 * k, BLUE, 10 * k, 24 * k)}</g>')
    b.append(_piece(cx, cy + 26 * k, "rook", 58 * k, PAPER))
    sy = by + 5 * cell + 22
    for i, kind in enumerate(("rook", "bishop", "king", "pawn")):
        sx = (MW - 266) / 2 + i * 70
        b.append(_rect(sx, sy, 56, 56, PAPER if i == 0 else STONE, 2.4 if i == 0 else 0, BLUE, 10))
        b.append(_piece(sx + 28, sy + 48, kind, 40, PAPER))
    yy = sy + 92
    for ln in wrap(m["caption"], 19, MW - 48, 600):
        b.append(text(MW / 2, yy, ln, 19, INK, 600, anchor="middle"))
        yy += 25
    return browser(yy + 10, "wavesbyling.com", "".join(b))
