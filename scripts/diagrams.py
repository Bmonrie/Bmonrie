"""Diagramas de arquitectura, con el oficio de un diagrama de documentación técnica.

- Zonas: campos de tono muy claro que agrupan por capa (cliente, borde, servidor…), con su rótulo.
- Tarjetas: esquina suave, borde fino, un glifo en su ficha, título y una línea. Todas las de un diagrama
  miden lo mismo. La pieza que sostiene el sistema lleva borde y ficha azules; lo externo, borde discontinuo.
- Conectores: rectos, de puerto a puerto (el centro de un lado), finos, con punta pequeña. Por cada uno
  viaja un punto azul, como un paquete de datos. Sin rayas: en reposo, la línea es una línea.
- Leyenda al pie. Texto mínimo de 18 px en escritorio y en teléfono.
"""
from icons import glyph
from kit import BLUE, INK, MUTED, PAPER, PW, PM, text, wrap

T, S = 19, 18  # título y línea de tarjeta
EDGE = "#A9C4E4"  # borde de tarjeta
ZONE = "#F1F6FB"  # campo de zona
KEYFILL = "#EAF3FC"  # tarjeta clave
CHIP = "#E7F3F5"  # ficha del glifo
LINE = "#2C3A9E"  # conectores
CW = PW - 2 * PM  # ancho útil en teléfono


# ─── Piezas ──────────────────────────────────────────────────────────────────
def card_height(w, title, sub, phone=False):
    if phone:
        tw = w - 76
        tl, sl = wrap(title, T, tw, 700), wrap(sub, S, tw) if sub else []
        return max(84, 30 + len(tl) * 23 + len(sl) * 22 + 6)
    tl, sl = wrap(title, T, w - 28, 700), wrap(sub, S, w - 28) if sub else []
    return 14 + 34 + 30 + (len(tl) - 1) * 23 + (6 + len(sl) * 22 if sl else 0) + 16


class Card:
    """Una tarjeta colocada: guarda su caja para que los conectores salgan del centro de un lado."""

    def __init__(self, x, y, w, h, title, sub, g, kind="plain", phone=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.title, self.sub, self.g, self.kind, self.phone = title, sub, g, kind, phone

    def port(self, side):
        return {"l": (self.x, self.y + self.h / 2), "r": (self.x + self.w, self.y + self.h / 2),
                "t": (self.x + self.w / 2, self.y), "b": (self.x + self.w / 2, self.y + self.h)}[side]

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        key, ext = self.kind == "key", self.kind == "external"
        st = f'stroke="{BLUE}" stroke-width="2"' if key else f'stroke="{EDGE}" stroke-width="1.6"'
        dash = ' stroke-dasharray="6 5"' if ext else ""
        out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{KEYFILL if key else PAPER}" {st}{dash}/>']
        if self.phone:
            cx, cy = x + 14, y + (h - 34) / 2
            tx, tw = x + 62, w - 76
        else:
            cx, cy = x + 14, y + 14
            tx, tw = x + 14, w - 28
        out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="34" height="34" rx="7" fill="{BLUE if key else CHIP}"/>')
        out.append(glyph(self.g, cx + 6, cy + 6, PAPER if key else INK, 22, 1.7))
        tl = wrap(self.title, T, tw, 700)
        sl = wrap(self.sub, S, tw) if self.sub else []
        if self.phone:
            ty = y + (h - (len(tl) * 23 + len(sl) * 22)) / 2 + 17
        else:
            ty = y + 14 + 34 + 26
        for ln in tl:
            out.append(text(tx, ty, ln, T, INK, 700))
            ty += 23
        ty += 2 if self.phone else 6
        for ln in sl:
            out.append(text(tx, ty, ln, S, MUTED))
            ty += 22
        return "".join(out)


def zone(x, y, w, h, label, accent=False):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{ZONE}"/>'
            + text(x + 16, y + 27, label, S, BLUE if accent else MUTED, 700))


