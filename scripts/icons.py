"""Iconos planos de 72 × 72 para las tiras de pasos: trazo índigo de 2.2, rellenos blanco y azul claro, y
el azul pleno solo en el paso que hace funcionar el sistema (`key=True`)."""
from iso import PIECES
from kit import BLUE, INK, PALE, PAPER, esc

SW = 2.2
DEEP = "#2B3199"  # índigo un punto más claro, para el fondo de una pantalla


def _r(x, y, w, h, fill, sw=SW, rx=0, extra=""):
    st = f' stroke="{INK}" stroke-width="{sw}"' if sw else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{st}{r}{extra}/>'


def _piece(x, y, kind, size, fill):
    return (f'<path d="{PIECES[kind]}" transform="translate({x:.1f} {y:.1f}) scale({size:.1f})" fill="{fill}" '
            f'stroke="{INK}" stroke-width="{2.0 / size:.4f}" stroke-linejoin="round"/>')


def _arrow(x1, y, x2, fill=INK, w=4):
    return (f'<path d="M{x1:.1f} {y - w / 2:.1f}H{x2 - 8:.1f}V{y - 7:.1f}L{x2:.1f} {y:.1f}L{x2 - 8:.1f} {y + 7:.1f}'
            f'V{y + w / 2:.1f}H{x1:.1f}Z" fill="{fill}"/>')


