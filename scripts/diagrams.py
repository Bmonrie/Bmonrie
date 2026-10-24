"""Diagramas planos: tiras de pasos y arquitecturas, sobre una cuadrícula.

Todas las cajas de un diagrama miden lo mismo y todas las flechas son rectas: van de una caja a la de al
lado, en la misma fila o en la misma columna. Cada flecha lleva encima un trazo animado que marca el
sentido del flujo. El azul pleno es la pieza que sostiene el sistema; el discontinuo, lo que es externo.
"""
import math

from icons import icon
from kit import BLUE, INK, MUTED, PAPER, PW, PM, flow, text, wrap

T, S = 21, 18  # título y línea de una caja: nunca por debajo de 18 px
SW = 2.2
DESK = dict(bw=200, bh=136, gx=(904 - 4 * 200) / 3, gy=46)
PHONE = dict(bw=PW - 2 * PM, bh=108, gx=0, gy=40)


def _head(x, y, ang, size=12):
    p1 = (x - size * math.cos(ang) + size * 0.55 * math.sin(ang), y - size * math.sin(ang) - size * 0.55 * math.cos(ang))
    p2 = (x - size * math.cos(ang) - size * 0.55 * math.sin(ang), y - size * math.sin(ang) + size * 0.55 * math.cos(ang))
    return f'<polygon points="{x:.1f},{y:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{INK}"/>'


def arrow(x1, y1, x2, y2, both=False):
    """Flecha recta con su trazo de flujo."""
    ang = math.atan2(y2 - y1, x2 - x1)
    out = [f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="{SW}"/>',
           flow(x1 + 4 * math.cos(ang), y1 + 4 * math.sin(ang), x2 - 13 * math.cos(ang), y2 - 13 * math.sin(ang)),
           _head(x2, y2, ang)]
    if both:
        out.append(_head(x1, y1, ang + math.pi))
    return "".join(out)


def box(x, y, w, h, title, sub="", kind="plain"):
    """Caja de tamaño fijo: título y una línea, centrados en vertical y alineados a la izquierda."""
    fill = BLUE if kind == "key" else PAPER
    tc, sc = (PAPER, PAPER) if kind == "key" else (INK, MUTED)
    dash = ' stroke-dasharray="8 6"' if kind == "external" else ""
    tl = wrap(title, T, w - 28, 700)
    sl = wrap(sub, S, w - 28) if sub else []
    need = T + (len(tl) - 1) * 25 + (10 + len(sl) * 23 if sl else 0)
    if need + 30 > h:
        print(f"  ! la caja «{title}» no cabe ({need + 30:.0f} > {h})")
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{SW}"{dash}/>']
    ty = y + (h - need) / 2 + T - 3
    for i, ln in enumerate(tl):
        out.append(text(x + 14, ty + i * 25, ln, T, tc, 700))
    ty += (len(tl) - 1) * 25 + 10
    for i, ln in enumerate(sl):
        out.append(text(x + 14, ty + 23 * (i + 1) - 4, ln, S, sc))
    return "".join(out)


def grid(nodes, edges, rows=None, bw=200, bh=124, gx=34.7, gy=46, x0=0.0, label_h=34):
    """Coloca cajas en (columna, fila) y une con flechas rectas las que comparten fila o columna.

    nodes: {id: (col, row, (title, sub), kind)} · edges: [(a, b) o (a, b, "both")] · rows: rótulo por fila o None.
    Devuelve (svg, alto)."""
    n_rows = 1 + max(r for _, r, _, _ in nodes.values())
    rows = rows or [None] * n_rows
    ys, y = [], 0.0
    out = []
    for r in range(n_rows):
        if rows[r]:
            out.append(text(x0, y + 20, rows[r], S, MUTED, 700))
            y += label_h
        ys.append(y)
        y += bh + gy
    pos = {k: (x0 + c * (bw + gx), ys[r]) for k, (c, r, _, _) in nodes.items()}
    for k, (c, r, (t, s), kind) in nodes.items():
        out.append(box(*pos[k], bw, bh, t, s, kind))
    for e in edges:
        a, b = e[0], e[1]
        (ax, ay), (bx, by) = pos[a], pos[b]
        both = len(e) > 2
        if abs(ay - by) < 1:  # misma fila
            yy = ay + bh / 2
            out.append(arrow(ax + bw, yy, bx, yy, both) if ax < bx else arrow(ax, yy, bx + bw, yy, both))
        else:  # misma columna
            xx = ax + bw / 2
            out.append(arrow(xx, ay + bh, xx, by, both) if ay < by else arrow(xx, ay, xx, by + bh, both))
    return "".join(out), y - gy


