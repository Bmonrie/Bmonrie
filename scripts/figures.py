"""Las figuras explicativas: una por proyecto y la de portada, todas en el mismo dibujo isométrico.

Cada función recibe los rótulos en el idioma de la lámina y devuelve (svg, alto). Las coordenadas
son locales a la figura; la lámina la coloca con un translate.
"""
from iso import DARK, FLOOR, GREY, WHITE, YELL, Iso, piece
from kit import INK, MUTED, PAPER, STONE, YELLOW, esc, text, wrap

LABEL, LINE = 22, 19  # tamaños de rótulo: nunca por debajo de 18 px


def callout(anchor, ly, title, line, maxw=230, side="right", fill=INK, muted=MUTED, ring=PAPER, tx=None):
    """Rótulo con guía: punto en la pieza, tramo vertical hasta la altura del rótulo y un tramo
    horizontal hasta el texto (corto, o hasta `tx` si se da una columna fija)."""
    ax, ay = anchor
    k = 1 if side == "right" else -1
    tx = ax + k * 16 if tx is None else tx
    out = [f'<polyline points="{ax:.1f},{ay:.1f} {ax:.1f},{ly - 7:.1f} {tx - k * 8:.1f},{ly - 7:.1f}" fill="none" '
           f'stroke="{fill}" stroke-width="1.6" stroke-linejoin="round"/>',
           f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="5" fill="{fill}" stroke="{ring}" stroke-width="2"/>']
    anchor_txt = "start" if side == "right" else "end"
    out.append(text(tx, ly, title, LABEL, fill, 700, anchor=anchor_txt))
    y = ly + 26
    for ln in wrap(line, LINE, maxw):
        out.append(text(tx, y, ln, LINE, muted, anchor=anchor_txt))
        y += 24
    return "".join(out)


# ─── Kakurega: de la obra que quieres leer a las lecciones de cada día ───────
SPINE = ("#FFFFFF", "#26282D", "#B9BCC3")


def kakurega(L, w=904):
    g = Iso(250, 120, 38)
    b = [g.box(-0.4, -0.4, -0.45, 15.8, 6.0, 0.45, FLOOR)]
    # La obra: dos tomos de manga y un fichero de subtítulos
    b.append(g.box(0.7, 0.9, 0, 2.2, 3.0, 0.42, SPINE))
    b.append(g.box(0.85, 1.05, 0.42, 2.0, 2.8, 0.42, SPINE))
    z = 0.84
    for (x0, x1, y0, y1, f) in [(1.0, 1.8, 1.2, 2.25, STONE), (1.9, 2.7, 1.2, 2.25, PAPER), (1.0, 2.7, 2.35, 3.7, PAPER)]:
        b.append(g.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], f, 1.4))
    b.append(g.box(0.8, 4.3, 0, 2.1, 0.8, 0.06, WHITE))
    for k in range(3):
        yy = 4.45 + k * 0.2
        b.append(g.line((1.0, yy, 0.06), (2.4 - k * 0.3, yy, 0.06), 2.4, MUTED))
    b.append(g.arrow((3.3, 4.75), (5.1, 4.75)))
    # El analizador: OCR y medida de lo que ya entiendes
    b.append(g.box(5.4, 1.2, 0, 2.8, 2.9, 2.2, WHITE))
    b.append(g.poly([(5.9, 1.7, 2.2), (7.7, 1.7, 2.2), (7.7, 1.98, 2.2), (5.9, 1.98, 2.2)], DARK[1], 1.4))
    b.append(g.panel_y(5.65, 4.1, 0.3, 2.3, 1.6, INK))
    b.append(g.panel_y(5.95, 4.1, 0.75, 1.7, 0.3, DARK[0], 0))
    b.append(g.panel_y(5.95, 4.1, 0.75, 1.7 * 0.62, 0.3, PAPER, 0))
    b.append(g.line((5.95 + 1.7 * 0.9, 4.1, 0.62), (5.95 + 1.7 * 0.9, 4.1, 1.18), 2.4, PAPER))
    b.append(f'<g transform="{g.matrix_y(5.95 + 0.85, 4.1, 1.5)}">'
             f'<text x="0" y="0" font-size="0.5" font-weight="800" fill="{PAPER}" text-anchor="middle">90%</text></g>')
    b.append(g.arrow((8.5, 4.75), (9.9, 4.75)))
    # Las lecciones: sus palabras y sus kanji primero
    for k in range(4):
        tone = YELL if k == 3 else WHITE
        b.append(g.box(9.9 + k * 0.1, 1.4 - k * 0.12, k * 0.13, 2.1, 2.5, 0.12, tone))
    zt = 3 * 0.13 + 0.12
    b.append(f'<g transform="{g.matrix_top(11.25, 2.45, zt)}"><text x="0" y="0.28" class="j" font-size="0.78" '
             f'fill="{INK}" text-anchor="middle">{esc("焼く")}</text></g>')
    b.append(g.arrow((12.4, 4.75), (13.4, 4.75)))
    # El lector con diccionario
    b.append(g.box(14.0, 2.75, 0, 0.7, 0.6, 0.35, WHITE))
    b.append(g.box(13.4, 3.35, 0, 2.1, 0.22, 3.0, WHITE))
    b.append(g.panel_y(13.5, 3.57, 0.15, 1.9, 2.7, PAPER, 1.4))
    for i, uw in enumerate([1.5, 1.3, 0.5, 1.4, 1.1]):
        b.append(g.panel_y(13.7, 3.57, 2.45 - i * 0.42, uw, 0.13, GREY[0], 0))
    b.append(g.panel_y(14.28, 3.57, 2.45 - 2 * 0.42 - 0.08, 0.95, 0.3, GREY[1], 1.2))
    b.append(g.panel_y(14.1, 3.82, 0.35, 1.45, 0.95, WHITE[0], 2.0))
    b.append(g.panel_y(14.25, 3.82, 1.02, 0.55, 0.12, INK, 0))
    b.append(g.panel_y(14.25, 3.82, 0.75, 1.1, 0.09, GREY[1], 0))
    b.append(g.panel_y(14.25, 3.82, 0.55, 0.8, 0.09, GREY[1], 0))

    c = L["fig"]
    b.append(callout(g.p(1.85, 2.0, 0.84), 40, *c["work"], maxw=240))
    b.append(callout(g.p(6.4, 4.1, 0.9), 600, *c["analyze"], maxw=250, side="left"))
    b.append(callout(g.p(10.6, 1.3, 0.51), 70, *c["lessons"], maxw=210))
    b.append(callout(g.p(14.8, 3.82, 0.8), 565, *c["reader"], maxw=210))
    return "".join(b), 720


