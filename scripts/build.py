#!/usr/bin/env python3
"""Genera el README de perfil de Bmonrie: sobrio y en los azules del perfil del trabajo.

Una cabecera (nombre, cargo, una frase y tres capacidades), el carrusel de tecnologías, una tarjeta por
proyecto (qué es, tres datos, tecnologías, enlace y su maqueta en un marco de dispositivo) con su
arquitectura plegada debajo, y una franja de contacto. Todo está dibujado en código; nada es una captura.
Cada lámina tiene versión de escritorio (assets/) y de teléfono (assets/m/), y el README elige con
<picture>. Inglés primero (README.md), luego español y catalán.

Uso:
    python scripts/build.py            # intenta leer el último Short del canal; si no hay red, usa data/
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import diagrams  # noqa: E402
import mockups  # noqa: E402
from content import PROJECTS, TXT  # noqa: E402
from kit import BLUE, INK, M, MUTED, PAPER, PM, PW, ROOT, STONE, W, block, esc, set_charset, svg, text, width  # noqa: E402

ASSETS = ROOT / "assets"
LATEST = ROOT / "data" / "latest-short.json"
LINKEDIN = ("https://www.linkedin.com/in/brunomonrealpujol", "linkedin.com/in/brunomonrealpujol")
FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=UCnFyMu7pAiblj8aV138ehsg"
CAP = 0.686  # altura de mayúscula de Archivo
EDGE = "#A9C4E4"  # borde fino de marcos y tarjetas
TECH = ["Python", "TypeScript", "FastAPI", "LangGraph", "MCP", "RAG", "pgvector", "PostgreSQL", "vLLM", "Next.js",
        "React", "Remotion", "ONNX Runtime", "FSRS", "Stockfish", "Docker", "GitHub Actions", "OpenTelemetry",
        "Langfuse", "Cloudflare"]
SCREEN = 600  # alto visible de una maqueta dentro de su marco


# ─── El último Short, para que la página cambie sola ────────────────────────
def latest_short():
    try:
        with urllib.request.urlopen(FEED, timeout=15) as r:
            root = ET.fromstring(r.read())
        ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
        e = root.find("a:entry", ns)
        data = {"title": e.find("a:title", ns).text, "published": e.find("a:published", ns).text[:10],
                "videoId": e.find("yt:videoId", ns).text}
        LATEST.parent.mkdir(exist_ok=True)
        LATEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return data
    except Exception:  # sin red: lo último que se guardó
        return json.loads(LATEST.read_text(encoding="utf-8"))


SHORT = latest_short()


# ─── Piezas ──────────────────────────────────────────────────────────────────
def geo(phone):
    """Ancho, margen y medida de la lámina."""
    return (PW, PM, PW - 2 * PM) if phone else (W, M, W - 2 * M)


def arrow(x, y, color, s=10):
    return (f'<path d="M{x:.1f} {y:.1f}L{x + s:.1f} {y - s:.1f}M{x + 2:.1f} {y - s:.1f}H{x + s:.1f}V{y - 2:.1f}" '
            f'stroke="{color}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')


def bullets(x, y, items, size, maxw, gap=12):
    """Lista con un cuadradito azul por punto."""
    out = []
    for it in items:
        out.append(f'<rect x="{x:.1f}" y="{y - size * 0.62:.1f}" width="8" height="8" rx="1.5" fill="{BLUE}"/>')
        t, y = block(x + 22, y, it, size, maxw - 22, INK, 400, lead=1.42)
        out.append(t)
        y += gap
    return "".join(out), y - gap


def mock_frame(p, P, x, y, phone):
    """La maqueta del producto dentro de un marco fino de dispositivo (el Short ya es un teléfono)."""
    fn = getattr(mockups, p["key"])
    body, mw, mh = fn(dict(mock=P["mock"] | ({"title": SHORT["title"]} if p["key"] == "blunderling" else {})))
    if p["key"] == "blunderling":
        col = 360 if phone else 384
        return f'<g transform="translate({x + (col - mw) / 2:.1f} {y:.1f})">{body}</g>', mh
    sh = min(mh, SCREEN)
    cid = f'clip-{p["key"]}-{"m" if phone else "d"}'
    if phone:  # en teléfono, sin bisel: la maqueta a su tamaño, en un marco redondeado
        clip = f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{mw}" height="{sh}" rx="22"/></clipPath>'
        return (f'<defs>{clip}</defs><g clip-path="url(#{cid})"><rect x="{x:.1f}" y="{y:.1f}" width="{mw}" height="{sh}" fill="{PAPER}"/>'
                f'<g transform="translate({x:.1f} {y:.1f})">{body}</g></g>'
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{mw}" height="{sh}" rx="22" fill="none" stroke="{EDGE}" stroke-width="1.6"/>'), sh
    bz = 12
    clip = f'<clipPath id="{cid}"><rect x="{x + bz:.1f}" y="{y + bz:.1f}" width="{mw}" height="{sh}" rx="24"/></clipPath>'
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{mw + 2 * bz}" height="{sh + 2 * bz}" rx="36" fill="{STONE}" stroke="{EDGE}" stroke-width="1.6"/>'
            f'<defs>{clip}</defs><g clip-path="url(#{cid})"><rect x="{x + bz:.1f}" y="{y + bz:.1f}" width="{mw}" height="{sh}" fill="{PAPER}"/>'
            f'<g transform="translate({x + bz:.1f} {y + bz:.1f})">{body}</g></g>'), sh + 2 * bz


# ─── Láminas ─────────────────────────────────────────────────────────────────
def header(lang, phone=False):
    L = TXT[lang]
    w, m, cw = geo(phone)
    size = 40 if phone else 64
    y = (36 if phone else 56) + size * CAP
    b = [text(m - 2, y, '<tspan>Bruno Monreal</tspan><tspan fill="' + BLUE + '">.</tspan>', size, INK, 700,
              track=-0.02, raw=True)]
    y += 34 if phone else 46
    t, y = block(m, y, L["role"], 18 if phone else 22, cw, BLUE, 600, lead=1.35)
    b.append(t)
    t, y = block(m, y + (10 if phone else 16), L["intro"], 19 if phone else 22, cw if phone else 780, INK, 400, lead=1.5)
    b.append(t)
    y += 12 if phone else 18
    x = m
    for cap in L["caps"]:
        cw_ = width(cap, 19, 600)
        if not phone and x != m and x + cw_ + 22 > w - m:
            x, y = m, y + 32
        b.append(f'<rect x="{x:.1f}" y="{y - 12:.1f}" width="9" height="9" rx="1.5" fill="{BLUE}"/>'
                 + text(x + 20, y, cap, 19, INK, 600))
        if phone:
            y += 32
        else:
            x += 20 + cw_ + 36
    end = (y - 32 if phone else y) + (36 if phone else 52)
    return svg(end, "".join(b), f'Bruno Monreal. {L["role"]}. {L["intro"]}', PAPER, w)


def marquee():
    """El carrusel: las tecnologías pasan en bucle, discretas."""
    H = 84
    parts, x = [], 0.0
    for t in TECH:
        parts.append(text(x, 56, t, 40, INK, 500, track=-0.01))
        x += width(t, 40, 500, track=-0.01) + 26
        parts.append(f'<rect x="{x:.1f}" y="38" width="9" height="9" rx="1.5" fill="{BLUE}"/>')
        x += 9 + 26
    row = "".join(parts)
    copies = int(W / x) + 2
    track = "".join(f'<g transform="translate({x * k:.1f} 0)">{row}</g>' for k in range(copies))
    css = (f"<style>.track{{animation:slide {x / 40:.1f}s linear infinite}}"
           f"@keyframes slide{{to{{transform:translateX(-{x:.1f}px)}}}}</style>")
    return svg(H, css + f'<g class="track">{track}</g>', TXT["en"]["alt_marquee"], STONE)


def card(lang, p, phone=False):
    """La tarjeta del proyecto: el texto a un lado y la maqueta al otro (debajo, en teléfono)."""
    L, P = TXT[lang], p[lang]
    w, m, cw = geo(phone)
    tw = cw if phone else 440
    y = (36 if phone else 56) + (30 if phone else 36) * CAP
    b = [text(m, y, p["name"], 30 if phone else 36, INK, 700, track=-0.01)]
    t, y = block(m, y + (30 if phone else 36), P["type"], 18 if phone else 19, tw, BLUE, 600, lead=1.35)
    b.append(t)
    t, y = block(m, y + 8, P["desc"], 19 if phone else 20, tw, INK, 400, lead=1.5)
    b.append(t)
    t, y = bullets(m, y + 16, P["facts"], 19, tw)
    b.append(t)
    t, y = block(m, y + 22, f'{L["built"]} {p["stack"]}', 18, tw, MUTED, 500, lead=1.4)
    b.append(t)
    y += 14
    if p["link"]:
        lab = p["link"][1]
        b.append(text(m, y, lab, 20, BLUE, 700) + arrow(m + width(lab, 20, 700) + 10, y - 3, BLUE))
    else:
        b.append(text(m, y, L["private"], 20, MUTED, 600))
    text_end = y + 10
    if phone:
        frame, fh = mock_frame(p, P, m, text_end + 30, True)
        end = text_end + 30 + fh + 36
    else:  # el texto, centrado en vertical frente a la maqueta
        frame, fh = mock_frame(p, P, w - m - 384, 48, False)
        top = 56
        shift = max(0, (48 + fh / 2) - (top + (text_end - top) / 2))
        b = [f'<g transform="translate(0 {shift:.1f})">{"".join(b)}</g>']
        end = max(text_end + shift + 48, 48 + fh + 48)
    b.append(frame)
    alt = f'{p["name"]}. {P["type"]}. {P["desc"]} ' + " ".join(P["facts"])
    return svg(end, "".join(b), alt, PAPER, w)


def arch(lang, p, phone=False):
    """La arquitectura, que el README muestra plegada bajo la tarjeta."""
    L, P = TXT[lang], p[lang]
    w, m, cw = geo(phone)
    d, dh = getattr(diagrams, p["key"])(dict(arch=P["arch"], legend=L["legend"]), phone)
    top = 28 if phone else 44
    b = [f'<g transform="translate({m} {top})">{d}</g>']
    c, y = block(m, top + dh + 34, P["arch_caption"], 18 if phone else 19, cw, MUTED, 500, lead=1.4)
    b.append(c)
    return svg(y + (12 if phone else 24), "".join(b), f'{p["name"]}. {P["arch_caption"]}', PAPER, w)


def contact(lang, phone=False):
    L = TXT[lang]
    w, m, cw = geo(phone)
    t, y = block(m, 52 if phone else 72, L["contact"], 24 if phone else 32, cw, INK, 700, lead=1.25)
    lab = LINKEDIN[1]
    sz, wg = (18, 600) if phone else (20, 700)
    b = [t, text(m, y + 10, lab, sz, BLUE, wg) + arrow(m + width(lab, sz, wg) + 10, y + 7, BLUE, 9)]
    return svg(y + (40 if phone else 56), "".join(b), f'{L["contact"]} LinkedIn: {lab}', STONE, w)


# ─── README ──────────────────────────────────────────────────────────────────
FILES = {"en": "README.md", "es": "README.es.md", "ca": "README.ca.md"}
PHONE_QUERY = "(max-width: 640px)"


def readme(lang):
    L = TXT[lang]

    def pic(name, alt, href=None):
        tag = (f'<picture><source media="{PHONE_QUERY}" srcset="assets/m/{name}">'
               f'<img src="assets/{name}" width="100%" alt="{esc(alt)}" /></picture>')
        return f'<a href="{href}">{tag}</a>' if href else tag

    langs = " · ".join(f"<b>{TXT[c]['name']}</b>" if c == lang else f'<a href="{FILES[c]}">{TXT[c]["name"]}</a>' for c in TXT)
    body = [f'<p align="right">{langs}</p>',
            pic(f"header-{lang}.svg", f'Bruno Monreal. {L["role"]}. {L["intro"]}'),
            f'<img src="assets/marquee.svg" width="100%" alt="{esc(L["alt_marquee"])}" />']
    for p in PROJECTS:
        href = p["link"][0] if p["link"] else None
        body.append(pic(f'{p["key"]}-{lang}.svg', f'{p["name"]}. {p[lang]["desc"]}', href))
        body.append(f'<details>\n<summary><b>{p["name"]}</b> · {L["how"]}</summary>\n\n'
                    + pic(f'{p["key"]}-arch-{lang}.svg', f'{p["name"]}. {p[lang]["arch_caption"]}') + "\n\n</details>")
    body.append(pic(f"contact-{lang}.svg", L["contact"], LINKEDIN[0]))
    (ROOT / FILES[lang]).write_text("\n\n".join(body) + "\n", encoding="utf-8")


def _all_text():
    def walk(v):
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            return "".join(walk(x) for x in v.values())
        if isinstance(v, (list, tuple)):
            return "".join(walk(x) for x in v)
        return ""
    return walk([TXT, PROJECTS, LINKEDIN, TECH]) + SHORT["title"] + "Bruno Monreal."


def main():
    set_charset(_all_text())
    (ASSETS / "m").mkdir(parents=True, exist_ok=True)
    for old in list(ASSETS.glob("*.svg")) + list((ASSETS / "m").glob("*.svg")):
        old.unlink()
    out = {"marquee.svg": marquee()}
    for lang in TXT:
        for phone in (False, True):
            d = "m/" if phone else ""
            out[f"{d}header-{lang}.svg"] = header(lang, phone)
            for p in PROJECTS:
                out[f'{d}{p["key"]}-{lang}.svg'] = card(lang, p, phone)
                out[f'{d}{p["key"]}-arch-{lang}.svg'] = arch(lang, p, phone)
            out[f"{d}contact-{lang}.svg"] = contact(lang, phone)
        readme(lang)
    for name, content in out.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"{len(out)} SVGs · último Short: {SHORT['title']}")


if __name__ == "__main__":
    main()