# ─── La tira de pasos: cómo funciona, en cuatro cajas iguales ────────────────
def steps(items, icons_, key, phone=False):
    """items: [(título, línea)] · icons_: nombre de icono por paso · key: índice del paso en azul."""
    out = []
    if not phone:
        bw, gx = DESK["bw"], DESK["gx"]
        bh = max(128 + (len(wrap(t, T, bw - 28, 700)) - 1) * 25 + 4 + len(wrap(s, S, bw - 28)) * 23 for t, s in items) + 18
        for i, ((t, s), ic) in enumerate(zip(items, icons_)):
            x = i * (bw + gx)
            out.append(f'<rect x="{x:.1f}" y="0" width="{bw}" height="{bh}" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>')
            out.append(icon(ic, x + 16, 18, key == i))
            y = 128
            for ln in wrap(t, T, bw - 28, 700):
                out.append(text(x + 14, y, ln, T, INK, 700))
                y += 25
            y += 4
            for ln in wrap(s, S, bw - 28):
                out.append(text(x + 14, y, ln, S, MUTED))
                y += 23
            if i:
                out.append(arrow(x - gx + 3, 54, x - 3, 54))
        return "".join(out), bh
    bw = PW - 2 * PM
    tw = bw - 104 - 12
    bh = max(38 + (len(wrap(t, T, tw, 700)) - 1) * 25 + 2 + len(wrap(s, S, tw)) * 23 for t, s in items) + 14
    bh = max(bh, 104)
    gy = 40
    for i, ((t, s), ic) in enumerate(zip(items, icons_)):
        y = i * (bh + gy)
        out.append(f'<rect x="0" y="{y:.1f}" width="{bw}" height="{bh}" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>')
        out.append(icon(ic, 16, y + (bh - 72) / 2, key == i))
        yy = y + 38
        for ln in wrap(t, T, tw, 700):
            out.append(text(104, yy, ln, T, INK, 700))
            yy += 25
        yy += 2
        for ln in wrap(s, S, tw):
            out.append(text(104, yy, ln, S, MUTED))
            yy += 23
        if i:
            out.append(arrow(52, y - gy + 3, 52, y - 3))
    return "".join(out), 4 * bh + 3 * gy


# ─── Arquitecturas ───────────────────────────────────────────────────────────
def _deck(nodes, edges, rows=None, phone=False, **kw):
    spec = dict(PHONE if phone else DESK)
    spec.update(kw)
    return grid(nodes, edges, rows, **spec)


def kakurega(L, phone=False):
    a = L["arch"]
    if phone:
        nodes = {"b": (0, 0, a["browser"], "plain"), "c": (0, 1, a["cdn"], "external"), "y": (0, 2, a["caddy"], "plain"),
                 "api": (0, 3, a["api"], "key"), "db": (0, 4, a["db"], "plain"), "ocr": (0, 5, a["ocr"], "plain")}
        return _deck(nodes, [("b", "c"), ("c", "y"), ("y", "api"), ("api", "db"), ("ocr", "db")], phone=True)
    nodes = {"b": (0, 0, a["browser"], "plain"), "c": (1, 0, a["cdn"], "external"), "y": (2, 0, a["caddy"], "plain"),
             "k": (1, 1, a["content"], "plain"), "api": (2, 1, a["api"], "key"), "db": (3, 1, a["db"], "plain"),
             "ocr": (3, 2, a["ocr"], "plain")}
    top, h1 = _deck(nodes, [("b", "c"), ("c", "y"), ("y", "api"), ("k", "api"), ("api", "db"), ("ocr", "db")])
    steps_ = {f"s{i}": (i, 0, st, "plain") for i, st in enumerate(a["deploy"])}
    low, h2 = _deck(steps_, [("s0", "s1"), ("s1", "s2"), ("s2", "s3")], rows=[a["ships"]])
    return top + f'<g transform="translate(0 {h1 + 56:.0f})">{low}</g>', h1 + 56 + h2


def blunderling(L, phone=False):
    a = L["arch"]
    if phone:
        nodes = {"l": (0, 0, a["lichess"], "external"), "s": (0, 1, a["stockfish"], "plain"),
                 "a": (0, 2, a["actions_phone"], "key"), "y": (0, 3, a["youtube"], "external"), "j": (0, 4, a["ledger"], "plain")}
        return _deck(nodes, [("l", "s"), ("s", "a"), ("a", "y"), ("y", "j")], phone=True)
    nodes = {"l": (0, 0, a["lichess"], "external"), "s": (1, 0, a["stockfish"], "plain"),
             "a": (0, 1, a["actions"], "key"), "r": (1, 1, a["remotion"], "plain"), "y": (2, 1, a["youtube"], "external"),
             "j": (3, 1, a["ledger"], "plain"),
             "o": (1, 2, a["statsjson"], "plain"), "n": (2, 2, a["analytics"], "external"), "t": (3, 2, a["stats"], "plain")}
    edges = [("l", "s"), ("s", "r"), ("a", "r"), ("r", "y"), ("y", "j"), ("j", "t"), ("t", "n"), ("n", "o")]
    return _deck(nodes, edges, rows=[a["analyst"], a["daily"], a["weekly"]])


def agents(L, phone=False):
    a = L["arch"]
    keys = ("clients", "core", "adapters", "external")
    kinds = {"core": "key", "external": "external"}
    if phone:
        nodes = {k: (0, r, (a[k][0], ", ".join(t for t, _ in a[k][1])), kinds.get(k, "plain")) for r, k in enumerate(keys)}
        return _deck(nodes, [(keys[i], keys[i + 1]) for i in range(3)], phone=True)
    nodes = {f"{k}{c}": (c, r, item, kinds.get(k, "plain")) for r, k in enumerate(keys) for c, item in enumerate(a[k][1])}
    edges = [(f"{keys[i]}1", f"{keys[i + 1]}1") for i in range(3)]  # una flecha por capa
    return _deck(nodes, edges, rows=[a[k][0] for k in keys])


def wavesling(L, phone=False):
    a = L["arch"]
    if phone:
        nodes = {"w": (0, 0, a["web"], "plain"), "e": (0, 1, a["engine"], "key"), "o": (0, 2, a["others"], "plain")}
        return _deck(nodes, [("w", "e"), ("o", "e")], phone=True)
    nodes = {"w": (1, 0, a["web"], "plain"), "g": (0, 1, a["game"], "plain"), "e": (1, 1, a["engine"], "key"),
             "s": (2, 1, a["autoplay"], "plain"), "n": (1, 2, a["generator"], "plain")}
    return _deck(nodes, [("w", "e"), ("g", "e"), ("s", "e"), ("n", "e")], x0=72, gx=80)