# ─── BlunderLing: la cadena que publica tres Shorts al día ───────────────────
def blunderling(L, w=904):
    g = Iso(285, 135, 36)
    b = [g.box(-0.4, -0.2, -0.45, 16.8, 5.8, 0.45, FLOOR)]
    # Datos abiertos de Lichess
    b.append(g.cyl(1.3, 2.6, 0, 1.05, 2.2, WHITE, bands=2))
    # La estación de render, detrás de la cinta
    b.append(g.box(8.5, 0.1, 0, 1.9, 1.4, 2.7, WHITE))
    b.append(g.panel_x(10.4, 0.35, 1.3, 0.9, 0.9, INK))
    b.append(g.box(8.8, 1.5, 1.55, 1.3, 0.75, 0.32, WHITE))
    # Pilar trasero del motor
    b.append(g.box(5.2, 1.55, 0, 1.4, 0.4, 2.6, WHITE))
    # La cinta y sus patas
    for x in (3.0, 7.2, 11.4):
        b.append(g.box(x, 2.2, 0, 0.3, 1.0, 0.55, GREY))
    b.append(g.box(2.6, 1.95, 0.55, 12.6, 1.5, 0.25, DARK))
    zb = 0.8
    for x in (3.1, 7.4):
        b.append(g.box(x, 2.2, zb, 1.0, 1.0, 0.1, WHITE))
        b.append(g.top_grid(x, 2.2, zb + 0.1, 1.0, 1.0, 4, 4, [PAPER, GREY[1]]))
    # El Short ya renderizado, de pie sobre la cinta
    b.append(g.box(11.0, 2.55, zb, 0.95, 0.12, 1.69, WHITE))
    b.append(g.panel_y(11.06, 2.67, zb + 0.06, 0.83, 1.57, INK))
    for i in range(3):
        for j in range(3):
            f = PAPER if (i + j) % 2 == 0 else GREY[1]
            b.append(g.panel_y(11.2 + i * 0.18, 2.67, zb + 0.55 + j * 0.18, 0.18, 0.18, f, 0))
    b.append(g.panel_y(11.18, 2.67, zb + 1.3, 0.6, 0.09, PAPER, 0))
    b.append(g.panel_y(11.26, 2.67, zb + 1.16, 0.44, 0.07, PAPER, 0))
    # Pilar delantero y viga del motor (Stockfish verifica cada línea)
    b.append(g.box(5.2, 3.45, 0, 1.4, 0.4, 2.6, WHITE))
    b.append(g.box(5.1, 1.5, 2.6, 1.6, 2.4, 0.55, WHITE))
    b.append(g.panel_y(5.35, 3.9, 2.7, 1.1, 0.32, INK))
    b.append(f'<circle cx="{g.p(5.9, 3.9, 2.86)[0]:.1f}" cy="{g.p(5.9, 3.9, 2.86)[1]:.1f}" r="4" fill="{PAPER}"/>')
    # La estación que sube los vídeos a su hora
    b.append(g.box(13.9, 1.5, 0, 2.2, 2.5, 2.3, YELL))
    b.append(g.panel_y(14.15, 4.0, 0.55, 1.7, 1.15, INK))
    cx, cy = g.p(15.0, 4.0, 1.12)
    b.append(f'<path d="M{cx - 9:.1f} {cy - 13:.1f}L{cx + 13:.1f} {cy + 0:.1f}L{cx - 9:.1f} {cy + 13:.1f}Z" fill="{PAPER}"/>')
    for i, t in enumerate(("13:17", "18:17", "23:17")):
        b.append(f'<g transform="{g.matrix_x(16.1, 3.75, 1.78 - i * 0.56)}"><text x="0" y="0" font-size="0.5" '
                 f'font-weight="700" fill="{INK}" class="n">{t}</text></g>')
    # El registro que impide repetir
    b.append(g.box(12.0, 4.35, 0, 1.4, 1.0, 0.36, SPINE))
    b.append(g.arrow((12.6, 4.15), (13.6, 3.3), z=0.02, w=0.16, head=0.42))

    c = L["fig"]
    b.append(callout(g.p(1.3, 2.6, 2.2), 30, *c["data"], maxw=250, side="left"))
    b.append(callout(g.p(5.9, 3.85, 1.3), 575, *c["engine"], maxw=220, side="left"))
    b.append(callout(g.p(9.45, 0.8, 2.7), 40, *c["render"], maxw=210))
    b.append(callout(g.p(12.7, 4.85, 0.36), 590, *c["publish"], maxw=240))
    return "".join(b), 670


