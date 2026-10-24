#!/usr/bin/env python3
"""Genera el README de perfil de Bmonrie: láminas SVG (ES/CA/EN) con lo que sé hacer y los
proyectos que lo demuestran.

Dirección de arte: «Eixample», la misma que el perfil del trabajo. El chaflán a 45° de las
manzanas de Cerdà es el único tratamiento de esquina; campos de color planos con bordes duros;
una sola familia (Archivo, variable en peso y anchura). La paleta es propia: grafito, piedra
y un acento terracota, sin los colores de ninguna empresa.

Todo el texto vive en TXT y PROJECTS. Si cambio de trabajo, solo cambia «now».

Uso:
    python scripts/build.py
"""
import base64
import io
import math
import string
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = ROOT / "scripts" / "fonts" / "archivo.woff2"
REPO_URL = "https://github.com/Bmonrie/Bmonrie/blob/main"
LINKEDIN = ("https://www.linkedin.com/in/brunomonrealpujol", "linkedin.com/in/brunomonrealpujol")

# ─── Paleta propia: campos planos, un solo acento ────────────────────────────
WHITE, INK, MUTED = "#FFFFFF", "#1B1B1F", "#5B5F66"
ACCENT, SOFT, TINT, PALE = "#C63D22", "#F08A6C", "#F4EFE8", "#E6DCD2"
ON_INK, ON_INK_SOFT = "#D9D6D0", "#A8A39C"  # texto secundario sobre el campo grafito
EASE = "cubic-bezier(.16,1,.3,1)"
M = 40  # margen de lámina
CUT = 28  # chaflán

