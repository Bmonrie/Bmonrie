"""Dibujo isométrico para las figuras explicativas.

Un solo estilo para todas: contorno de tinta de grosor fijo, caras planas en tres tonos (la de arriba
la más clara) y el azul reservado para la pieza que hace funcionar el sistema.

Ejes: x baja hacia la derecha, y baja hacia la izquierda, z sube. Se ven la cara de arriba, la de
delante a la izquierda (plano y = y + d) y la de delante a la derecha (plano x = x + w). El orden de
pintado es cosa de quien dibuja: de atrás (x + y pequeño) hacia delante.
"""
import math

from kit import BLUE, INK

C30 = math.cos(math.radians(30))
SW = 2.2  # contorno
SW_FINE = 1.4  # detalle

# Tonos (arriba, delante-izquierda, delante-derecha)
WHITE = ("#FFFFFF", "#E7F3F5", "#C9DFF2")
FLOOR = ("#F4F9FB", "#DCEBF5", "#C2D8EC")
ACCENT = (BLUE, "#005FAD", "#004C8C")
DARK = ("#2B3199", "#171C8F", "#10146B")
GREY = ("#C9DFF2", "#A8C7E3", "#8DB3D6")


def _pts(points):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in points)


class Iso:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return (self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s - z * self.s)

    def poly(self, pts, fill, sw=SW, stroke=INK):
        return (f'<polygon points="{_pts(self.p(*q) for q in pts)}" fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{sw}" stroke-linejoin="round"/>')

    def line(self, a, b, sw=SW_FINE, stroke=INK, dash=None):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
                f'stroke-width="{sw}" stroke-linecap="round"{d}/>')

    def box(self, x, y, z, w, d, h, tone=WHITE, sw=SW):
        t, l, r = tone
        return (self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], l, sw)
                + self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], r, sw)
                + self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], t, sw))

    def top_grid(self, x, y, z, w, d, n, m, fills, sw=SW_FINE):
        """Cuadrícula sobre un plano horizontal (tablero de ajedrez, celdas)."""
        out = []
        cw, cd = w / n, d / m
        for i in range(n):
            for j in range(m):
                xx, yy = x + i * cw, y + j * cd
                out.append(self.poly([(xx, yy, z), (xx + cw, yy, z), (xx + cw, yy + cd, z), (xx, yy + cd, z)],
                                     fills[(i + j) % len(fills)], sw))
        return "".join(out)

    def cyl(self, cx, cy, z, r, h, tone=WHITE, sw=SW, bands=0):
        t, l, _ = tone
        tx, ty = self.p(cx, cy, z + h)
        _, by = self.p(cx, cy, z)
        rx, ry = r * self.s * C30 * math.sqrt(2), r * self.s * 0.5 * math.sqrt(2)
        out = [f'<path d="M{tx - rx:.1f} {ty:.1f}V{by:.1f}A{rx:.1f} {ry:.1f} 0 0 0 {tx + rx:.1f} {by:.1f}V{ty:.1f}Z" '
               f'fill="{l}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>']
        for k in range(1, bands + 1):
            yy = ty + (by - ty) * k / (bands + 1)
            out.append(f'<path d="M{tx - rx:.1f} {yy:.1f}A{rx:.1f} {ry:.1f} 0 0 0 {tx + rx:.1f} {yy:.1f}" '
                       f'fill="none" stroke="{INK}" stroke-width="{SW_FINE}"/>')
        out.append(f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{t}" '
                   f'stroke="{INK}" stroke-width="{sw}"/>')
        return "".join(out)

    def arrow(self, a, b, z=0.0, w=0.26, head=0.7, fill=INK, sw=0):
        """Flecha plana sobre el plano z, de a=(x, y) a b=(x, y)."""
        (x1, y1), (x2, y2) = a, b
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy, ux
        qx, qy = x2 - ux * head, y2 - uy * head
        hw = w / 2
        pts = [(x1 + nx * hw, y1 + ny * hw), (qx + nx * hw, qy + ny * hw), (qx + nx * head * 0.62, qy + ny * head * 0.62),
               (x2, y2), (qx - nx * head * 0.62, qy - ny * head * 0.62), (qx - nx * hw, qy - ny * hw),
               (x1 - nx * hw, y1 - ny * hw)]
        st = f' stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
        return f'<polygon points="{_pts(self.p(px, py, z) for px, py in pts)}" fill="{fill}"{st}/>'

    def panel_y(self, x, y, z, w, h, fill, sw=SW_FINE):
        """Rectángulo sobre el plano vertical y = const (cara delantera izquierda)."""
        return self.poly([(x, y, z), (x + w, y, z), (x + w, y, z + h), (x, y, z + h)], fill, sw)

    def panel_x(self, x, y, z, d, h, fill, sw=SW_FINE):
        """Rectángulo sobre el plano vertical x = const (cara delantera derecha)."""
        return self.poly([(x, y, z), (x, y + d, z), (x, y + d, z + h), (x, y, z + h)], fill, sw)

    def matrix_y(self, x, y, z):
        """Transformación que lleva coordenadas locales (u a la derecha, v hacia abajo, en unidades)
        al plano y = const con origen en (x, y, z)."""
        ox, oy = self.p(x, y, z)
        s = self.s
        return f"matrix({C30 * s:.3f} {0.5 * s:.3f} 0 {s:.3f} {ox:.1f} {oy:.1f})"

    def matrix_x(self, x, y, z):
        """Igual, para el plano x = const: se lee hacia -y, que en pantalla va a la derecha."""
        ox, oy = self.p(x, y, z)
        s = self.s
        return f"matrix({C30 * s:.3f} {-0.5 * s:.3f} 0 {s:.3f} {ox:.1f} {oy:.1f})"

    def matrix_top(self, x, y, z):
        ox, oy = self.p(x, y, z)
        s = self.s
        return f"matrix({C30 * s:.3f} {0.5 * s:.3f} {-C30 * s:.3f} {0.5 * s:.3f} {ox:.1f} {oy:.1f})"