# ─── Template_Agents: una carpeta de datos, un núcleo sin proveedor, cualquier modelo ──
def agents(L, w=904):
    g = Iso(330, 190, 40)
    b = [g.box(-0.4, -0.4, -0.45, 13.4, 7.2, 0.45, FLOOR)]
    # La carpeta del agente: YAML, prompt, herramientas, evals
    b.append(g.box(0.0, 2.0, 0, 2.6, 2.1, 0.6, WHITE))
    b.append(g.box(0.15, 1.85, 0.6, 1.0, 0.5, 0.12, WHITE))
    for k in range(4):
        b.append(g.box(0.35 + k * 0.55, 2.3, 0.6, 0.07, 1.5, 1.2 - k * 0.1, WHITE, 1.6))
    b.append(g.arrow((2.9, 3.05), (4.1, 3.05)))
    # El núcleo: bucle, políticas, memoria, varios agentes
    b.append(g.box(4.3, 1.4, 0, 3.1, 3.2, 1.5, YELL))
    for i in range(3):
        for j in range(2):
            b.append(g.box(4.55 + i * 0.95, 1.65 + j * 1.45, 1.5, 0.75, 1.2, 0.32, WHITE, 1.6))
    b.append(g.arrow((7.7, 3.0), (9.4, 3.0)))
    # Los modelos: una pila de intercambiables, el núcleo no sabe cuál hay. El nombre va en su cara.
    providers = L["fig"]["providers"]
    for k, name in enumerate(providers):
        z = k * 0.8
        b.append(g.box(9.5, 2.2, z, 3.3, 1.7, 0.66, WHITE))
        b.append(f'<g transform="{g.matrix_y(9.68, 3.9, z + 0.17)}"><text x="0" y="0" font-size="0.46" '
                 f'font-weight="700" fill="{INK}">{esc(name)}</text></g>')
    # Memoria y conocimiento: Postgres con pgvector, delante
    b.append(g.cyl(5.85, 6.0, 0, 0.75, 1.25, WHITE, bands=2))

    c = L["fig"]
    b.append(callout(g.p(1.3, 2.9, 1.3), 60, *c["folder"], maxw=230, side="left"))
    b.append(callout(g.p(5.9, 1.9, 1.82), 40, *c["core"], maxw=230))
    b.append(callout(g.p(11.15, 3.05, 3.86), 150, *c["models"], maxw=230))
    b.append(callout(g.p(5.2, 6.0, 0.6), 600, *c["store"], maxw=240, side="left"))
    return "".join(b), 690


