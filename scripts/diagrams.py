"""Diagramas de arquitectura en plano, con el mismo trazo que las figuras isométricas.

Cajas de tinta sobre papel, el amarillo para la pieza que sostiene el sistema, discontinuo para lo
que es externo, y gris piedra para agrupar. Texto mínimo de 18 px.
"""
import math

from kit import INK, MUTED, PAPER, STONE, YELLOW, text, wrap

T, S = 21, 18  # título y línea de una caja
SW = 2.2
TINT = STONE  # fondo de los grupos; la lámina lo cambia si su propio fondo ya es piedra
GROUND = PAPER  # fondo de la lámina, para el halo de los rótulos de las flechas


def node_height(w, title, sub=""):
    tl = wrap(title, T, w - 28, 700)
    sl = wrap(sub, S, w - 28) if sub else []
    return 36 + T + (len(tl) - 1) * 25 + (8 + len(sl) * 23 if sl else 0)


def node(x, y, w, title, sub="", fill=PAPER, dashed=False, h=None, center=False):
    """Caja con título y una línea; crece si el texto no cabe en `h`. Devuelve (svg, alto)."""
    tl = wrap(title, T, w - 28, 700)
    sl = wrap(sub, S, w - 28) if sub else []
    need = node_height(w, title, sub)
    hh = max(h or 0, need)
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{hh:.1f}" fill="{fill}" stroke="{INK}" '
           f'stroke-width="{SW}"{dash}/>']
    tx, anchor = (x + w / 2, "middle") if center else (x + 14, "start")
    ty = y + (hh - need) / 2 + 17 + T
    for i, ln in enumerate(tl):
        out.append(text(tx, ty + i * 25, ln, T, INK, 700, anchor=anchor))
    ty += (len(tl) - 1) * 25
    for i, ln in enumerate(sl):
        out.append(text(tx, ty + 8 + 23 * (i + 1), ln, S, MUTED if fill == PAPER else INK, anchor=anchor))
    return "".join(out), hh


def group(x, y, w, h, label):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{TINT}"/>'
            + text(x + 14, y + 28, label, S, INK, 700))