# Siluetas planas de piezas, base en (0, 0), alto 1. Se dibujan de pie sobre su casilla.
PIECES = {
    "rook": "M-0.30 0H0.30V-0.10H0.22L0.18 -0.62H0.26V-0.86H0.16V-0.76H0.06V-0.86H-0.06V-0.76H-0.16V-0.86H-0.26V-0.62H-0.18L-0.22 -0.10H-0.30Z",
    "king": "M-0.30 0H0.30V-0.10H0.20L0.24 -0.58Q0.24 -0.70 0.06 -0.72V-0.80H0.14V-0.88H0.06V-0.96H-0.06V-0.88H-0.14V-0.80H-0.06V-0.72Q-0.24 -0.70 -0.24 -0.58L-0.20 -0.10H-0.30Z",
    "pawn": "M-0.28 0H0.28V-0.10H0.17L0.11 -0.48A0.17 0.17 0 1 0 -0.11 -0.48L-0.17 -0.10H-0.28Z",
    "bishop": "M-0.28 0H0.28V-0.10H0.17L0.13 -0.52Q0.24 -0.66 0 -0.90Q-0.24 -0.66 -0.13 -0.52L-0.17 -0.10H-0.28Z",
    "queen": "M-0.30 0H0.30V-0.10H0.20L0.30 -0.74L0.12 -0.46L0.10 -0.86L0 -0.50L-0.10 -0.86L-0.12 -0.46L-0.30 -0.74L-0.20 -0.10H-0.30Z",
    "knight": "M-0.30 0H0.30V-0.10H0.22Q0.26 -0.50 0.16 -0.72Q0.04 -0.92 -0.14 -0.90L-0.18 -0.98L-0.24 -0.84Q-0.34 -0.72 -0.30 -0.58L-0.20 -0.52Q-0.10 -0.60 -0.02 -0.56Q-0.20 -0.36 -0.20 -0.10H-0.30Z",
}


def piece(px, py, kind, size, fill, stroke=INK):
    return (f'<path d="{PIECES[kind]}" transform="translate({px:.1f} {py:.1f}) scale({size:.1f})" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{SW / size:.4f}" stroke-linejoin="round"/>')