# ─── WavesLing: una marea mueve todas las piezas; las reglas se miden ─────────
def wavesling(L, w=904):
    g = Iso(330, 120, 56)
    b = [g.box(-0.5, -0.5, -0.35, 6.0, 6.8, 0.35, FLOOR)]
    b.append(g.box(0, 0, 0, 5, 5, 0.42, WHITE))
    b.append(g.top_grid(0, 0, 0.42, 5, 5, 5, 5, [PAPER, GREY[0]]))
    z = 0.42
    # Antes (contorno discontinuo) y después de la marea hacia +x
    moves = [("rook", 0, 1, 3, PAPER), ("king", 1, 3, 2, INK), ("rook", 2, 4, 4, INK), ("pawn", 3, 0, 4, PAPER),
             ("bishop", 4, 2, 3, PAPER)]
    for kind, row, x0, x1, fill in sorted(moves, key=lambda m: m[1] + m[3]):
        if x1 != x0:
            b.append(g.arrow((x0 + 0.75, row + 0.5), (x1 + 0.25, row + 0.5), z=z + 0.005, w=0.1, head=0.3, fill=INK))
            px, py = g.p(x0 + 0.5, row + 0.5, z)
            b.append(piece(px, py, kind, 46, "none").replace('stroke-linejoin', 'stroke-dasharray="0.06 0.05" stroke-linejoin'))
    for kind, row, x0, x1, fill in sorted(moves, key=lambda m: m[1] + m[3]):
        px, py = g.p(x1 + 0.5, row + 0.5, z)
        b.append(piece(px, py, kind, 58, fill))
    # La marea
    b.append(g.arrow((0.3, 5.75), (4.9, 5.75), z=0, w=0.42, head=0.95, fill=YELLOW, sw=2.2))
    # Lo medido: tablas en partidas simuladas, antes y después
    k = 0.055
    b.append(g.box(6.4, -0.1, 0, 1.1, 1.1, 71.9 * k, GREY))
    b.append(g.box(8.6, 1.0, 0, 1.1, 1.1, 23 * k, YELL))
    c = L["fig"]
    px, py = g.p(6.95, 0.45, 71.9 * k)
    b.append(text(px, py - 64, c["fmt"](71.9), 34, INK, 800, 112, anchor="middle", cls="n"))
    b.append(text(px, py - 38, c["before"], LINE, MUTED, anchor="middle"))
    px, py = g.p(9.7, 1.0, 23 * k)
    b.append(text(px + 18, py + 4, c["fmt"](23.0), 34, INK, 800, 112, cls="n"))
    b.append(text(px + 18, py + 30, c["after"], LINE, MUTED))
    b.append(callout(g.p(2.5, 5.75, 0.0), 585, *c["tide"], maxw=300))
    return "".join(b), 660


