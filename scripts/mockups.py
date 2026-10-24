"""Maquetas de cada producto, redibujadas en plano con el estilo de las figuras (no son capturas).

Toda letra que se lee mide 18 px o más; lo que es relleno se dibuja como barra, nunca como texto
diminuto.
"""
from iso import PIECES
from kit import INK, MUTED, ON_INK, ON_INK_SOFT, PAPER, STONE, YELLOW, esc, text, width, wrap

GREY, DARK = "#C9CCD2", "#26282D"


def _rect(x, y, w, h, fill, sw=2.2, stroke=INK, rx=0):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if sw else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{st}{r}/>'


def browser(w, h, url, body, cid):
    """Ventana de navegador: barra con la dirección y el contenido recortado a su marco."""
    bar = 54
    return (f'<defs><clipPath id="{cid}"><rect x="0" y="{bar}" width="{w}" height="{h - bar}"/></clipPath></defs>'
            + _rect(0, 0, w, h, PAPER)
            + _rect(0, 0, w, bar, STONE, 0)
            + _rect(18, 12, w - 36, 30, PAPER, 1.6)
            + text(36, 33, url, 18, INK, 500)
            + f'<g clip-path="url(#{cid})"><g transform="translate(0 {bar})">{body}</g></g>'
            + f'<line x1="0" y1="{bar}" x2="{w}" y2="{bar}" stroke="{INK}" stroke-width="2.2"/>'
            + _rect(0, 0, w, h, "none"))