def edge(points, label=None, at=0.5, both=False, lx=0, ly=-10):
    """Flecha en ángulo recto que termina en punta; `label` va sobre el tramo indicado por `at`."""
    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in points)
    out = [f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>']
    out.append(_head(points[-2], points[-1]))
    if both:
        out.append(_head(points[1], points[0]))
    if label:
        i = min(int(at * (len(points) - 1)), len(points) - 2)
        (x1, y1), (x2, y2) = points[i], points[i + 1]
        mx, my = (x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly
        out.append(text(mx, my, label, S, INK, 600, anchor="middle", halo=GROUND))
    return "".join(out)


def _head(a, b, size=12):
    (x1, y1), (x2, y2) = a, b
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - size * math.cos(ang) + size * 0.55 * math.sin(ang), y2 - size * math.sin(ang) - size * 0.55 * math.cos(ang))
    p2 = (x2 - size * math.cos(ang) - size * 0.55 * math.sin(ang), y2 - size * math.sin(ang) + size * 0.55 * math.cos(ang))
    return f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{INK}"/>'


# ─── Kakurega ────────────────────────────────────────────────────────────────
def kakurega(L):
    a = L["arch"]
    b = []
    gx, cw = 392, 230  # grupo del servidor y ancho de sus columnas
    c1, c2 = gx + 18, gx + 18 + cw + 20
    r1 = max(node_height(cw, *a["caddy"]), node_height(cw, *a["ocr"]))
    r2 = max(node_height(cw, *a["api"]), node_height(cw, *a["db"]))
    y1, y2 = 48, 48 + r1 + 34
    y3 = y2 + r2 + 30
    r3 = node_height(2 * cw + 20, *a["content"])
    gh = y3 + r3 + 18
    hb = max(node_height(166, *a["browser"]), node_height(166, *a["cdn"]))
    yb = y1 + r1 / 2 - hb / 2
    b.append(node(0, yb, 166, *a["browser"], h=hb)[0])
    b.append(node(196, yb, 166, *a["cdn"], dashed=True, h=hb)[0])
    b.append(group(gx, 0, 904 - gx, gh, a["host"]))
    b.append(node(c1, y1, cw, *a["caddy"], h=r1)[0])
    b.append(node(c2, y1, cw, *a["ocr"], h=r1)[0])
    b.append(node(c1, y2, cw, *a["api"], fill=YELLOW, h=r2)[0])
    b.append(node(c2, y2, cw, *a["db"], h=r2)[0])
    b.append(node(c1, y3, 2 * cw + 20, *a["content"], h=r3)[0])
    mid = yb + hb / 2
    b.append(edge([(166, mid), (196, mid)]))
    b.append(edge([(362, mid), (c1, mid)]))
    b.append(edge([(c1 + cw / 2, y1 + r1), (c1 + cw / 2, y2)]))
    b.append(edge([(c1 + cw, y2 + r2 / 2), (c2, y2 + r2 / 2)]))
    b.append(edge([(c2 + cw / 2, y1 + r1), (c2 + cw / 2, y2)]))
    b.append(edge([(c1 + cw / 2, y2 + r2), (c1 + cw / 2, y3)]))
    # Cómo se publica: un grupo con su rótulo, sin amarillo (el amarillo es la API)
    y0 = gh + 30
    steps = a["deploy"]
    wst = (904 - 32 - 3 * 32) / 4
    hs = max(node_height(wst, *st) for st in steps)
    b.append(group(0, y0, 904, 48 + hs + 18, a["ships"]))
    y = y0 + 48
    for i, (t, s_) in enumerate(steps):
        x = 16 + i * (wst + 32)
        b.append(node(x, y, wst, t, s_, h=hs)[0])
        if i:
            b.append(edge([(x - 32, y + hs / 2), (x, y + hs / 2)]))
    return "".join(b), y + hs + 18


# ─── BlunderLing ─────────────────────────────────────────────────────────────
def blunderling(L):
    a = L["arch"]
    # Una sola vez: los puzles y su análisis quedan fijados en el repo
    w1 = 300
    r1 = max(node_height(w1, *a["lichess"]), node_height(w1, *a["stockfish"]))
    g1 = 48 + r1 + 18
    b = [group(0, 0, 904, g1, a["analyst"])]
    b.append(node(16, 48, w1, *a["lichess"], dashed=True, h=r1)[0])
    b.append(node(16 + w1 + 56, 48, w1, *a["stockfish"], h=r1)[0])
    b.append(edge([(16 + w1, 48 + r1 / 2), (16 + w1 + 56, 48 + r1 / 2)]))
    # Cada día, sin nadie: la Action renderiza, sube y apunta
    g2 = g1 + 64
    wa, wr, wy = 270, 250, 270
    xa, xr, xy = 16, 16 + wa + 46, 16 + wa + 46 + wr + 46
    r2 = max(node_height(wa, *a["actions"]), node_height(wr, *a["remotion"]), node_height(wy, *a["youtube"]))
    rl = node_height(904 - 32, *a["ledger"])
    gh2 = 48 + r2 + 40 + rl + 18
    b.append(group(0, g2, 904, gh2, a["daily"]))
    b.append(node(xa, g2 + 48, wa, *a["actions"], fill=YELLOW, h=r2)[0])
    b.append(node(xr, g2 + 48, wr, *a["remotion"], h=r2)[0])
    b.append(node(xy, g2 + 48, wy, *a["youtube"], dashed=True, h=r2)[0])
    my = g2 + 48 + r2 / 2
    b.append(edge([(xa + wa, my), (xr, my)]))
    b.append(edge([(xr + wr, my), (xy, my)]))
    yl = g2 + 48 + r2 + 40
    b.append(node(16, yl, 904 - 32, *a["ledger"], h=rl)[0])
    b.append(edge([(xa + wa / 2, g2 + 48 + r2), (xa + wa / 2, yl)], both=True))
    # El análisis fijado entra en el render
    sx = 16 + w1 + 56 + w1 / 2
    b.append(edge([(sx, 48 + r1), (sx, g2 + 20), (xr + wr / 2, g2 + 20), (xr + wr / 2, g2 + 48)]))
    b.append(text(sx + 14, g1 + 36, a["baked"], S, INK, 600))
    # Cada lunes: la retención
    g3 = g2 + gh2 + 26
    r3 = max(node_height(270, *a[k]) for k in ("stats", "analytics", "statsjson"))
    b.append(group(0, g3, 904, 48 + r3 + 18, a["weekly"]))
    b.append(node(16, g3 + 48, 262, *a["stats"], h=r3)[0])
    b.append(node(320, g3 + 48, 262, *a["analytics"], dashed=True, h=r3)[0])
    b.append(node(626, g3 + 48, 262, *a["statsjson"], h=r3)[0])
    b.append(edge([(278, g3 + 48 + r3 / 2), (320, g3 + 48 + r3 / 2)]))
    b.append(edge([(582, g3 + 48 + r3 / 2), (626, g3 + 48 + r3 / 2)]))
    return "".join(b), g3 + 48 + r3 + 18


# ─── Template_Agents ─────────────────────────────────────────────────────────
def agents(L):
    a = L["arch"]
    b = []
    rows = [("clients", a["clients"], PAPER, False), ("core", a["core"], YELLOW, False),
            ("adapters", a["adapters"], PAPER, False), ("external", a["external"], PAPER, True)]
    y = 0
    lab_w = 150
    gap = 46
    for key, (label, items), fill, dashed in rows:
        n_items = len(items)
        cw = (904 - lab_w - (n_items - 1) * 12) / n_items
        rh = max(84, max(node_height(cw, t, s_) for t, s_ in items))
        b.append(text(0, y + rh / 2 + 7, label, S + 1, INK, 700))
        if key == "core":
            b.append(f'<rect x="{lab_w:.1f}" y="{y:.1f}" width="{904 - lab_w:.1f}" height="{rh}" fill="{YELLOW}" '
                     f'stroke="{INK}" stroke-width="{SW}"/>')
            for i, (t, s_) in enumerate(items):
                x = lab_w + i * (cw + 12)
                b.append(text(x + cw / 2 + 6, y + 36, t, T, INK, 700, anchor="middle"))
                b.append(text(x + cw / 2 + 6, y + 62, s_, S, INK, anchor="middle"))
        else:
            for i, (t, s_) in enumerate(items):
                x = lab_w + i * (cw + 12)
                n, _ = node(x, y, cw, t, s_, fill=fill, dashed=dashed, h=rh, center=True)
                b.append(n)
        if key != "external":
            b.append(edge([(lab_w + (904 - lab_w) / 2, y + rh), (lab_w + (904 - lab_w) / 2, y + rh + gap)],
                          a["calls"][key], lx=0, ly=4))
        y += rh + gap
    return "".join(b), y - gap


# ─── WavesLing ───────────────────────────────────────────────────────────────
def wavesling(L):
    a = L["arch"]
    b = []
    n, _ = node(312, 196, 280, *a["engine"], fill=YELLOW, h=128)
    b.append(n)
    around = [("web", 0, 0), ("server", 312, 0), ("game", 624, 0), ("generator", 0, 392), ("autoplay", 312, 392),
              ("tests", 624, 392)]
    for key, x, y in around:
        n, _ = node(x, y, 280, *a[key], h=104)
        b.append(n)
    b.append(edge([(140, 104), (140, 160), (380, 160), (380, 196)]))
    b.append(edge([(452, 104), (452, 196)]))
    b.append(edge([(764, 104), (764, 160), (524, 160), (524, 196)]))
    b.append(edge([(140, 392), (140, 360), (380, 360), (380, 324)]))
    b.append(edge([(452, 392), (452, 324)]))
    b.append(edge([(764, 392), (764, 360), (524, 360), (524, 324)]))
    b.append(text(452, 176, a["imports"], S, INK, 600, anchor="middle", halo=GROUND))
    return "".join(b), 496