# ─── Textos ──────────────────────────────────────────────────────────────────
TXT = {
    "es": dict(
        name="Español",
        lead="AI Engineer en Barcelona.",
        sub="Construyo agentes, productos y automatizaciones con LLMs, y los llevo hasta producción.",
        can_title="Lo que sé hacer",
        can=[
            ("Agentes de IA fiables", "Orquestación, herramientas, RAG y evaluaciones."),
            ("Producto de punta a punta", "Backend, interfaz, datos y despliegue."),
            ("Automatización desatendida", "Pipelines que publican solos, cada día."),
            ("Decisiones con datos", "Simular y medir antes de opinar."),
        ],
        about_title="IA que funciona cada día, no solo en la demo.",
        about=(
            "Trabajo donde los LLMs se encuentran con el software de verdad: agentes que usan herramientas "
            "con permisos claros, búsqueda sobre documentos, evaluaciones y la infraestructura que los sostiene. "
            "Fuera del trabajo construyo productos completos para llevar las ideas hasta el final."
        ),
        now_title="Ahora",
        now="AI & Data Manager en Forvis Mazars.",
        how_title="Cómo trabajo",
        how=[
            "El código orquesta; el LLM solo razona.",
            "Si no está medido, es una opinión.",
            "Lo que se repite, se automatiza.",
            "Mejor aburrido de mantener que brillante una vez.",
        ],
        projects_title="Proyectos que lo demuestran",
        projects_sub="Cuatro proyectos personales, cada uno con una capacidad detrás.",
        private="Repositorio privado",
        footer="Hablemos de lo que quieres construir.",
        alt_hero=("Bruno Monreal, AI Engineer en Barcelona. Lo que sé hacer: agentes de IA fiables, producto "
                  "de punta a punta, automatización desatendida y decisiones con datos."),
        alt_marquee="Tecnologías: Python, TypeScript, FastAPI, MCP, RAG, PostgreSQL, React, Docker…",
        alt_about="Sobre mí y cómo trabajo",
        alt_footer="Hablemos de lo que quieres construir: mi LinkedIn",
    ),
    "ca": dict(
        name="Català",
        lead="AI Engineer a Barcelona.",
        sub="Construeixo agents, productes i automatitzacions amb LLMs, i els porto fins a producció.",
        can_title="El que sé fer",
        can=[
            ("Agents d'IA fiables", "Orquestració, eines, RAG i avaluacions."),
            ("Producte de cap a cap", "Backend, interfície, dades i desplegament."),
            ("Automatització desatesa", "Pipelines que publiquen sols, cada dia."),
            ("Decisions amb dades", "Simular i mesurar abans d'opinar."),
        ],
        about_title="IA que funciona cada dia, no només a la demo.",
        about=(
            "Treballo on els LLMs es troben amb el programari de veritat: agents que fan servir eines amb "
            "permisos clars, cerca sobre documents, avaluacions i la infraestructura que els sosté. "
            "Fora de la feina construeixo productes sencers per portar les idees fins al final."
        ),
        now_title="Ara",
        now="AI & Data Manager a Forvis Mazars.",
        how_title="Com treballo",
        how=[
            "El codi orquestra; el LLM només raona.",
            "Si no està mesurat, és una opinió.",
            "El que es repeteix, s'automatitza.",
            "Millor avorrit de mantenir que brillant un cop.",
        ],
        projects_title="Projectes que ho demostren",
        projects_sub="Quatre projectes personals, cadascun amb una capacitat al darrere.",
        private="Repositori privat",
        footer="Parlem del que vols construir.",
        alt_hero=("Bruno Monreal, AI Engineer a Barcelona. El que sé fer: agents d'IA fiables, producte de cap "
                  "a cap, automatització desatesa i decisions amb dades."),
        alt_marquee="Tecnologies: Python, TypeScript, FastAPI, MCP, RAG, PostgreSQL, React, Docker…",
        alt_about="Sobre mi i com treballo",
        alt_footer="Parlem del que vols construir: el meu LinkedIn",
    ),
    "en": dict(
        name="English",
        lead="AI Engineer in Barcelona.",
        sub="I build agents, products and automations with LLMs, and I take them all the way to production.",
        can_title="What I do",
        can=[
            ("Reliable AI agents", "Orchestration, tools, RAG and evals."),
            ("End-to-end product", "Backend, interface, data and deployment."),
            ("Unattended automation", "Pipelines that ship on their own, every day."),
            ("Data-driven decisions", "Simulate and measure before having an opinion."),
        ],
        about_title="AI that works every day, not just in the demo.",
        about=(
            "I work where LLMs meet real software: agents that use tools with clear permissions, search over "
            "documents, evaluations and the infrastructure that holds it all up. Outside work I build complete "
            "products to take ideas all the way."
        ),
        now_title="Now",
        now="AI & Data Manager at Forvis Mazars.",
        how_title="How I work",
        how=[
            "Code orchestrates; the LLM only reasons.",
            "If it isn't measured, it's an opinion.",
            "If it repeats, it gets automated.",
            "Boring to maintain beats brilliant once.",
        ],
        projects_title="Projects that prove it",
        projects_sub="Four personal projects, each with a capability behind it.",
        private="Private repository",
        footer="Let's talk about what you want to build.",
        alt_hero=("Bruno Monreal, AI Engineer in Barcelona. What I do: reliable AI agents, end-to-end product, "
                  "unattended automation and data-driven decisions."),
        alt_marquee="Tech: Python, TypeScript, FastAPI, MCP, RAG, PostgreSQL, React, Docker…",
        alt_about="About me and how I work",
        alt_footer="Let's talk about what you want to build: my LinkedIn",
    ),
}