def link(a, b, label=None, both=False, pill=PAPER):
    """Conector recto entre dos puertos alineados, con punta pequeña y un paquete que viaja."""
    (x1, y1), (x2, y2) = a, b
    horiz = abs(y1 - y2) < 0.5
    sx = (1 if x2 > x1 else -1) if horiz else 0
    sy = 0 if horiz else (1 if y2 > y1 else -1)
    # la punta queda pegada al borde de la tarjeta de destino
    ex, ey = x2 - sx * 1.5, y2 - sy * 1.5
    out = [f'<line x1="{x1 + sx * 1.5:.1f}" y1="{y1 + sy * 1.5:.1f}" x2="{ex - sx * 8:.1f}" y2="{ey - sy * 8:.1f}" '
           f'stroke="{LINE}" stroke-width="1.7" stroke-linecap="round"/>',
           _head(ex, ey, sx, sy)]
    if both:
        out.append(_head(x1 + sx * 1.5, y1 + sy * 1.5, -sx, -sy))
    length = abs(x2 - x1) + abs(y2 - y1)
    if length > 30:
        out.append(f'<circle r="3.6" fill="{BLUE}" class="packet"><animateMotion dur="{max(1.2, length / 70):.2f}s" '
                   f'repeatCount="indefinite" path="M{x1 + sx * 4:.1f} {y1 + sy * 4:.1f}L{ex - sx * 10:.1f} {ey - sy * 10:.1f}"/></circle>')
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        from kit import width
        lw = width(label, S, 600) + 16
        if horiz:
            out.append(f'<rect x="{mx - lw / 2:.1f}" y="{my - 34:.1f}" width="{lw:.1f}" height="26" rx="5" fill="{pill}"/>'
                       + text(mx, my - 15, label, S, INK, 600, anchor="middle"))
        else:
            out.append(f'<rect x="{mx + 10:.1f}" y="{my - 14:.1f}" width="{lw:.1f}" height="28" rx="5" fill="{pill}"/>'
                       + text(mx + 18, my + 6, label, S, INK, 600))
    return "".join(out)


def _head(x, y, sx, sy, L=9, Wd=4.5):
    if sx:
        pts = [(x, y), (x - sx * L, y - Wd), (x - sx * L, y + Wd)]
    else:
        pts = [(x, y), (x - Wd, y - sy * L), (x + Wd, y - sy * L)]
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{LINE}"/>'


def legend(y, L, phone=False):
    """Leyenda: qué es la tarjeta azul, qué es el discontinuo y qué es una flecha."""
    lg = L["legend"]
    items = [(f'<rect x="0" y="-15" width="30" height="20" rx="4" fill="{KEYFILL}" stroke="{BLUE}" stroke-width="2"/>', lg[0]),
             (f'<rect x="0" y="-15" width="30" height="20" rx="4" fill="{PAPER}" stroke="{EDGE}" stroke-width="1.6" stroke-dasharray="6 5"/>', lg[1]),
             (f'<line x1="0" y1="-5" x2="22" y2="-5" stroke="{LINE}" stroke-width="1.7"/>' + _head(30, -5, 1, 0), lg[2])]
    from kit import width
    out, x, yy = [], 0.0, y
    for mark, lab in items:
        wdt = 42 + width(lab, S, 500)
        if phone and x and x + wdt > CW:
            x, yy = 0.0, yy + 34
        out.append(f'<g transform="translate({x:.1f} {yy:.1f})">{mark}</g>' + text(x + 42, yy, lab, S, MUTED, 500))
        x += wdt + 34
    return "".join(out), yy


def _stack(sections, links, L, w=CW, gap=34):
    """Teléfono: zonas una debajo de otra, tarjetas a todo lo ancho, conectores verticales."""
    out, cards, y = [], {}, 0.0
    for label, accent, items in sections:
        # En teléfono, el rótulo de zona es corto («Server», no «Server · Hetzner · …»): así la flecha que
        # entra por el centro de la primera tarjeta no lo cruza
        label = label.split(" · ")[0] if label else None
        inner = w - 28 if label else w
        hs = [card_height(inner, t, s, True) for _, (t, s), _, _ in items]
        top = 44 if label else 0
        zh = top + sum(hs) + gap * (len(items) - 1) + (16 if label else 0)
        if label:
            out.append(zone(0, y, w, zh, label, accent))
        cy = y + top
        for (key, (t, s), g, kind), h in zip(items, hs):
            cards[key] = Card(14 if label else 0, cy, inner, h, t, s, g, kind, phone=True)
            cy += h + gap
        y += zh + (26 if label else gap)
    out += [c.svg() for c in cards.values()]
    for a, b in links:
        ca, cb = cards[a], cards[b]
        out.append(link(ca.port("b"), cb.port("t")) if ca.y < cb.y else link(ca.port("t"), cb.port("b")))
    lg, ly = legend(y + 10, L, phone=True)
    out.append(lg)
    return "".join(out), ly + 8