# ─── Portada: todo lo que hace falta para que un sistema de IA llegue y aguante ──
def stack(L, w=904):
    """Cinco plataformas que bajan en escalera: de lo que razona (arriba) a lo que lo mantiene vivo."""
    g = Iso(185, 300, 25)
    out, anchors = [], []
    W_, D_, STEP, DROP = 3.8, 4.0, 4.4, 1.05
    for i in range(5):
        x0, z = i * STEP, (4 - i) * DROP
        out.append(g.box(x0, 0, 0, W_, D_, z + 0.3, FLOOR) if i == 4 else g.box(x0, 0, z, W_, D_, 0.3, FLOOR))
        if i < 4:  # el pilar que sostiene la plataforma
            out.append(g.box(x0 + 1.4, 1.4, 0, 1.0, 1.2, z, GREY))
            out.append(g.box(x0, 0, z, W_, D_, 0.3, FLOOR))
        zt = z + 0.3
        if i == 0:  # la IA: el bloque que razona, con sus piezas
            out.append(g.box(x0 + 0.5, 0.6, zt, 2.8, 2.8, 0.95, YELL))
            for a in range(2):
                for c_ in range(2):
                    out.append(g.box(x0 + 0.72 + a * 1.32, 0.82 + c_ * 1.32, zt + 0.95, 1.1, 1.1, 0.24, WHITE, 1.6))
            anchors.append(g.p(x0 + 1.9, 2.0, zt + 1.19))
        elif i == 1:  # la interfaz: una pantalla con su acción
            out.append(g.box(x0 + 0.5, 2.0, zt, 2.8, 0.18, 1.8, WHITE))
            out.append(g.panel_y(x0 + 0.62, 2.18, zt + 0.12, 2.56, 1.56, PAPER, 1.4))
            for r, uw in enumerate([1.8, 1.4, 1.0]):
                out.append(g.panel_y(x0 + 0.85, 2.18, zt + 1.3 - r * 0.3, uw, 0.13, GREY[0], 0))
            out.append(g.panel_y(x0 + 0.85, 2.18, zt + 0.3, 0.95, 0.32, GREY[1], 1.2))
            anchors.append(g.p(x0 + 1.5, 4.0, zt))
        elif i == 2:  # el backend: servidor y base de datos
            out.append(g.box(x0 + 0.4, 0.6, zt, 1.5, 2.0, 1.3, WHITE))
            out.append(g.cyl(x0 + 2.75, 2.2, zt, 0.75, 1.0, WHITE, bands=1))
            anchors.append(g.p(x0 + 1.15, 1.6, zt + 1.3))
        elif i == 3:  # el despliegue: contenedores
            for (dx, zz) in ((0.2, 0), (1.95, 0), (1.1, 0.72)):
                out.append(g.box(x0 + dx, 1.0, zt + zz, 1.65, 2.0, 0.72, WHITE))
            anchors.append(g.p(x0 + 1.9, 2.0, zt + 1.44))
        else:  # lo que lo mantiene vivo: un reloj que nadie tiene que mirar
            out.append(g.cyl(x0 + 1.9, 2.0, zt, 1.45, 0.3, WHITE))
            cx, cy = g.p(x0 + 1.9, 2.0, zt + 0.3)
            out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx - 2:.1f}" y2="{cy - 16:.1f}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                       f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + 24:.1f}" y2="{cy + 5:.1f}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
            anchors.append((cx, cy))
    for i, (anchor, (title, line)) in enumerate(zip(anchors, L["layers"])):
        if i == 3:  # el despliegue: a la derecha, a su altura, para no pisar la última plataforma
            out.append(callout(anchor, anchor[1] + 7, title, line, maxw=165, tx=742))
        else:
            out.append(callout(anchor, 32 if i % 2 == 0 else 600, title, line, maxw=150))
    return "".join(out), 690