def icon(name, x, y, key=False):
    f = BLUE if key else PAPER
    on = PAPER if key else INK
    o = []
    if name == "book":  # un tomo de manga encima de otro
        o += [_r(x + 6, y + 16, 46, 50, PALE), _r(x + 18, y + 6, 46, 50, f), _r(x + 18, y + 6, 8, 50, INK),
              _r(x + 32, y + 14, 24, 16, PALE if not key else PAPER, 1.6), _r(x + 32, y + 34, 24, 14, PALE if not key else PAPER, 1.6)]
    elif name == "gauge":  # cuánto entiendes ya, contra la meta del 90 %
        o += [_r(x + 2, y + 16, 68, 40, INK), _r(x + 10, y + 30, 52, 12, DEEP, 0), _r(x + 10, y + 30, 32, 12, BLUE if key else PALE, 0),
              f'<line x1="{x + 57:.1f}" y1="{y + 24:.1f}" x2="{x + 57:.1f}" y2="{y + 48:.1f}" stroke="{PAPER}" stroke-width="2.6"/>']
    elif name == "cards":  # las lecciones: la de hoy, arriba
        o += [_r(x + 4, y + 24, 46, 42, PAPER), _r(x + 12, y + 15, 46, 42, PAPER), _r(x + 20, y + 6, 46, 42, f),
              f'<text x="{x + 43:.1f}" y="{y + 37:.1f}" class="j" font-size="26" font-weight="700" fill="{on}" '
              f'text-anchor="middle">{esc("焼")}</text>']
    elif name == "reader":  # la página real con el diccionario emergente
        o += [_r(x + 6, y + 2, 50, 66, PAPER)]
        for i, w in enumerate((34, 28, 34, 20)):
            o.append(_r(x + 14, y + 12 + i * 10, w, 4, PALE, 0))
        o += [_r(x + 26, y + 30, 16, 6, BLUE if key else INK, 0), _r(x + 30, y + 40, 38, 28, f)]
        o += [_r(x + 36, y + 48, 18, 4, on, 0), _r(x + 36, y + 56, 26, 4, PALE, 0)]
    elif name == "database":  # datos abiertos: un cilindro
        o.append(f'<path d="M{x + 12} {y + 16}V{y + 56}A24 8 0 0 0 {x + 60} {y + 56}V{y + 16}" fill="{f}" stroke="{INK}" stroke-width="{SW}"/>')
        o.append(f'<path d="M{x + 12} {y + 36}A24 8 0 0 0 {x + 60} {y + 36}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        o.append(f'<ellipse cx="{x + 36}" cy="{y + 16}" rx="24" ry="8" fill="{PALE}" stroke="{INK}" stroke-width="{SW}"/>')
    elif name == "engine":  # el motor revisa el tablero
        for i in range(3):
            for j in range(3):
                o.append(_r(x + 4 + i * 15, y + 4 + j * 15, 15, 15, PAPER if (i + j) % 2 == 0 else PALE, 0))
        o += [_r(x + 4, y + 4, 45, 45, "none"),
              f'<circle cx="{x + 48}" cy="{y + 46}" r="13" fill="{f}" stroke="{INK}" stroke-width="{SW}"/>',
              f'<line x1="{x + 57}" y1="{y + 55}" x2="{x + 68}" y2="{y + 66}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>']
    elif name == "phone":  # el Short, renderizado en código
        o += [_r(x + 18, y + 2, 36, 68, INK, SW, 6), _r(x + 22, y + 10, 28, 6, PAPER, 0)]
        for i in range(3):
            for j in range(3):
                o.append(_r(x + 23 + i * 9, y + 24 + j * 9, 9, 9, PAPER if (i + j) % 2 == 0 else PALE, 0))
        o.append(_r(x + 22, y + 56, 20, 4, BLUE if key else PALE, 0))
    elif name == "upload":  # subido a su hora
        o += [_r(x + 4, y + 10, 64, 46, f),
              f'<path d="M{x + 30} {y + 22}L{x + 48} {y + 33}L{x + 30} {y + 44}Z" fill="{on}"/>',
              _r(x + 24, y + 60, 24, 6, INK, 0)]
    elif name == "folder":  # un agente es una carpeta
        o += [f'<path d="M{x + 4} {y + 14}H{x + 28}L{x + 34} {y + 22}H{x + 68}V{y + 64}H{x + 4}Z" fill="{PALE}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>',
              _r(x + 14, y + 6, 30, 40, PAPER, 1.6), _r(x + 26, y + 10, 30, 40, PAPER, 1.6),
              _r(x + 4, y + 30, 64, 34, f)]
    elif name == "loop":  # el núcleo hace girar el bucle
        o += [_r(x + 4, y + 4, 64, 64, f),
              f'<path d="M{x + 22} {y + 44}A15 15 0 1 1 {x + 50} {y + 44}" fill="none" stroke="{on}" stroke-width="4" stroke-linecap="round"/>',
              f'<path d="M{x + 50} {y + 36}L{x + 52} {y + 47}L{x + 41} {y + 46}Z" fill="{on}"/>']
    elif name == "shield":  # las políticas deciden
        o += [f'<path d="M{x + 36} {y + 4}L{x + 64} {y + 14}V{y + 34}Q{x + 64} {y + 58} {x + 36} {y + 68}Q{x + 8} {y + 58} {x + 8} {y + 34}V{y + 14}Z" '
              f'fill="{f}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>',
              f'<path d="M{x + 24} {y + 36}L{x + 33} {y + 45}L{x + 49} {y + 27}" fill="none" stroke="{on}" stroke-width="4" '
              f'stroke-linecap="round" stroke-linejoin="round"/>']
    elif name == "models":  # cualquier modelo: capas intercambiables
        for i in range(3):
            o.append(_r(x + 6 + i * 4, y + 44 - i * 18, 56, 14, f if i == 2 else PAPER))
    elif name == "pad":  # eliges una de ocho direcciones
        for i in range(3):
            for j in range(3):
                o.append(_r(x + 4 + i * 22, y + 4 + j * 22, 20, 20, PALE if (i, j) == (2, 1) else PAPER, 1.6))
        o.append(_arrow(x + 49, y + 37, x + 66, INK, 3))
    elif name == "tide":  # todas las piezas responden a la vez
        for i, (kind, fill) in enumerate((("rook", PAPER), ("king", INK), ("pawn", PAPER))):
            yy = y + 22 + i * 22
            o.append(_arrow(x + 4, yy - 6, x + 30, INK, 3))
            o.append(_piece(x + 46 + (i % 2) * 10, yy + 2, kind, 22, fill))
    elif name == "versus":  # IA contra IA
        o += [_piece(x + 20, y + 62, "king", 44, PAPER), _piece(x + 52, y + 62, "king", 44, INK)]
    elif name == "bars":  # lo medido: tablas antes y después
        o += [f'<g class="grow">{_r(x + 8, y + 6, 24, 60, PALE)}</g>',
              f'<g class="grow" style="animation-delay:.3s">{_r(x + 40, y + 47, 24, 19, f)}</g>',
              f'<line x1="{x + 2}" y1="{y + 66}" x2="{x + 70}" y2="{y + 66}" stroke="{INK}" stroke-width="{SW}"/>']
    return "".join(o)