def jp(x, y, s, size, fill=INK, wght=400, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="j" font-size="{size}" font-weight="{wght}" fill="{fill}" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


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


def kakurega(L, w=904, h=600):
    m = L["mock"]
    b = [_rect(0, 0, w, 62, INK, 0), text(28, 40, "Kakurega", 24, ON_INK, 800, 110)]
    x = 200
    for i, item in enumerate(m["nav"]):
        active = i == 3
        b.append(text(x, 39, item, 19, ON_INK if active else ON_INK_SOFT, 700 if active else 500))
        x += len(item) * 11 + 40
    b.append(jp(40, 108, "蜘蛛の糸", 24, INK, 700))
    size, lead, x0, y0 = 24, 47, 40, 160
    for i, ln in enumerate(READING):
        y = y0 + i * lead
        if i == 6:  # la palabra que se ha tocado
            k = ln.index("蜘蛛")
            b.append(_rect(x0 + k * size - 3, y - size + 1, 2 * size + 6, size + 9, YELLOW, 0))
        b.append(jp(x0, y, ln, size))
        for (a, n) in {0: [(6, 2), (11, 3)], 2: [(0, 2), (12, 3)], 3: [(0, 1), (2, 2)], 5: [(11, 1)]}.get(i, []):
            b.append(f'<line x1="{x0 + a * size:.1f}" y1="{y + 8:.1f}" x2="{x0 + (a + n) * size - 3:.1f}" y2="{y + 8:.1f}" '
                     f'stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="3 4"/>')
    # El diccionario emergente, al lado de la palabra
    cx, cy, cw = 598, 178, 280
    b.append(_rect(cx, cy, cw, 360, PAPER))
    b.append(jp(cx + 22, cy + 40, "くも", 20, MUTED))
    b.append(jp(cx + 22, cy + 92, "蜘蛛", 44, INK, 700))
    tw = len(m["common"]) * 10.5 + 24
    b.append(_rect(cx + 130, cy + 64, tw, 32, STONE, 0) + text(cx + 142, cy + 86, m["common"], 18, INK, 600))
    b.append(text(cx + 22, cy + 132, m["noun"], 18, MUTED))
    b.append(text(cx + 22, cy + 162, m["meaning"], 24, INK, 700))
    b.append(text(cx + 22, cy + 198, m["add"], 19, INK, 600))
    b.append(_rect(cx, cy + 222, cw, 138, STONE, 0))
    for i, (k, on) in enumerate((("蜘", "ち"), ("蛛", "ちゅ、しゅ"))):
        yy = cy + 238 + i * 60
        b.append(_rect(cx + 22, yy, 50, 50, PAPER, 1.6) + jp(cx + 47, yy + 36, k, 30, INK, 700, "middle"))
        b.append(text(cx + 88, yy + 22, m["spider"], 20, INK, 700))
        b.append(text(cx + 88, yy + 46, "On:", 18, MUTED) + jp(cx + 124, yy + 46, on, 18, MUTED))
    b.append(_rect(cx, cy, cw, 360, "none"))
    return browser(w, h, "kakuregalearn.com", "".join(b), "ck"), h


# ─── BlunderLing: un Short y las tres franjas del día ────────────────────────
def _board(x, y, cell, light=PAPER, dark=GREY, hi=()):
    out = []
    for r in range(8):
        for c in range(8):
            f = YELLOW if (c, r) in hi else (light if (r + c) % 2 == 0 else dark)
            out.append(_rect(x + c * cell, y + r * cell, cell, cell, f, 0))
    out.append(_rect(x, y, 8 * cell, 8 * cell, "none", 2.2))
    return "".join(out)


def _piece2d(x, y, kind, size, fill):
    return (f'<path d="{PIECES[kind]}" transform="translate({x:.1f} {y:.1f}) scale({size:.1f})" fill="{fill}" '
            f'stroke="{INK}" stroke-width="{2.0 / size:.4f}" stroke-linejoin="round"/>')


def blunderling(L, w=904, h=620):
    m = L["mock"]
    px, py, pw, ph = 40, 10, 312, 600
    b = [_rect(px, py, pw, ph, INK, 2.2, INK, 40), _rect(px + 12, py + 12, pw - 24, ph - 24, DARK, 0, rx=30)]
    hs = min(28, min(28 * (pw - 64) / width(ln, 28, 800) for ln in m["hook"]))
    for i, ln in enumerate(m["hook"]):
        b.append(text(px + pw / 2, py + 82 + i * (hs + 8), ln, round(hs, 1), ON_INK, 800, anchor="middle"))
    cell = 31
    bx, by = px + (pw - 8 * cell) / 2, py + 170
    # Una Escocesa tras 3...exd4 4.Nxd4: el caballo negro de f6 acaba de saltar a d5 (las dos casillas en amarillo)
    b.append(_board(bx, by, cell, hi={(3, 3), (5, 2)}))
    black = [(0, 0, "rook"), (2, 0, "bishop"), (3, 0, "queen"), (4, 0, "king"), (5, 0, "bishop"), (7, 0, "rook"),
             (2, 2, "knight"), (3, 3, "knight")] + [(c, 1, "pawn") for c in (0, 1, 2, 3, 5, 6, 7)]
    white = [(0, 7, "rook"), (2, 7, "bishop"), (3, 7, "queen"), (4, 7, "king"), (7, 7, "rook"), (2, 5, "knight"),
             (3, 4, "knight"), (2, 4, "bishop"), (4, 4, "pawn")] + [(c, 6, "pawn") for c in (0, 1, 2, 5, 6, 7)]
    for (c, r, kind, fill) in [(c, r, k, INK) for c, r, k in black] + [(c, r, k, PAPER) for c, r, k in white]:
        b.append(_piece2d(bx + c * cell + cell / 2, by + r * cell + cell - 3, kind, cell * 0.95, fill))
    b.append(text(px + 30, py + 470, "@BlunderLing", 19, ON_INK_SOFT, 600))
    y = py + 502
    for ln in wrap(m["title"], 19, pw - 60, 600)[:3]:
        b.append(text(px + 30, y, ln, 19, ON_INK, 600))
        y += 26
    # Las tres franjas
    x0, y0 = 410, 40
    for i, (t, name, line) in enumerate(m["slots"]):
        yy = y0 + i * 186
        b.append(_rect(x0, yy, 494, 160, PAPER))
        b.append(text(x0 + 24, yy + 62, t, 48, INK, 800, 112, cls="n"))
        b.append(text(x0 + 200, yy + 50, name, 22, INK, 700))
        ly = yy + 80
        for ln in wrap(line, 19, 270):
            b.append(text(x0 + 200, ly, ln, 19, MUTED))
            ly += 25
    return "".join(b), h


# ─── Template_Agents: el chat que trae la plantilla ──────────────────────────
def agents(L, w=904, h=600):
    m = L["mock"]
    b = [_rect(0, 0, 240, h, STONE, 0), text(24, 44, m["convos"], 20, INK, 700)]
    for i, c in enumerate(m["threads"]):
        y = 74 + i * 54
        if i == 0:
            b.append(_rect(12, y, 216, 44, PAPER, 1.6))
        b.append(text(26, y + 29, c, 19, INK, 600 if i == 0 else 400))
    # El mensaje del usuario
    qw = 330
    b.append(_rect(w - 30 - qw, 30, qw, 52, INK, 0) + text(w - 30 - qw + 20, 63, m["question"], 19, ON_INK, 500))
    # La herramienta que pide permiso
    tx, ty = 270, 110
    b.append(_rect(tx, ty, 534, 168, PAPER))
    b.append(text(tx + 20, ty + 38, "get_order_status", 21, INK, 700))
    b.append(text(tx + 20, ty + 68, m["args"], 18, MUTED))
    b.append(text(tx + 20, ty + 98, m["approval"], 19, INK, 600))
    aw = width(m["approved"], 19, 700) + 40
    b.append(_rect(tx + 20, ty + 114, aw, 40, YELLOW) + text(tx + 20 + aw / 2, ty + 140, m["approved"], 19, INK, 700, anchor="middle"))
    b.append(text(tx + 40 + aw, ty + 140, m["by"], 19, MUTED))
    # La respuesta, con su cita
    y = 318
    for ln in wrap(m["answer"], 21, 560):
        b.append(text(270, y, ln, 21, INK))
        y += 31
    cw = len(m["cite"]) * 10 + 40
    b.append(_rect(270, y - 6, cw, 34, STONE, 0) + text(284, y + 17, m["cite"], 18, INK, 600))
    # La caja de escribir
    b.append(_rect(270, h - 96, w - 300, 50, PAPER) + text(290, h - 64, m["input"], 19, MUTED))
    return browser(w, h + 54, "localhost:3000", "".join(b), "ca"), h + 54


# ─── WavesLing: el puzle del día ─────────────────────────────────────────────
def _arrow2d(x1, y1, x2, y2, fill, w=10, head=24):
    import math
    L_ = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L_, (y2 - y1) / L_
    nx, ny = -uy, ux
    qx, qy = x2 - ux * head, y2 - uy * head
    pts = [(x1 + nx * w / 2, y1 + ny * w / 2), (qx + nx * w / 2, qy + ny * w / 2), (qx + nx * head * 0.6, qy + ny * head * 0.6),
           (x2, y2), (qx - nx * head * 0.6, qy - ny * head * 0.6), (qx - nx * w / 2, qy - ny * w / 2),
           (x1 - nx * w / 2, y1 - ny * w / 2)]
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'


def wavesling(L, w=904, h=600):
    m = L["mock"]
    b = []
    x = 28
    for i, tab in enumerate(m["tabs"]):
        tw = len(tab) * 11 + 34
        b.append(_rect(x, 22, tw, 40, INK if i == 0 else PAPER) + text(x + tw / 2, 48, tab, 19, ON_INK if i == 0 else INK, 700, anchor="middle"))
        x += tw + 12
    y = 140
    for ln in wrap(m["heading"], 34, 230, 800, 105):
        b.append(text(28, y, ln, 34, INK, 800, 105))
        y += 38
    y += 12
    for ln in wrap(m["body"], 19, 230):
        b.append(text(28, y, ln, 19, MUTED))
        y += 27
    # El tablero, la torre y sus cuatro direcciones
    cell, bx, by = 64, 300, 86
    for r in range(5):
        for c in range(5):
            b.append(_rect(bx + c * cell, by + r * cell, cell, cell, PAPER if (r + c) % 2 == 0 else GREY, 0))
    b.append(_rect(bx, by, 5 * cell, 5 * cell, "none"))
    cx, cy = bx + 2.5 * cell, by + 2.5 * cell
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        b.append(_arrow2d(cx + dx * 40, cy + dy * 40, cx + dx * 140, cy + dy * 140, YELLOW))
    b.append(_piece2d(cx, cy + 26, "rook", 58, PAPER))
    sy = by + 5 * cell + 24
    for i, kind in enumerate(("rook", "bishop", "king", "pawn")):
        sx = bx + 34 + i * 70
        b.append(_rect(sx, sy, 56, 56, PAPER if i == 0 else STONE, 3.2 if i == 0 else 0))
        b.append(_piece2d(sx + 28, sy + 48, kind, 40, PAPER))
    b.append(text(bx + 160, sy + 92, m["caption"], 19, INK, 600, anchor="middle"))
    # El mando de ocho direcciones
    px, py, k = 680, 150, 62
    b.append(_rect(px - 14, py - 14, 3 * k + 28, 3 * k + 28, STONE))
    import math
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
