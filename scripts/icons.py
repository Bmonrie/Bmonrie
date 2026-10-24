"""Glifos de 24 × 24 en trazo, para las fichas de tarjetas y pasos de los diagramas."""


# ─── Glifos (24 × 24, trazo) ─────────────────────────────────────────────────
_G = {
    "browser": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9H22"/><circle cx="5.5" cy="6.5" r=".6"/><circle cx="8" cy="6.5" r=".6"/>',
    "cloud": '<path d="M7 19H17.5A4.5 4.5 0 0 0 17.5 10A5.5 5.5 0 0 0 7 8.8A5.1 5.1 0 0 0 7 19Z"/>',
    "proxy": '<path d="M3 8H19M15 4L19 8L15 12M21 16H5M9 12L5 16L9 20"/>',
    "code": '<path d="M8 6L2.5 12L8 18M16 6L21.5 12L16 18M13.5 4L10.5 20"/>',
    "db": '<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5V18.5A8 3 0 0 0 20 18.5V5.5M4 12A8 3 0 0 0 20 12"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5V5.5M12 18.5V21.5M2.5 12H5.5M18.5 12H21.5M5.3 5.3L7.4 7.4M16.6 16.6L18.7 18.7M5.3 18.7L7.4 16.6M16.6 7.4L18.7 5.3"/><circle cx="12" cy="12" r="6.5"/>',
    "file": '<path d="M6 2.5H14L19 7.5V21.5H6Z"/><path d="M14 2.5V7.5H19M9 12H16M9 16H16"/>',
    "layers": '<path d="M12 3L21.5 8L12 13L2.5 8Z"/><path d="M2.5 12.5L12 17.5L21.5 12.5M2.5 17L12 22L21.5 17"/>',
    "clock": '<circle cx="12" cy="12" r="9.5"/><path d="M12 6.5V12L15.5 14.5"/>',
    "film": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M10 9.5L15 12L10 14.5Z"/>',
    "play": '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="M10 9L15.5 12L10 15Z"/>',
    "ledger": '<rect x="4" y="2.5" width="16" height="19" rx="2"/><path d="M8 8L9.5 9.5L12 7M8 13L9.5 14.5L12 12M14 8.5H17M14 13.5H17M8 18H17"/>',
    "chart": '<path d="M3 21H21M6.5 21V12M12 21V5M17.5 21V15"/>',
    "board": '<rect x="3" y="3" width="18" height="18"/><path d="M3 12H21M12 3V21"/><path d="M3 3H12V12H3ZM12 12H21V21H12Z" fill="currentColor" stroke="none" opacity=".35"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21A8 7 0 0 1 20 21"/>',
    "monitor": '<rect x="2.5" y="3.5" width="19" height="13" rx="1.5"/><path d="M8.5 21H15.5M12 16.5V21"/>',
    "terminal": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M6.5 9L9.5 12L6.5 15M12 15H17"/>',
    "plug": '<path d="M9 2.5V7.5M15 2.5V7.5M6 7.5H18V11.5A6 6 0 0 1 6 11.5Z"/><path d="M12 17.5V21.5"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9.5 2.5V6M14.5 2.5V6M9.5 18V21.5M14.5 18V21.5M2.5 9.5H6M2.5 14.5H6M18 9.5H21.5M18 14.5H21.5"/>',
    "shield": '<path d="M12 2.5L20 5.5V11.5Q20 18 12 21.5Q4 18 4 11.5V5.5Z"/><path d="M8.5 12L11 14.5L15.5 9.5"/>',
    "bookmark": '<path d="M6 2.5H18V21.5L12 17L6 21.5Z"/>',
    "agents": '<circle cx="6" cy="7" r="3"/><circle cx="18" cy="7" r="3"/><circle cx="12" cy="18" r="3"/><path d="M8.5 8.7L10.6 15.6M15.5 8.7L13.4 15.6M9 7H15"/>',
    "cube": '<path d="M12 2.5L21 7.5V16.5L12 21.5L3 16.5V7.5Z"/><path d="M3 7.5L12 12.5L21 7.5M12 12.5V21.5"/>',
    "grid": '<rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M3 9H21M3 15H21M9 3V21M15 3V21"/>',
    "loop": '<path d="M20 12A8 8 0 0 1 6 17.3M4 12A8 8 0 0 1 18 6.7"/><path d="M18 2.5V6.7H13.8M6 21.5V17.3H10.2"/>',
    "gamepad": '<rect x="2.5" y="7" width="19" height="11" rx="5.5"/><path d="M7 10.5V14.5M5 12.5H9"/><circle cx="15.5" cy="11.5" r=".9"/><circle cx="17.5" cy="13.8" r=".9"/>',
    "spark": '<path d="M12 2.5L14 10L21.5 12L14 14L12 21.5L10 14L2.5 12L10 10Z"/>',
    "server": '<rect x="3" y="3.5" width="18" height="7" rx="1.5"/><rect x="3" y="13.5" width="18" height="7" rx="1.5"/><path d="M7 7H7.5M7 17H7.5"/>',
    "pulse": '<path d="M2.5 12H7L10 5L14 19L17 12H21.5"/>',
    "book": '<path d="M5 4.5A2 2 0 0 1 7 2.5H19V18.5H7A2 2 0 0 0 5 20.5Z"/><path d="M5 20.5A2 2 0 0 0 7 22.5H19"/>',
    "tool": '<path d="M14.5 3.5A5 5 0 0 0 9.8 10.3L3.5 16.6A2.1 2.1 0 0 0 6.4 19.5L12.7 13.2A5 5 0 0 0 19.5 8.5L16.5 11.5L13.5 10.5L12.5 7.5Z"/>',
    "git": '<circle cx="6" cy="5" r="2.5"/><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="8" r="2.5"/><path d="M6 7.5V16.5M18 10.5Q18 15 8.5 17.5"/>',
    "check": '<circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5L10.5 15.5L16.5 9"/>',
    "package": '<path d="M12 2.5L21 7V17L12 21.5L3 17V7Z"/><path d="M3 7L12 11.5L21 7M12 11.5V21.5M7.5 4.8L16.5 9.3"/>',
    "swap": '<path d="M3 8H18M14 4L18 8L14 12M21 16H6M10 12L6 16L10 20"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20A6.5 6 0 0 1 15.5 20"/><path d="M16 4.6A3.5 3.5 0 0 1 16 11.4M18.5 14.2A6.5 6 0 0 1 21.5 20"/>',
}


def glyph(name, x, y, color, size=24, sw=1.8):
    """Un glifo de 24 × 24 con su esquina en (x, y), en el color pedido."""
    k = size / 24
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.3f})" fill="none" stroke="{color}" color="{color}" '
            f'stroke-width="{sw / k:.2f}" stroke-linecap="round" stroke-linejoin="round">{_G[name]}</g>')