# Cada proyecto demuestra una capacidad de TXT[lang]["can"] (índice «cap»).
PROJECTS = [
    dict(
        key="agents", cap=0, name="Template_Agents", link=None,
        tech=["Python", "FastAPI", "PostgreSQL", "pgvector", "MCP", "Next.js", "OpenTelemetry"],
        es=dict(
            kicker="Base de producción para agentes conversacionales.",
            body=("Un núcleo sin SDKs de proveedor: el código orquesta y el LLM solo razona. Un agente nuevo "
                  "es una carpeta de datos (YAML, prompt, herramientas y evals), no código nuevo."),
            points=[
                "Cualquier modelo: Anthropic, OpenAI, Azure, vLLM u Ollama, con fallback entre proveedores.",
                "Herramientas y servidores MCP bajo políticas deterministas, con aprobación humana.",
                "Ejecuciones duraderas: checkpoint en cada paso y, si cae una réplica, otra la retoma.",
                "RAG híbrido con citas, memoria por usuario, multi-tenant con RLS y evals con usuario simulado.",
            ],
        ),
        ca=dict(
            kicker="Base de producció per a agents conversacionals.",
            body=("Un nucli sense SDKs de proveïdor: el codi orquestra i el LLM només raona. Un agent nou és "
                  "una carpeta de dades (YAML, prompt, eines i evals), no codi nou."),
            points=[
                "Qualsevol model: Anthropic, OpenAI, Azure, vLLM o Ollama, amb fallback entre proveïdors.",
                "Eines i servidors MCP sota polítiques deterministes, amb aprovació humana.",
                "Execucions durables: checkpoint a cada pas i, si cau una rèplica, una altra la reprèn.",
                "RAG híbrid amb cites, memòria per usuari, multi-tenant amb RLS i evals amb usuari simulat.",
            ],
        ),
        en=dict(
            kicker="A production foundation for conversational agents.",
            body=("A provider-free core where the code orchestrates and the LLM only reasons. A new agent is a "
                  "folder of data (YAML, prompt, tools and evals), not new code."),
            points=[
                "Any model: Anthropic, OpenAI, Azure, vLLM or Ollama, with fallback across providers.",
                "Tools and MCP servers under deterministic policies, with human approval.",
                "Durable runs: a checkpoint after every step, and another replica takes over if one crashes.",
                "Hybrid RAG with citations, per-user memory, multi-tenancy with RLS and evals with a simulated user.",
            ],
        ),
    ),
    dict(
        key="kakurega", cap=1, name="Kakurega", link=("https://kakuregalearn.com", "kakuregalearn.com"),
        tech=["FastAPI", "PostgreSQL", "React", "TypeScript", "ONNX Runtime", "Docker", "Caddy"],
        es=dict(
            kicker="Aprender japonés con lo que quieres leer y ver.",
            body=("Subes una novela, un manga o un anime con subtítulos: te dice cuánto entiendes, qué te falta "
                  "y adapta tus lecciones a esa obra. En producción."),
            points=[
                "OCR de manga en el servidor (ONNX Runtime), con una cola de trabajos que sigue donde se quedó.",
                "Repaso espaciado con FSRS, 62 niveles propios y diccionario JMdict con desconjugación.",
                "Unas 1.000 sesiones por minuto con p95 por debajo de 70 ms en un solo i5.",
                "Despliegue sin cortes y tests e2e con Playwright y accesibilidad (axe) en cada página.",
            ],
        ),
        ca=dict(
            kicker="Aprendre japonès amb el que vols llegir i veure.",
            body=("Hi puges una novel·la, un manga o un anime amb subtítols: et diu quant n'entens, què et falta "
                  "i adapta les lliçons a aquella obra. En producció."),
            points=[
                "OCR de manga al servidor (ONNX Runtime), amb una cua de feines que continua on s'havia quedat.",
                "Repàs espaiat amb FSRS, 62 nivells propis i diccionari JMdict amb desconjugació.",
                "Unes 1.000 sessions per minut amb p95 per sota de 70 ms en un sol i5.",
                "Desplegament sense talls i tests e2e amb Playwright i accessibilitat (axe) a cada pàgina.",
            ],
        ),
        en=dict(
            kicker="Learn Japanese with what you want to read and watch.",
            body=("Upload a novel, a manga or an anime with subtitles: it tells you how much you understand, "
                  "what you are missing, and shapes your lessons around that work. Live in production."),
            points=[
                "Server-side manga OCR (ONNX Runtime) with a job queue that resumes where it stopped.",
                "Spaced repetition with FSRS, 62 custom levels and a JMdict dictionary with deinflection.",
                "Around 1,000 sessions a minute with p95 under 70 ms on a single i5.",
                "Zero-downtime deploys and Playwright end-to-end tests with accessibility checks (axe).",
            ],
        ),
    ),
    dict(
        key="blunderling", cap=2, name="BlunderLing", link=("https://www.youtube.com/@BlunderLing", "youtube.com/@BlunderLing"),
        tech=["TypeScript", "Node.js", "Remotion", "React", "Stockfish", "YouTube API", "GitHub Actions"],
        es=dict(
            kicker="La fábrica de vídeos detrás del canal @BlunderLing.",
            body=("Tres Shorts de ajedrez al día: importados de datos abiertos, verificados con motor, "
                  "renderizados, titulados y publicados sin que nadie mire. Coste por vídeo: cero."),
            points=[
                "Stockfish analiza una vez; Remotion y React renderizan; música y efectos se generan por código.",
                "Horario a prueba de cambios de hora y pasadas de recuperación cuando GitHub se salta un cron.",
                "Publicación idempotente: un registro en el repo impide repetir un puzle o una franja.",
                "Retención semanal desde YouTube Analytics para decidir los A/B con datos.",
            ],
        ),
        ca=dict(
            kicker="La fàbrica de vídeos darrere del canal @BlunderLing.",
            body=("Tres Shorts d'escacs al dia: importats de dades obertes, verificats amb motor, renderitzats, "
                  "titulats i publicats sense que ningú miri. Cost per vídeo: zero."),
            points=[
                "Stockfish analitza un cop; Remotion i React renderitzen; música i efectes es generen per codi.",
                "Horari a prova de canvis d'hora i passades de recuperació quan GitHub se salta un cron.",
                "Publicació idempotent: un registre al repo impedeix repetir un puzle o una franja.",
                "Retenció setmanal des de YouTube Analytics per decidir els A/B amb dades.",
            ],
        ),
        en=dict(
            kicker="The video factory behind the @BlunderLing channel.",
            body=("Three chess Shorts a day: imported from open data, engine-verified, rendered, titled and "
                  "uploaded with nobody watching. Cost per video: zero."),
            points=[
                "Stockfish analyses once; Remotion and React render; music and sound effects are generated in code.",
                "DST-proof scheduling, plus catch-up passes for when GitHub silently drops a cron.",
                "Idempotent publishing: a ledger in the repo stops a puzzle or a slot from going out twice.",
                "Weekly retention from YouTube Analytics, so A/B tests are decided on data.",
            ],
        ),
    ),
    dict(
        key="wavesling", cap=3, name="WavesLing", link=("https://wavesling.pages.dev", "wavesling.pages.dev"),
        tech=["TypeScript", "React", "Vite", "Vitest", "Cloudflare Pages", "D1"],
        es=dict(
            kicker="Puzle de tablero diario en el navegador, con motor propio.",
            body=("Un tablero de 5×5 donde cada marea mueve a la vez tus piezas y las del rival. Las reglas, la "
                  "apertura y los precios se decidieron simulando partidas, no por gusto."),
            points=[
                "Motor en TypeScript puro, sin dependencias, compartido por web, servidor, generador y simulador.",
                "Con las reglas nuevas, las tablas simuladas bajan del 71,9 % al 23 %.",
                "Solver BFS que garantiza solución única, IA minimax y Elo de rivales calibrado en round robin.",
                "Funciona sin red y se sirve desde Cloudflare Pages y D1.",
            ],
        ),
        ca=dict(
            kicker="Trencaclosques de tauler diari al navegador, amb motor propi.",
            body=("Un tauler de 5×5 on cada marea mou alhora les teves peces i les del rival. Les regles, "
                  "l'obertura i els preus es van decidir simulant partides, no per gust."),
            points=[
                "Motor en TypeScript pur, sense dependències, compartit per web, servidor, generador i simulador.",
                "Amb les regles noves, les taules simulades baixen del 71,9 % al 23 %.",
                "Solver BFS que garanteix solució única, IA minimax i Elo de rivals calibrat en un round robin.",
                "Funciona sense xarxa i se serveix des de Cloudflare Pages i D1.",
            ],
        ),
        en=dict(
            kicker="A daily browser board puzzle with its own engine.",
            body=("A 5×5 board where every tide moves your pieces and your rival's at once. The rules, the "
                  "opening and the prices were decided by simulating games, not by taste."),
            points=[
                "A pure TypeScript engine with zero dependencies, shared by web app, server, generator and simulator.",
                "With the new rules, simulated draws fall from 71.9% to 23%.",
                "A BFS solver that guarantees unique solutions, a minimax AI and bot Elo calibrated in a round robin.",
                "Works offline and is served from Cloudflare Pages and D1.",
            ],
        ),
    ),
]