# ─── Kakurega ────────────────────────────────────────────────────────────────
def kakurega(L, phone=False):
    a = L["arch"]
    if phone:
        return _stack([(a["z_client"], False, [("b", a["browser"], "browser", "plain")]),
                       (a["z_edge"], False, [("c", a["cdn"], "cloud", "external")]),
                       (a["z_server"], False, [("y", a["caddy"], "proxy", "plain"), ("api", a["api"], "code", "key"),
                                               ("db", a["db"], "db", "plain"), ("ocr", a["ocr"], "gear", "plain")])],
                      [("b", "c"), ("c", "y"), ("y", "api"), ("api", "db"), ("ocr", "db")], L)
    cw, gap_in, zg = 189, 24, 20
    keys = ("browser", "cdn", "caddy", "static", "api", "content", "ocr", "db")
    ch = max(card_height(cw, *a[k]) for k in keys)
    r0 = 44
    r1 = r0 + ch + 44
    r2 = r1 + ch + 44
    zs = 2 * (cw + 28) + 2 * zg  # x de la zona del servidor
    c2, c3 = zs + 14, zs + 14 + cw + gap_in
    lane = r2 + ch + 18
    out = [zone(0, 0, cw + 28, lane, a["z_client"]), zone(cw + 28 + zg, 0, cw + 28, lane, a["z_edge"]),
           zone(zs, 0, 904 - zs, lane, a["z_server"])]
    C = {"b": Card(14, r1, cw, ch, *a["browser"], "browser"),
         "c": Card(cw + 28 + zg + 14, r1, cw, ch, *a["cdn"], "cloud", "external"),
         "y": Card(c2, r1, cw, ch, *a["caddy"], "proxy"), "api": Card(c3, r1, cw, ch, *a["api"], "code", "key"),
         "w": Card(c2, r0, cw, ch, *a["static"], "layers"), "k": Card(c3, r0, cw, ch, *a["content"], "file"),
         "o": Card(c2, r2, cw, ch, *a["ocr"], "gear"), "db": Card(c3, r2, cw, ch, *a["db"], "db")}
    out += [c.svg() for c in C.values()]
    out += [link(C["b"].port("r"), C["c"].port("l")), link(C["c"].port("r"), C["y"].port("l")),
            link(C["y"].port("r"), C["api"].port("l")), link(C["y"].port("t"), C["w"].port("b")),
            link(C["api"].port("t"), C["k"].port("b")), link(C["api"].port("b"), C["db"].port("t")),
            link(C["o"].port("r"), C["db"].port("l"))]
    # Cómo se publica
    y0 = r2 + ch + 18 + 30
    dw = (904 - 28 - 3 * 30) / 4
    dh = max(card_height(dw, t, s) for t, s in a["deploy"])
    out.append(zone(0, y0, 904, 44 + dh + 18, a["z_release"]))
    D = [Card(14 + i * (dw + 30), y0 + 44, dw, dh, t, s, g) for i, ((t, s), g) in enumerate(zip(a["deploy"], ("git", "check", "package", "swap")))]
    out += [d.svg() for d in D]
    out += [link(D[i].port("r"), D[i + 1].port("l")) for i in range(3)]
    lg, ly = legend(y0 + 44 + dh + 18 + 44, L)
    out.append(lg)
    return "".join(out), ly + 8


# ─── BlunderLing ─────────────────────────────────────────────────────────────
def blunderling(L, phone=False):
    a = L["arch"]
    if phone:
        return _stack([(a["z_once"], False, [("l", a["lichess"], "board", "external"), ("s", a["stockfish"], "search", "plain")]),
                       (a["z_daily"], True, [("r", a["remotion"], "film", "key"), ("y", a["youtube"], "play", "external"),
                                             ("j", a["ledger"], "ledger", "plain")])],
                      [("l", "s"), ("s", "r"), ("r", "y"), ("y", "j")], L)
    cw = (904 - 28 - 3 * 30) / 4
    X = [14 + i * (cw + 30) for i in range(4)]
    keys = ("lichess", "stockfish", "schedule", "remotion", "youtube", "ledger", "stats", "analytics", "statsjson")
    ch = max(card_height(cw, *a[k]) for k in keys)
    z1, z2 = 0, 44 + ch + 18 + 34
    z3 = z2 + 44 + ch + 18 + 34
    out = [zone(0, z1, X[1] + cw + 14, 44 + ch + 18, a["z_once"]), zone(0, z2, 904, 44 + ch + 18, a["z_daily"], True),
           zone(X[1] - 14, z3, 904 - X[1] + 14, 44 + ch + 18, a["z_weekly"])]
    C = {"l": Card(X[0], z1 + 44, cw, ch, *a["lichess"], "board", "external"), "s": Card(X[1], z1 + 44, cw, ch, *a["stockfish"], "search"),
         "a": Card(X[0], z2 + 44, cw, ch, *a["schedule"], "clock", "key"), "r": Card(X[1], z2 + 44, cw, ch, *a["remotion"], "film"),
         "y": Card(X[2], z2 + 44, cw, ch, *a["youtube"], "play", "external"), "j": Card(X[3], z2 + 44, cw, ch, *a["ledger"], "ledger"),
         "o": Card(X[1], z3 + 44, cw, ch, *a["statsjson"], "chart"), "n": Card(X[2], z3 + 44, cw, ch, *a["analytics"], "pulse", "external"),
         "t": Card(X[3], z3 + 44, cw, ch, *a["stats"], "code")}
    out += [c.svg() for c in C.values()]
    out += [link(C["l"].port("r"), C["s"].port("l")), link(C["s"].port("b"), C["r"].port("t"), a["baked"]),
            link(C["a"].port("r"), C["r"].port("l")), link(C["r"].port("r"), C["y"].port("l")),
            link(C["y"].port("r"), C["j"].port("l")), link(C["j"].port("b"), C["t"].port("t")),
            link(C["t"].port("l"), C["n"].port("r")), link(C["n"].port("l"), C["o"].port("r"))]
    lg, ly = legend(z3 + 44 + ch + 18 + 44, L)
    out.append(lg)
    return "".join(out), ly + 8


