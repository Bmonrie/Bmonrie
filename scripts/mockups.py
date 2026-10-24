"""Maquetas de cada producto, redibujadas en plano con el estilo del número (no son capturas).

Cada una tiene versión de escritorio (904 de ancho) y de teléfono (360). Toda letra que se lee mide 18 px o
más; lo que es relleno se dibuja como barra, nunca como texto diminuto.
"""
import math

from iso import PIECES
from kit import BLUE, INK, MUTED, NOVA, ON_INK, ON_INK_SOFT, PALE, PAPER, PM, PW, STONE, esc, text, width, wrap

DEEP = "#10146B"  # el fondo de los Shorts: índigo profundo
PHW = PW - 2 * PM  # ancho útil en teléfono


def _rect(x, y, w, h, fill, sw=2.2, stroke=INK, rx=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if sw else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{st}{r}{extra}/>'


def browser(w, h, url, body, cid):
    """Ventana de navegador: barra con la dirección y el contenido recortado a su marco."""
    bar = 54
    return (f'<defs><clipPath id="{cid}"><rect x="0" y="{bar}" width="{w}" height="{h - bar}"/></clipPath></defs>'
            + _rect(0, 0, w, h, PAPER)
            + _rect(0, 0, w, bar, STONE, 0)
            + _rect(16, 12, w - 32, 30, PAPER, 1.6)
            + text(32, 33, url, 18, INK, 500)
            + f'<g clip-path="url(#{cid})"><g transform="translate(0 {bar})">{body}</g></g>'
            + f'<line x1="0" y1="{bar}" x2="{w}" y2="{bar}" stroke="{INK}" stroke-width="2.2"/>'
            + _rect(0, 0, w, h, "none"))


def jp(x, y, s, size, fill=INK, wght=400, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="j" font-size="{size}" font-weight="{wght}" fill="{fill}" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


def _piece2d(x, y, kind, size, fill):
    return (f'<path d="{PIECES[kind]}" transform="translate({x:.1f} {y:.1f}) scale({size:.1f})" fill="{fill}" '
            f'stroke="{INK}" stroke-width="{2.0 / size:.4f}" stroke-linejoin="round"/>')


def _arrow2d(x1, y1, x2, y2, fill, w=10, head=24, cls=""):
    L_ = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L_, (y2 - y1) / L_
    nx, ny = -uy, ux
    qx, qy = x2 - ux * head, y2 - uy * head
    pts = [(x1 + nx * w / 2, y1 + ny * w / 2), (qx + nx * w / 2, qy + ny * w / 2), (qx + nx * head * 0.6, qy + ny * head * 0.6),
           (x2, y2), (qx - nx * head * 0.6, qy - ny * head * 0.6), (qx - nx * w / 2, qy - ny * w / 2),
           (x1 - nx * w / 2, y1 - ny * w / 2)]
    c = f' class="{cls}"' if cls else ""
    return (f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.6" stroke-linejoin="round"{c}/>')


# ─── Kakurega: el lector con el diccionario emergente ────────────────────────
READING = [
    "するとその地獄の底に、犍陀多と云う男が一人、",
    "ほかの罪人と一しょに蠢いている姿が、",
    "御眼に止まりました。この犍陀多と云う男は、",
    "人を殺したり家に火をつけたり、いろいろ",
    "悪事を働いた大泥坊でございますが、",
    "ある時この男が深い林の中を通りますと、",
    "小さな蜘蛛が一匹、路ばたを這って行くのが",
    "見えました。",
]
UNDERLINES = {0: [(6, 2), (11, 3)], 2: [(0, 2), (12, 3)], 3: [(0, 1), (2, 2)], 5: [(11, 1)]}


def _popup(m, cx, cy, cw):
    """El diccionario emergente: lectura, palabra, significado y sus kanji."""
    b = [_rect(cx, cy, cw, 360, PAPER), jp(cx + 22, cy + 40, "くも", 20, MUTED), jp(cx + 22, cy + 92, "蜘蛛", 44, INK, 700)]
    tw = width(m["common"], 18, 600) + 24
    b.append(_rect(cx + 130, cy + 64, tw, 32, STONE, 0) + text(cx + 142, cy + 86, m["common"], 18, INK, 600))
    b.append(text(cx + 22, cy + 132, m["noun"], 18, MUTED))
    b.append(text(cx + 22, cy + 162, m["meaning"], 24, INK, 700))
    b.append(text(cx + 22, cy + 198, m["add"], 19, BLUE, 700))
    b.append(_rect(cx, cy + 222, cw, 138, STONE, 0))
    for i, (k, on) in enumerate((("蜘", "ち"), ("蛛", "ちゅ、しゅ"))):
        yy = cy + 238 + i * 60
        b.append(_rect(cx + 22, yy, 50, 50, PAPER, 1.6) + jp(cx + 47, yy + 36, k, 30, INK, 700, "middle"))
        b.append(text(cx + 88, yy + 22, m["spider"], 20, INK, 700))
        b.append(text(cx + 88, yy + 46, "On:", 18, MUTED) + jp(cx + 124, yy + 46, on, 18, MUTED))
    b.append(_rect(cx, cy, cw, 360, "none"))
    return "".join(b)


def _reading(lines, x0, y0, size, lead, unders, mark):
    b = []
    for i, ln in enumerate(lines):
        y = y0 + i * lead
        if mark in ln:  # la palabra que se ha tocado
            k = ln.index(mark)
            b.append(_rect(x0 + k * size - 3, y - size + 1, len(mark) * size + 6, size + 9, PALE, 0))
        b.append(jp(x0, y, ln, size))
        for (a, n) in unders.get(i, []):
            b.append(f'<line x1="{x0 + a * size:.1f}" y1="{y + 8:.1f}" x2="{x0 + (a + n) * size - 3:.1f}" y2="{y + 8:.1f}" '
                     f'stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="3 4"/>')
    return "".join(b)


def kakurega(L, phone=False):
    m = L["mock"]
    if phone:
        w = PHW
        b = [_rect(0, 0, w, 56, INK, 0), text(20, 37, "Kakurega", 22, ON_INK, 800, 110)]
        for i in range(3):
            b.append(_rect(w - 46, 18 + i * 8, 26, 3, ON_INK, 0))
        b.append(jp(20, 98, "蜘蛛の糸", 22, INK, 700))
        flat = "".join(READING[5:8])
        lines = [flat[i:i + 14] for i in range(0, len(flat), 14)]
        b.append(_reading(lines, 20, 146, 22, 42, {}, "蜘蛛"))
        top = 146 + len(lines) * 42
        b.append(_popup(m, 20, top, w - 40))
        h = 54 + top + 360 + 24
        return browser(w, h, "kakuregalearn.com", "".join(b), "ckm"), h
    w, h = 904, 600
    b = [_rect(0, 0, w, 62, INK, 0), text(28, 40, "Kakurega", 24, ON_INK, 800, 110)]
    x = 200
    for i, item in enumerate(m["nav"]):
        active = i == 3
        b.append(text(x, 39, item, 19, ON_INK if active else ON_INK_SOFT, 700 if active else 500))
        x += width(item, 19, 700 if active else 500) + 40
    b.append(jp(40, 108, "蜘蛛の糸", 24, INK, 700))
    b.append(_reading(READING, 40, 160, 24, 47, UNDERLINES, "蜘蛛"))
    b.append(_popup(m, 598, 178, 280))
    return browser(w, h, "kakuregalearn.com", "".join(b), "ck"), h


# ─── BlunderLing: un Short y las tres franjas del día ────────────────────────
def _board(x, y, cell, hi=()):
    out = []
    for r in range(8):
        for c in range(8):
            f = NOVA if (c, r) in hi else (PAPER if (r + c) % 2 == 0 else PALE)
            out.append(_rect(x + c * cell, y + r * cell, cell, cell, f, 0))
    out.append(_rect(x, y, 8 * cell, 8 * cell, "none", 2.2))
    return "".join(out)


# Una Escocesa tras 3...exd4 4.Nxd4: el caballo negro de f6 acaba de saltar a d5 (las dos casillas marcadas)
BLACK = [(0, 0, "rook"), (2, 0, "bishop"), (3, 0, "queen"), (4, 0, "king"), (5, 0, "bishop"), (7, 0, "rook"),
         (2, 2, "knight"), (3, 3, "knight")] + [(c, 1, "pawn") for c in (0, 1, 2, 3, 5, 6, 7)]
WHITE_ = [(0, 7, "rook"), (2, 7, "bishop"), (3, 7, "queen"), (4, 7, "king"), (7, 7, "rook"), (2, 5, "knight"),
          (3, 4, "knight"), (2, 4, "bishop"), (4, 4, "pawn")] + [(c, 6, "pawn") for c in (0, 1, 2, 5, 6, 7)]


def _short(m, px, py, pw, ph, cell):
    """El teléfono con el Short: frase, tablero y título."""
    b = [_rect(px, py, pw, ph, INK, 2.2, INK, 40), _rect(px + 12, py + 12, pw - 24, ph - 24, DEEP, 0, rx=30)]
    hs = min(28, min(28 * (pw - 64) / width(ln, 28, 800) for ln in m["hook"]))
    for i, ln in enumerate(m["hook"]):
        b.append(text(px + pw / 2, py + 72 + i * (hs + 8), ln, round(hs, 1), ON_INK, 800, anchor="middle"))
    bx, by = px + (pw - 8 * cell) / 2, py + 72 + 2 * (hs + 8) + 14
    b.append(f'<g class="pulse">{_rect(bx + 3 * cell, by + 3 * cell, cell, cell, NOVA, 0)}</g>')
    b.append(_board(bx, by, cell, hi={(3, 3), (5, 2)}))
    for (c, r, kind, fill) in [(c, r, k, INK) for c, r, k in BLACK] + [(c, r, k, PAPER) for c, r, k in WHITE_]:
        b.append(_piece2d(bx + c * cell + cell / 2, by + r * cell + cell - 3, kind, cell * 0.95, fill))
    y = by + 8 * cell + 40
    b.append(text(px + 30, y, "@BlunderLing", 19, ON_INK_SOFT, 600))
    y += 32
    for ln in wrap(m["title"], 19, pw - 60, 600)[:3]:
        b.append(text(px + 30, y, ln, 19, ON_INK, 600))
        y += 26
    return "".join(b)


def _slot(x, y, w, t, name, line, h=160, tcol=176):
    b = [_rect(x, y, w, h, PAPER), text(x + 22, y + 60 if h > 120 else y + 50, t, 44 if h > 120 else 34, INK, 800, 112, cls="n")]
    ty = y + 50 if h > 120 else y + 34
    tx = x + tcol
    b.append(text(tx, ty, name, 21, INK, 700))
    ly = ty + 28
    for ln in wrap(line, 18, w - tcol - 18):
        b.append(text(tx, ly, ln, 18, MUTED))
        ly += 23
    return "".join(b)


def blunderling(L, phone=False):
    m = L["mock"]
    if phone:
        w = PHW
        b = [_short(m, (w - 290) / 2, 0, 290, 560, 28)]
        y = 590
        for t, name, line in m["slots"]:
            b.append(_slot(0, y, w, t, name, line, h=118, tcol=138))
            y += 136
        return "".join(b), y - 18
    b = [_short(m, 40, 10, 312, 600, 31)]
    for i, (t, name, line) in enumerate(m["slots"]):
        b.append(_slot(410, 40 + i * 186, 494, t, name, line))
    return "".join(b), 620


# ─── Template_Agents: el chat que trae la plantilla ──────────────────────────
def _chat(m, x0, w, y0, h):
    """La columna del chat: pregunta, herramienta aprobada, respuesta con cita y caja de escribir."""
    b = []
    qw = min(w - 40, width(m["question"], 19, 500) + 40)
    b.append(_rect(x0 + w - qw, y0, qw, 52, INK, 0) + text(x0 + w - qw + 20, y0 + 33, m["question"], 19, ON_INK, 500))
    ty = y0 + 80
    lines = wrap(m["approval"], 19, w - 40, 600)
    ch = 150 + (len(lines) - 1) * 25
    b.append(_rect(x0, ty, w, ch, PAPER))
    b.append(text(x0 + 20, ty + 38, "get_order_status", 21, INK, 700))
    b.append(text(x0 + 20, ty + 68, m["args"], 18, MUTED))
    for i, ln in enumerate(lines):
        b.append(text(x0 + 20, ty + 98 + i * 25, ln, 19, INK, 600))
    by = ty + 108 + (len(lines) - 1) * 25
    aw = width(m["approved"], 19, 700) + 40
    b.append(_rect(x0 + 20, by, aw, 34, BLUE, 0) + text(x0 + 20 + aw / 2, by + 23, m["approved"], 19, PAPER, 700, anchor="middle"))
    b.append(text(x0 + 36 + aw, by + 23, m["by"], 18, MUTED))
    y = ty + ch + 40
    for ln in wrap(m["answer"], 21, w):
        b.append(text(x0, y, ln, 21, INK))
        y += 31
    cw = width(m["cite"], 18, 600) + 28
    b.append(_rect(x0, y - 6, cw, 34, STONE, 0) + text(x0 + 14, y + 17, m["cite"], 18, INK, 600))
    b.append(_rect(x0, h - 96, w, 50, PAPER) + text(x0 + 30, h - 64, m["input"], 19, MUTED))
    b.append(f'<g class="blink">{_rect(x0 + 18, h - 84, 3, 26, BLUE, 0)}</g>')
    return "".join(b)


def agents(L, phone=False):
    m = L["mock"]
    if phone:
        w, h = PHW, 640
        body = _chat(m, 20, w - 40, 24, h - 54)
        return browser(w, h, "localhost:3000", body, "cam"), h
    w, h = 904, 600
    b = [_rect(0, 0, 240, h, STONE, 0), text(24, 44, m["convos"], 20, INK, 700)]
    for i, c in enumerate(m["threads"]):
        y = 74 + i * 54
        if i == 0:
            b.append(_rect(12, y, 216, 44, PAPER, 1.6))
        b.append(text(26, y + 29, c, 19, INK, 600 if i == 0 else 400))
    b.append(_chat(m, 270, 604, 30, h))
    return browser(w, h + 54, "localhost:3000", "".join(b), "ca"), h + 54


# ─── WavesLing: el puzle del día ─────────────────────────────────────────────
def _tabs(m, x, y, pad=34, gap=12):
    b = []
    for i, tab in enumerate(m["tabs"]):
        tw = width(tab, 19, 700) + pad
        b.append(_rect(x, y, tw, 40, INK if i == 0 else PAPER) + text(x + tw / 2, y + 26, tab, 19, ON_INK if i == 0 else INK, 700, anchor="middle"))
        x += tw + gap
    return "".join(b)


def _tide_board(bx, by, cell):
    b = []
    for r in range(5):
        for c in range(5):
            b.append(_rect(bx + c * cell, by + r * cell, cell, cell, PAPER if (r + c) % 2 == 0 else PALE, 0))
    b.append(_rect(bx, by, 5 * cell, 5 * cell, "none"))
    cx, cy = bx + 2.5 * cell, by + 2.5 * cell
    k = cell / 64
    for i, (dx, dy) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
        b.append(f'<g class="pulse" style="animation-delay:{i * 0.6:.1f}s">'
                 f'{_arrow2d(cx + dx * 40 * k, cy + dy * 40 * k, cx + dx * 140 * k, cy + dy * 140 * k, BLUE, 10 * k, 24 * k)}</g>')
    b.append(_piece2d(cx, cy + 26 * k, "rook", 58 * k, PAPER))
    return "".join(b)


def _selector(m, x, y, cx, maxw=420):
    b = []
    for i, kind in enumerate(("rook", "bishop", "king", "pawn")):
        sx = x + i * 70
        b.append(_rect(sx, y, 56, 56, PAPER if i == 0 else STONE, 3.2 if i == 0 else 0))
        b.append(_piece2d(sx + 28, y + 48, kind, 40, PAPER))
    for k, ln in enumerate(wrap(m["caption"], 19, maxw, 600)):
        b.append(text(cx, y + 92 + k * 25, ln, 19, INK, 600, anchor="middle"))
    return "".join(b)


def wavesling(L, phone=False):
    m = L["mock"]
    if phone:
        w = PHW
        b = [_tabs(m, 20, 22, 22, 8)]
        y = 110
        for ln in wrap(m["heading"], 30, w - 40, 800, 105):
            b.append(text(20, y, ln, 30, INK, 800, 105))
            y += 34
        y += 8
        for ln in wrap(m["body"], 18, w - 40):
            b.append(text(20, y, ln, 18, MUTED))
            y += 25
        cell = 56
        bx, by = (w - 5 * cell) / 2, y + 14
        b.append(_tide_board(bx, by, cell))
        sy = by + 5 * cell + 22
        b.append(_selector(m, (w - 266) / 2, sy, w / 2, w - 48))
        h = 54 + sy + 150
        return browser(w, h, "wavesbyling.com", "".join(b), "cwm"), h
    w, h = 904, 600
    b = [_tabs(m, 28, 22)]
    y = 140
    for ln in wrap(m["heading"], 34, 230, 800, 105):
        b.append(text(28, y, ln, 34, INK, 800, 105))
        y += 38
    y += 12
    for ln in wrap(m["body"], 19, 230):
        b.append(text(28, y, ln, 19, MUTED))
        y += 27
    bx, by = 300, 86
    b.append(_tide_board(bx, by, 64))
    b.append(_selector(m, bx + 34, by + 5 * 64 + 24, bx + 160))
    # El mando de ocho direcciones
    px, py, k = 680, 150, 62
    b.append(_rect(px - 14, py - 14, 3 * k + 28, 3 * k + 28, STONE))
    for r in range(3):
        for c in range(3):
            x0, y0 = px + c * k, py + r * k
            b.append(_rect(x0 + 4, y0 + 4, k - 8, k - 8, PAPER, 1.8))
            if (r, c) != (1, 1):
                ang = math.atan2(r - 1, c - 1)
                mx, my = x0 + k / 2, y0 + k / 2
                b.append(_arrow2d(mx - 12 * math.cos(ang), my - 12 * math.sin(ang), mx + 14 * math.cos(ang),
                                  my + 14 * math.sin(ang), INK, 4, 12))
    b.append(text(px + 1.5 * k, py + 3 * k + 50, m["pad"], 19, MUTED, anchor="middle"))
    return browser(w, h, "wavesbyling.com", "".join(b), "cw"), h