MARQUEE = [
    "Python", "TypeScript", "FastAPI", "LangGraph", "MCP", "RAG", "pgvector", "PostgreSQL", "vLLM", "Next.js",
    "React", "Remotion", "ONNX Runtime", "FSRS", "Stockfish", "Docker", "GitHub Actions", "OpenTelemetry",
    "Langfuse", "Cloudflare",
]


# ─── Fuente: Archivo variable, recortada a los caracteres usados ─────────────
def _chars(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return "".join(_chars(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return "".join(_chars(x) for x in v)
    return ""


def _font_css():
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    font = TTFont(FONT)
    sub = subset.Subsetter(opts)
    sub.populate(text=_chars([TXT, PROJECTS, MARQUEE, LINKEDIN]) + string.printable + "%·")
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return ("@font-face{font-family:'A';src:url(data:font/woff2;base64,%s) format('woff2');"
            "font-weight:100 900;font-stretch:62%% 125%%}" % data)


FONT_CSS = _font_css()
BASE_CSS = (
    "text{font-family:'A',Archivo,'Helvetica Neue',Arial,sans-serif;font-kerning:normal}"
    ".n{font-variant-numeric:tabular-nums}"
    f".gx{{transform-box:fill-box;transform-origin:0 50%;animation:gx .6s {EASE} backwards}}"
    "@keyframes gx{from{transform:scaleX(0)}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)

_metrics = {}


def width(s, size, wght=400, wdth=100, track=0.0):
    key = (wght, wdth)
    if key not in _metrics:
        f = instantiateVariableFont(TTFont(FONT), {"wght": wght, "wdth": wdth})
        _metrics[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upm = _metrics[key]
    units = sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in s)
    return units * size / upm + len(s) * track * size


def wrap(s, size, maxw, wght=400):
    lines, cur = [], ""
    for word in s.split():
        test = f"{cur} {word}".strip()
        if cur and width(test, size, wght) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = test
    return lines + [cur] if cur else lines


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def text(x, y, s, size, fill=INK, wght=400, wdth=100, anchor="start", track=0.0, cls="", extra=""):
    style = f' style="font-stretch:{wdth}%"' if wdth != 100 else ""
    ls = f' letter-spacing="{track * size:.2f}"' if track else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{wght}" fill="{fill}" '
            f'text-anchor="{anchor}"{style}{ls}{c}{extra}>{s if s.startswith("<tspan") else esc(s)}</text>')


def chamfer(w, h, c=CUT, x=0, y=0):
    """Lámina con chaflán arriba a la izquierda y abajo a la derecha."""
    return f"M{x + c} {y}H{x + w}V{y + h - c}L{x + w - c} {y + h}H{x}V{y + c}Z"


def octagon(x, y, w, h, c):
    return (f"M{x + c:.1f} {y:.1f}H{x + w - c:.1f}L{x + w:.1f} {y + c:.1f}V{y + h - c:.1f}"
            f"L{x + w - c:.1f} {y + h:.1f}H{x + c:.1f}L{x:.1f} {y + h - c:.1f}V{y + c:.1f}Z")


def arrow(x, y, color, s=9):
    """Flecha diagonal de enlace externo (Archivo no trae ↗)."""
    return (f'<path d="M{x:.1f} {y:.1f}L{x + s:.1f} {y - s:.1f}M{x + 2:.1f} {y - s:.1f}H{x + s:.1f}V{y - 2:.1f}" '
            f'stroke="{color}" stroke-width="2" fill="none"/>')


def svg(w, h, body, title, fill=WHITE, css="", defs="", cut=CUT):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<defs><style>{FONT_CSS}{BASE_CSS}{css}</style>'
            f'<clipPath id="p"><path d="{chamfer(w, h, cut)}"/></clipPath>{defs}</defs>'
            f'<g clip-path="url(#p)"><path d="{chamfer(w, h, cut)}" fill="{fill}"/>{body}</g></svg>')


def delay(s):
    return f' style="animation-delay:{s:.3f}s"'


def head(y, s, fill=INK, maxw=760):
    out = []
    for ln in wrap(s, 44, maxw, 700):
        out.append(text(M, y, ln, 44, fill, 700, track=-0.02))
        y += 50
    return "".join(out), y - 50


# ─── Láminas ─────────────────────────────────────────────────────────────────
def hero(lang):
    L = TXT[lang]
    W = 1000
    b = [text(M - 6, 150, "Bruno", 140, INK, 700, 125, track=-0.03),
         text(M - 6, 279, f'<tspan>Monreal</tspan><tspan fill="{ACCENT}">.</tspan>', 140, INK, 700, 125, track=-0.03),
         text(M, 346, L["lead"], 26, INK, 600)]
    y = 384
    for ln in wrap(L["sub"], 20, 640):
        b.append(text(M, y, ln, 20, MUTED))
        y += 30

    # Índice de capacidades: cada tarjeta de proyecto lleva el número de la que demuestra
    y += 40
    b.append(text(M, y, L["can_title"], 16, MUTED))
    top = y + 24
    col = (W - 2 * M) / 4
    bottom = top
    for i, (title, line) in enumerate(L["can"]):
        x = M + i * col
        b.append(f'<rect class="gx" x="{x:.1f}" y="{top}" width="{col - 24:.1f}" height="3" fill="{INK}"{delay(.15 + i * .08)}/>')
        b.append(text(x, top + 48, f"{i + 1:02d}", 32, ACCENT, 700, cls="n"))
        ty = top + 82
        for ln in wrap(title, 20, col - 30, 700):
            b.append(text(x, ty, ln, 20, INK, 700))
            ty += 26
        ty += 4
        for ln in wrap(line, 16, col - 30):
            b.append(text(x, ty, ln, 16, MUTED))
            ty += 22
        bottom = max(bottom, ty)
    return svg(W, bottom + 34, "".join(b), L["alt_hero"])


def marquee():
    W, H = 1000, 112
    parts, x = [], 0.0
    for t in MARQUEE:
        parts.append(text(x, 76, t, 56, INK, 500, track=-0.02))
        x += width(t, 56, 500, track=-0.02) + 30
        parts.append(f'<path d="{octagon(x, 49, 14, 14, 4)}" fill="{ACCENT}"/>')
        x += 14 + 30
    row = "".join(parts)
    copies = math.ceil(W / x) + 1
    track = "".join(f'<g transform="translate({x * k:.1f} 0)">{row}</g>' for k in range(copies))
    css = ".track{animation:slide %.1fs linear infinite}@keyframes slide{to{transform:translateX(-%.1fpx)}}" % (x / 45, x)
    return svg(W, H, f'<g class="track">{track}</g>', TXT["en"]["alt_marquee"], TINT, css)


def about(lang):
    L = TXT[lang]
    W = 1000
    h, y = head(100, L["about_title"], WHITE, 540)
    b = [h]
    top = y + 64
    ly = top
    for ln in wrap(L["about"], 22, 500):
        b.append(text(M, ly, ln, 22, ON_INK))
        ly += 34
    rx = 620
    b.append(text(rx, top, L["now_title"], 16, SOFT, 700, track=0.04))
    ry = top + 32
    for ln in wrap(L["now"], 20, W - M - rx, 600):
        b.append(text(rx, ry, ln, 20, WHITE, 600))
        ry += 28
    ry += 30
    b.append(text(rx, ry, L["how_title"], 16, SOFT, 700, track=0.04))
    ry += 32
    for f in L["how"]:
        for ln in wrap(f, 18, W - M - rx):
            b.append(text(rx, ry, ln, 18, ON_INK))
            ry += 26
        ry += 12
    return svg(W, max(ly, ry) + 30, "".join(b), L["alt_about"], INK)


def projects_head(lang):
    L = TXT[lang]
    W = 1000
    h, y = head(100, L["projects_title"])
    b = [h]
    y += 44
    for ln in wrap(L["projects_sub"], 20, 760):
        b.append(text(M, y, ln, 20, MUTED))
        y += 30
    return svg(W, y + 18, "".join(b), L["projects_title"])


def card_alt(lang, p):
    P = p[lang]
    return f'{p["name"]}. {P["kicker"]} {P["body"]}'


def card(lang, p):
    L, P = TXT[lang], p[lang]
    W = 1000
    cap = L["can"][p["cap"]][0]
    b = [f'<path d="{octagon(M, 57, 14, 14, 4)}" fill="{ACCENT}"/>',
         text(M + 26, 70, f'{p["cap"] + 1:02d} · {cap}', 16, ACCENT, 700, track=0.02, cls="n")]
    if p["link"]:
        b.append(text(W - M - 18, 70, p["link"][1], 16, INK, 600, anchor="end") + arrow(W - M - 9, 68, INK))
    else:
        b.append(text(W - M, 70, L["private"], 16, MUTED, anchor="end"))
    b.append(text(M - 3, 144, p["name"], 60, INK, 700, 112, track=-0.02))
    y = 194
    for ln in wrap(P["kicker"], 24, W - 2 * M, 600):
        b.append(text(M, y, ln, 24, INK, 600))
        y += 32
    y += 2
    for ln in wrap(P["body"], 20, 780):
        b.append(text(M, y, ln, 20, MUTED))
        y += 30

    # Lo que lo demuestra: dos columnas, filas alineadas
    y += 8
    b.append(f'<rect class="gx" x="{M}" y="{y}" width="{W - 2 * M}" height="1" fill="{PALE}"/>')
    y += 44
    gap = 40
    colw = (W - 2 * M - gap) / 2
    pts = P["points"]
    for r in range(0, len(pts), 2):
        row_h = 0
        for c, pt in enumerate(pts[r:r + 2]):
            x = M + c * (colw + gap)
            lines = wrap(pt, 18, colw - 26)
            b.append(f'<path d="{octagon(x, y - 12, 10, 10, 3)}" fill="{ACCENT}"/>')
            for k, ln in enumerate(lines):
                b.append(text(x + 24, y + k * 27, ln, 18, INK))
            row_h = max(row_h, len(lines) * 27)
        y += row_h + 16

    # Tecnologías, en chips achaflanados
    y += 8
    x = M
    for t in p["tech"]:
        tw = width(t, 15, 500) + 26
        if x + tw > W - M:
            x = M
            y += 42
        b.append(f'<path d="{chamfer(tw, 32, 8, x, y)}" fill="{TINT}"/>' + text(x + 13, y + 21, t, 15, INK, 500))
        x += tw + 10
    return svg(W, y + 32 + 40, "".join(b), card_alt(lang, p))


def footer(lang):
    L = TXT[lang]
    W, H = 1000, 240
    # Fragmento del Eixample: manzanas achaflanadas, girado como la trama real, y la Diagonal
    blk, street = 116, 26
    step = blk + street
    blocks = "".join(f'<path d="{octagon(x, y, blk, blk, 22)}"/>'
                     for x in range(-260, 1260, step) for y in range(-260, 500, step))
    b = [f'<g fill="#fff" fill-opacity=".12" transform="rotate(-9 500 120)">{blocks}</g>',
         '<path d="M-20 266 L1020 -6" stroke="#fff" stroke-opacity=".3" stroke-width="16"/>']
    y = 104
    for ln in wrap(L["footer"], 34, 700, 600):
        b.append(text(M, y, ln, 34, WHITE, 600, track=-0.01))
        y += 42
    label = LINKEDIN[1]
    b.append(text(M, y + 8, label, 20, WHITE, 600) + arrow(M + width(label, 20, 600) + 10, y + 6, WHITE))
    return svg(W, H, "".join(b), L["alt_footer"], ACCENT)


def lang_link(code, on):
    W, H = 136, 48
    name = TXT[code]["name"]
    tw = width(name, 20, 700 if on else 400)
    body = text(W / 2, 28, name, 20, INK if on else MUTED, 700 if on else 400, anchor="middle")
    if on:
        body += f'<rect x="{(W - tw) / 2:.1f}" y="35" width="{tw:.1f}" height="4" fill="{ACCENT}"/>'
    return svg(W, H, body, name, cut=10)


# ─── README ──────────────────────────────────────────────────────────────────
FILES = {"es": "README.md", "ca": "README.ca.md", "en": "README.en.md"}


def readme(lang):
    L = TXT[lang]

    def img(src, alt, href=None):
        tag = f'<img src="assets/{src}" width="100%" alt="{esc(alt)}" />'
        return f'<a href="{href}">{tag}</a>' if href else tag

    links = "\n  ".join(
        f'<a href="{REPO_URL}/{FILES[c]}"><img src="assets/lang-{c}-{"on" if c == lang else "off"}.svg" height="40" alt="{TXT[c]["name"]}" /></a>'
        for c in TXT)
    body = [f'<p align="right">\n  {links}\n</p>',
            img(f"hero-{lang}.svg", L["alt_hero"]),
            img("marquee.svg", L["alt_marquee"]),
            img(f"about-{lang}.svg", L["alt_about"]),
            img(f"projects-{lang}.svg", L["projects_title"])]
    for p in PROJECTS:
        body.append(img(f'{p["key"]}-{lang}.svg', card_alt(lang, p), p["link"][0] if p["link"] else None))
    body.append(img(f"footer-{lang}.svg", L["alt_footer"], LINKEDIN[0]))
    (ROOT / FILES[lang]).write_text("\n\n".join(body) + "\n", encoding="utf-8")


def main():
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    out = {"marquee.svg": marquee()}
    for lang in TXT:
        out[f"hero-{lang}.svg"] = hero(lang)
        out[f"about-{lang}.svg"] = about(lang)
        out[f"projects-{lang}.svg"] = projects_head(lang)
        for p in PROJECTS:
            out[f'{p["key"]}-{lang}.svg'] = card(lang, p)
        out[f"footer-{lang}.svg"] = footer(lang)
        for on in (True, False):
            out[f"lang-{lang}-{'on' if on else 'off'}.svg"] = lang_link(lang, on)
        readme(lang)
    for name, content in out.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"{len(out)} SVGs")


if __name__ == "__main__":
    main()