# ─── Template_Agents ─────────────────────────────────────────────────────────
GLYPHS = {"clients": ("user", "monitor", "code", "terminal"), "core": ("loop", "shield", "bookmark", "agents"),
          "adapters": ("plug", "tool", "book", "pulse"), "external": ("spark", "server", "db", "chart")}


def agents(L, phone=False):
    a = L["arch"]
    keys = ("clients", "core", "adapters", "external")
    kinds = {"core": "key", "external": "external"}
    if phone:
        secs = [(None, False, [(k, (a[k][0], ", ".join(t for t, _ in a[k][1])), GLYPHS[k][0], kinds.get(k, "plain"))])
                for k in keys]
        return _stack(secs, [(keys[i], keys[i + 1]) for i in range(3)], L)
    lab = 132  # columna del rótulo de capa
    cw = (904 - lab - 14 - 3 * 20) / 4
    ch = max(card_height(cw, t, s) for k in keys for t, s in a[k][1])
    out, rows, y = [], [], 0.0
    for k in keys:
        zh = ch + 28
        out.append(f'<rect x="0" y="{y:.1f}" width="904" height="{zh:.1f}" rx="12" fill="{ZONE}"/>')
        title, _, rest = a[k][0].partition(" · ")
        ly = y + zh / 2 + (-4 if rest else 6)
        out.append(text(16, ly, title, S + 1, BLUE if k == "core" else INK, 700))
        if rest:
            for j, ln in enumerate(wrap(rest, S, lab - 24)):
                out.append(text(16, ly + 24 + j * 22, ln, S, BLUE if k == "core" else MUTED))
        rows.append([Card(lab + i * (cw + 20), y + 14, cw, ch, t, s, GLYPHS[k][i], kinds.get(k, "plain"))
                     for i, (t, s) in enumerate(a[k][1])])
        y += zh + 30
    for r in rows:
        out += [c.svg() for c in r]
    for r1, r2 in zip(rows, rows[1:]):
        out += [link(c1.port("b"), c2.port("t")) for c1, c2 in zip(r1, r2)]
    lg, ly = legend(y + 10, L)
    out.append(lg)
    return "".join(out), ly + 8


# ─── WavesLing ───────────────────────────────────────────────────────────────
def wavesling(L, phone=False):
    a = L["arch"]
    if phone:
        return _stack([(a["z_repo"], False, [("w", a["web"], "monitor", "plain"), ("e", a["engine"], "cube", "key"),
                                             ("o", a["others"], "gamepad", "plain")])],
                      [("w", "e"), ("o", "e")], L)
    cw, gx = 240, (904 - 28 - 3 * 240) / 2
    X = [14 + i * (cw + gx) for i in range(3)]
    keys = ("web", "game", "engine", "autoplay", "generator", "bank")
    ch = max(card_height(cw, *a[k]) for k in keys)
    R = [44 + i * (ch + 50) for i in range(3)]
    out = [zone(0, 0, 904, R[2] + ch + 18, a["z_repo"])]
    C = {"w": Card(X[1], R[0], cw, ch, *a["web"], "monitor"), "g": Card(X[0], R[1], cw, ch, *a["game"], "gamepad"),
         "e": Card(X[1], R[1], cw, ch, *a["engine"], "cube", "key"), "s": Card(X[2], R[1], cw, ch, *a["autoplay"], "loop"),
         "n": Card(X[1], R[2], cw, ch, *a["generator"], "gear"), "k": Card(X[2], R[2], cw, ch, *a["bank"], "grid")}
    out += [c.svg() for c in C.values()]
    out += [link(C["w"].port("b"), C["e"].port("t")), link(C["g"].port("r"), C["e"].port("l")),
            link(C["s"].port("l"), C["e"].port("r")), link(C["n"].port("t"), C["e"].port("b")),
            link(C["n"].port("r"), C["k"].port("l"))]
    lg, ly = legend(R[2] + ch + 18 + 44, L)
    out.append(lg)
    return "".join(out), ly + 8
