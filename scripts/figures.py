"""La única figura isométrica: la escalera de la portada, todo lo que hace falta para que un sistema de IA
llegue a producción y aguante. El resto del número es plano (pasos, maquetas y diagramas).

`stack` devuelve (svg, alto). En escritorio lleva sus rótulos; en teléfono se dibuja sola y la lámina pone
la lista de capas debajo, en el mismo orden que los peldaños.
"""
from iso import ACCENT, FLOOR, GREY, WHITE, Iso
from kit import INK, MUTED, PAPER, text, wrap

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


def stack(L, phone=False):
    """Cinco plataformas que bajan en escalera: de lo que razona (arriba) a lo que lo mantiene vivo."""
    g = Iso(70, 118, 16) if phone else Iso(185, 300, 25)
    hand = 0.64 if phone else 1.0
    out, anchors = [], []
    W_, D_, STEP, DROP = 3.8, 4.0, 4.4, 1.05
    for i in range(5):
        x0, z = i * STEP, (4 - i) * DROP
        if i < 4:  # el pilar que sostiene la plataforma
            out.append(g.box(x0 + 1.4, 1.4, 0, 1.0, 1.2, z, GREY))
            out.append(g.box(x0, 0, z, W_, D_, 0.3, FLOOR))
        else:
            out.append(g.box(x0, 0, 0, W_, D_, z + 0.3, FLOOR))
        zt = z + 0.3
        if i == 0:  # la IA: el bloque que razona, con sus piezas
            out.append(g.box(x0 + 0.5, 0.6, zt, 2.8, 2.8, 0.95, ACCENT))
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
        else:  # lo que lo mantiene vivo: un reloj que nadie tiene que mirar, y que no para
            out.append(g.cyl(x0 + 1.9, 2.0, zt, 1.45, 0.3, WHITE))
            cx, cy = g.p(x0 + 1.9, 2.0, zt + 0.3)
            out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + 22 * hand:.1f}" y2="{cy + 5 * hand:.1f}" '
                       f'stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
            out.append(f'<g class="spin" style="transform-origin:{cx:.1f}px {cy:.1f}px">'
                       f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy - 17 * hand:.1f}" stroke="{INK}" '
                       f'stroke-width="2.4" stroke-linecap="round"/></g>')
            anchors.append((cx, cy))
    if phone:
        return "".join(out), 330
    for i, (anchor, (title, line)) in enumerate(zip(anchors, L["layers"])):
        if i == 3:  # el despliegue: a la derecha, a su altura, para no pisar la última plataforma
            out.append(callout(anchor, anchor[1] + 7, title, line, maxw=165, tx=742))
        else:
            out.append(callout(anchor, 32 if i % 2 == 0 else 600, title, line, maxw=150))
    return "".join(out), 690
