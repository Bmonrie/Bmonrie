#!/usr/bin/env python3
"""Genera el README de perfil de Bmonrie: un número de revista sobre un solo ingeniero.

Portada, carta con el sumario, un reportaje por proyecto (figura isométrica, maqueta del producto y
diagrama de arquitectura) y contraportada. Todas las imágenes están dibujadas en código con el mismo
trazo; ninguna es una captura. Inglés primero (README.md), luego español y catalán.

Uso:
    python scripts/build.py            # intenta leer el último Short del canal; si no hay red, usa data/
"""
import datetime as dt
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import diagrams  # noqa: E402
import figures  # noqa: E402
import mockups  # noqa: E402
from kit import (INK, M, MUTED, ON_INK, ON_INK_SOFT, PAPER, ROOT, STONE, W, YELLOW, block, esc, fit,  # noqa: E402
                 rich, set_charset, svg, text, width, wrap)

ASSETS = ROOT / "assets"
LATEST = ROOT / "data" / "latest-short.json"
REPO_URL = "https://github.com/Bmonrie/Bmonrie/blob/main"
LINKEDIN = ("https://www.linkedin.com/in/brunomonrealpujol", "linkedin.com/in/brunomonrealpujol")
FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=UCnFyMu7pAiblj8aV138ehsg"
CAP = 0.675  # altura de mayúscula de Anybody

# ─── Textos ──────────────────────────────────────────────────────────────────
TXT = {
    "en": dict(
        name="English",
        meta="Bruno Monreal · AI & Data Manager · Barcelona",
        headline="Builds the whole thing.",
        standfirst="AI agents, products and pipelines, from the model to the deploy, left running in production.",
        layers=[
            ("The model", "Agents that reason, use tools and pass evals."),
            ("The interface", "Built for the people who use it every day."),
            ("The backend", "APIs, queues and PostgreSQL that hold up under load."),
            ("The deploy", "Containers and releases without downtime."),
            ("What keeps it running", "Schedules, catch-up runs and traces, nobody watching."),
        ],
        letter_title="Four projects, one person.",
        letter_lead="I'm an AI & Data Manager at Forvis Mazars, where I take LLM systems from prototype to production.",
        letter_body=("Outside work I build complete products: the model, the backend, the interface, the deploy and "
                     "what keeps it running. Three of these four are live today; the fourth is the foundation I "
                     "build agents on."),
        private="Private repository",
        built="Built with",
        back_title="Need the whole thing built? Let's talk.",
        colophon=("Set in Anybody. Every figure, mockup and diagram in this issue is drawn in code from the "
                  "projects themselves."),
        date=lambda d: f"{d.day} {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.month - 1]} {d.year}",
        pct=lambda v: f"{v:g}%",
    ),
    "es": dict(
        name="Español",
        meta="Bruno Monreal · AI & Data Manager · Barcelona",
        headline="Construye el sistema entero.",
        standfirst="Agentes, productos y pipelines con IA, del modelo al despliegue, y funcionando en producción.",
        layers=[
            ("El modelo", "Agentes que razonan, usan herramientas y pasan evals."),
            ("La interfaz", "Hecha para quien la usa cada día."),
            ("El backend", "APIs, colas y PostgreSQL que aguantan la carga."),
            ("El despliegue", "Contenedores y versiones sin cortes."),
            ("Lo que lo mantiene vivo", "Horarios, reintentos y trazas, sin nadie mirando."),
        ],
        letter_title="Cuatro proyectos, una persona.",
        letter_lead="Soy AI & Data Manager en Forvis Mazars, donde llevo sistemas con LLMs del prototipo a producción.",
        letter_body=("Fuera del trabajo construyo productos completos: el modelo, el backend, la interfaz, el "
                     "despliegue y lo que los mantiene en marcha. Tres de estos cuatro están en producción hoy; el "
                     "cuarto es la base sobre la que construyo agentes."),
        private="Repositorio privado",
        built="Hecho con",
        back_title="¿Necesitas el sistema entero? Hablemos.",
        colophon=("Compuesto en Anybody. Todas las figuras, maquetas y diagramas de este número están dibujados en "
                  "código a partir de los propios proyectos."),
        date=lambda d: f"{d.day} {['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'][d.month - 1]} {d.year}",
        pct=lambda v: f"{v:g} %".replace(".", ","),
    ),
    "ca": dict(
        name="Català",
        meta="Bruno Monreal · AI & Data Manager · Barcelona",
        headline="Construeix el sistema sencer.",
        standfirst="Agents, productes i pipelines amb IA, del model al desplegament, i funcionant en producció.",
        layers=[
            ("El model", "Agents que raonen, fan servir eines i passen evals."),
            ("La interfície", "Feta per a qui la fa servir cada dia."),
            ("El backend", "APIs, cues i PostgreSQL que aguanten la càrrega."),
            ("El desplegament", "Contenidors i versions sense talls."),
            ("El que el manté viu", "Horaris, reintents i traces, sense ningú mirant."),
        ],
        letter_title="Quatre projectes, una persona.",
        letter_lead="Soc AI & Data Manager a Forvis Mazars, on porto sistemes amb LLMs del prototip a producció.",
        letter_body=("Fora de la feina construeixo productes sencers: el model, el backend, la interfície, el "
                     "desplegament i el que els manté en marxa. Tres d'aquests quatre són en producció avui; el "
                     "quart és la base sobre la qual construeixo agents."),
        private="Repositori privat",
        built="Fet amb",
        back_title="Necessites el sistema sencer? Parlem.",
        colophon=("Compost en Anybody. Totes les figures, maquetes i diagrames d'aquest número estan dibuixats en "
                  "codi a partir dels mateixos projectes."),
        date=lambda d: f"{d.day} {['gen.', 'febr.', 'març', 'abr.', 'maig', 'juny', 'jul.', 'ag.', 'set.', 'oct.', 'nov.', 'des.'][d.month - 1]} {d.year}",
        pct=lambda v: f"{v:g} %".replace(".", ","),
    ),
}

# Un reportaje por proyecto. Cada uno: textos por idioma y rótulos de sus tres dibujos.
PROJECTS = [
    dict(
        key="kakurega", name="Kakurega", link=("https://kakuregalearn.com", "kakuregalearn.com"),
        stack="FastAPI · PostgreSQL · React · ONNX Runtime · Docker · Caddy",
        en=dict(
            what="A learning platform",
            headline="Japanese, taught from your manga.",
            standfirst=("Upload a novel, a manga or an anime with subtitles. Kakurega measures how much of it you "
                        "already understand and turns the rest into your daily lessons."),
            facts=["**About 1,000 study sessions a minute** on a single i5, with p95 under 70\u00a0ms.",
                   "**62 levels** from JLPT N5 to N1, every review scheduled with FSRS.",
                   "**Manga OCR on the server**, page by page, resuming after a restart.",
                   "**Zero-downtime deploys**, Playwright end-to-end tests and accessibility checks."],
            fig_caption="From the work you want to read to the lessons you study today.",
            mock_caption="The reader: tap any word for its reading, meaning and kanji, over the real page.",
            arch_caption="One API, one OCR worker and one Postgres behind Caddy and Cloudflare; every release swaps in without downtime.",
            fig={"work": ("Your manga, novel or anime", "Uploaded as it is: CBZ, EPUB, PDF or subtitles."),
                 "analyze": ("What you already know", "OCR reads every bubble; the target is 90% of its words."),
                 "lessons": ("Lessons from that work", "Its kanji and words first, reviewed with FSRS."),
                 "reader": ("Read it with help", "A pop-up dictionary over the real page.")},
            mock={"nav": ["Home", "Levels", "Grammar", "Library", "Dictionary"], "common": "Common", "noun": "noun",
                  "meaning": "spider", "add": "Add to my words", "spider": "Spider"},
            arch={"browser": ("Browser", "React 19 single-page app"), "cdn": ("Cloudflare", "CDN and TLS"),
                  "host": "Hetzner · Docker Compose", "caddy": ("Caddy", "HTTPS and the static web"),
                  "api": ("API", "FastAPI: study, reader, dictionary"), "ocr": ("OCR worker", "ONNX Runtime, one page at a time"),
                  "db": ("PostgreSQL 17", "Users, progress, OCR queue"),
                  "content": ("Read-only content", "JMdict, KANJIDIC and grammar, shipped with each process"),
                  "ships": "How it ships", "deploy": [("Push to pro", "The production branch"), ("Tests", "Backend, web and browser"),
                             ("arm64 images", "Built and pushed"), ("Swap when healthy", "The old API keeps serving")]},
        ),
        es=dict(
            what="Una plataforma de aprendizaje",
            headline="Japonés, enseñado con tu manga.",
            standfirst=("Subes una novela, un manga o un anime con subtítulos. Kakurega mide cuánto entiendes ya y "
                        "convierte el resto en tus lecciones de cada día."),
            facts=["**Unas 1.000 sesiones de estudio por minuto** en un solo i5, con p95 por debajo de 70\u00a0ms.",
                   "**62 niveles** del JLPT N5 al N1, cada repaso programado con FSRS.",
                   "**OCR de manga en el servidor**, página a página, y sigue donde iba tras un reinicio.",
                   "**Despliegues sin cortes**, tests de extremo a extremo con Playwright y accesibilidad revisada."],
            fig_caption="De la obra que quieres leer a las lecciones que estudias hoy.",
            mock_caption="El lector: toca cualquier palabra para ver su lectura, su significado y sus kanji, sobre la página real.",
            arch_caption="Una API, un proceso de OCR y un Postgres detrás de Caddy y Cloudflare; cada versión entra sin cortes.",
            fig={"work": ("Tu manga, novela o anime", "Se sube tal cual: CBZ, EPUB, PDF o subtítulos."),
                 "analyze": ("Lo que ya sabes", "El OCR lee cada bocadillo; la meta es el 90 % de sus palabras."),
                 "lessons": ("Lecciones de esa obra", "Primero sus kanji y palabras, con repasos FSRS."),
                 "reader": ("Léela con ayuda", "Un diccionario emergente sobre la página real.")},
            mock={"nav": ["Inicio", "Niveles", "Gramática", "Biblioteca", "Diccionario"], "common": "Común",
                  "noun": "sustantivo", "meaning": "araña", "add": "Añadir a mis palabras", "spider": "Araña"},
            arch={"browser": ("Navegador", "Aplicación React 19"), "cdn": ("Cloudflare", "CDN y TLS"),
                  "host": "Hetzner · Docker Compose", "caddy": ("Caddy", "HTTPS y la web estática"),
                  "api": ("API", "FastAPI: estudio, lector, diccionario"), "ocr": ("Proceso de OCR", "ONNX Runtime, página a página"),
                  "db": ("PostgreSQL 17", "Usuarios, progreso, cola de OCR"),
                  "content": ("Contenido de solo lectura", "JMdict, KANJIDIC y gramática, dentro de cada proceso"),
                  "ships": "Cómo se publica", "deploy": [("Push a pro", "La rama de producción"), ("Tests", "Backend, web y navegador"),
                             ("Imágenes arm64", "Se construyen y suben"), ("Relevo en sano", "La API vieja sigue sirviendo")]},
        ),
        ca=dict(
            what="Una plataforma d'aprenentatge",
            headline="Japonès, ensenyat amb el teu manga.",
            standfirst=("Hi puges una novel·la, un manga o un anime amb subtítols. Kakurega mesura quant n'entens ja i "
                        "converteix la resta en les teves lliçons de cada dia."),
            facts=["**Unes 1.000 sessions d'estudi per minut** en un sol i5, amb p95 per sota de 70\u00a0ms.",
                   "**62 nivells** del JLPT N5 al N1, cada repàs programat amb FSRS.",
                   "**OCR de manga al servidor**, pàgina a pàgina, i continua on anava després d'un reinici.",
                   "**Desplegaments sense talls**, tests d'extrem a extrem amb Playwright i accessibilitat revisada."],
            fig_caption="De l'obra que vols llegir a les lliçons que estudies avui.",
            mock_caption="El lector: toca qualsevol paraula per veure'n la lectura, el significat i els kanji, sobre la pàgina real.",
            arch_caption="Una API, un procés d'OCR i un Postgres darrere de Caddy i Cloudflare; cada versió entra sense talls.",
            fig={"work": ("El teu manga, novel·la o anime", "S'hi puja tal qual: CBZ, EPUB, PDF o subtítols."),
                 "analyze": ("El que ja saps", "L'OCR llegeix cada bafarada; l'objectiu és el 90 % de les paraules."),
                 "lessons": ("Lliçons d'aquella obra", "Primer els seus kanji i paraules, amb repassos FSRS."),
                 "reader": ("Llegeix-la amb ajuda", "Un diccionari emergent sobre la pàgina real.")},
            mock={"nav": ["Inici", "Nivells", "Gramàtica", "Biblioteca", "Diccionari"], "common": "Comú",
                  "noun": "substantiu", "meaning": "aranya", "add": "Afegeix a la llista", "spider": "Aranya"},
            arch={"browser": ("Navegador", "Aplicació React 19"), "cdn": ("Cloudflare", "CDN i TLS"),
                  "host": "Hetzner · Docker Compose", "caddy": ("Caddy", "HTTPS i la web estàtica"),
                  "api": ("API", "FastAPI: estudi, lector, diccionari"), "ocr": ("Procés d'OCR", "ONNX Runtime, pàgina a pàgina"),
                  "db": ("PostgreSQL 17", "Usuaris, progrés, cua d'OCR"),
                  "content": ("Contingut de només lectura", "JMdict, KANJIDIC i gramàtica, dins de cada procés"),
                  "ships": "Com es publica", "deploy": [("Push a pro", "La branca de producció"), ("Tests", "Backend, web i navegador"),
                             ("Imatges arm64", "Es construeixen i es pugen"), ("Relleu en sa", "L'API vella continua servint")]},
        ),
    ),
    dict(
        key="blunderling", name="BlunderLing", link=("https://www.youtube.com/@BlunderLing", "youtube.com/@BlunderLing"),
        stack="TypeScript · Remotion · React · Stockfish · YouTube API · GitHub Actions",
        en=dict(
            what="A video pipeline",
            headline="Three Shorts a day. Nobody presses publish.",
            standfirst=("The video factory behind the @BlunderLing chess channel. Every puzzle is imported, verified, "
                        "rendered, titled and uploaded on a schedule. Cost per video: zero."),
            facts=["**DST-proof scheduling** at 13:17, 18:17 and 23:17, Madrid time.",
                   "**Catch-up runs** for the days GitHub silently drops a cron.",
                   "**A ledger in the repo** that refuses to publish a puzzle or a slot twice.",
                   "**Weekly retention** from YouTube Analytics to settle A/B tests."],
            fig_caption="From open puzzle data to a Short on the channel, three times a day.",
            mock_caption="A recent Short: “{title}”, published {date}.",
            arch_caption="Engine analysis happens once and is baked in; a GitHub Action does the rest every day.",
            fig={"data": ("Open puzzle data", "Imported from Lichess, never written by hand."),
                 "engine": ("Engine-verified", "Stockfish checks every line once, then it is baked in."),
                 "render": ("Rendered in code", "Remotion draws each frame; the music is synthesized."),
                 "publish": ("Uploaded on schedule", "Three slots a day, Madrid time. A ledger in the repo blocks duplicates.")},
            mock={"hook": ["HE TOOK THE KNIGHT.", "QUEEN GONE."],
                  "slots": [("13:17", "Which piece?", "One piece is covered and three are offered. Only one mates."),
                            ("18:17", "Brilliant or blunder?", "One move is drawn on the board. Half of them are traps."),
                            ("23:17", "The trap", "A real opening trap from a Lichess game, punished on screen.")]},
            arch={"analyst": "Once: puzzles and analysis, baked into the repo", "daily": "Every day, unattended", "baked": "baked analysis",
                  "lichess": ("Lichess", "Puzzles and real games"), "stockfish": ("Stockfish", "Verifies and annotates"),
                  "remotion": ("Remotion", "React, one per format"), "youtube": ("YouTube", "Data API upload"),
                  "actions": ("GitHub Actions", "Three slots, a DST gate and catch-up passes"),
                  "ledger": ("published.json", "The only memory: what went out and when, committed back so nothing goes out twice"),
                  "weekly": "Every Monday", "stats": ("stats.ts", "Reads the ledger"),
                  "analytics": ("YouTube Analytics", "Retention per video"), "statsjson": ("stats.json", "Week-on-week series")},
        ),
        es=dict(
            what="Una cadena de vídeo automática",
            headline="Tres Shorts al día. Nadie pulsa publicar.",
            standfirst=("La fábrica de vídeos del canal de ajedrez @BlunderLing. Cada puzle se importa, se verifica, "
                        "se renderiza, se titula y se sube a su hora. Coste por vídeo: cero."),
            facts=["**Horario a prueba de cambios de hora**: 13:17, 18:17 y 23:17, hora de Madrid.",
                   "**Pasadas de recuperación** para los días en que GitHub se salta un cron sin avisar.",
                   "**Un registro en el repo** que impide publicar dos veces un puzle o una franja.",
                   "**Retención semanal** desde YouTube Analytics para decidir los A/B."],
            fig_caption="De los datos abiertos de puzles a un Short en el canal, tres veces al día.",
            mock_caption="Un Short reciente: «{title}», publicado el {date}.",
            arch_caption="El análisis del motor se hace una vez y queda fijado; una GitHub Action hace el resto cada día.",
            fig={"data": ("Datos abiertos", "Puzles importados de Lichess, nunca escritos a mano."),
                 "engine": ("Verificado con motor", "Stockfish comprueba cada línea una vez y queda fijada."),
                 "render": ("Renderizado en código", "Remotion dibuja cada fotograma; la música se sintetiza."),
                 "publish": ("Subido a su hora", "Tres franjas al día, hora de Madrid. Un registro en el repo impide duplicados.")},
            mock={"hook": ["HE TOOK THE KNIGHT.", "QUEEN GONE."],
                  "slots": [("13:17", "¿Qué pieza?", "Una pieza está tapada y hay tres opciones. Solo una da mate."),
                            ("18:17", "¿Genial o error?", "Hay una jugada dibujada. La mitad son trampas."),
                            ("23:17", "La trampa", "Una trampa de apertura real de Lichess, castigada en pantalla.")]},
            arch={"analyst": "Una vez: puzles y análisis, fijados en el repo", "daily": "Cada día, sin nadie", "baked": "análisis fijado",
                  "lichess": ("Lichess", "Puzles y partidas reales"), "stockfish": ("Stockfish", "Verifica y anota"),
                  "remotion": ("Remotion", "React, una por formato"), "youtube": ("YouTube", "Subida por Data API"),
                  "actions": ("GitHub Actions", "Tres franjas, filtro de horario y pasadas de recuperación"),
                  "ledger": ("published.json", "La única memoria: qué salió y cuándo, de vuelta al repo para que nada salga dos veces"),
                  "weekly": "Cada lunes", "stats": ("stats.ts", "Lee el registro"),
                  "analytics": ("YouTube Analytics", "Retención por vídeo"), "statsjson": ("stats.json", "Serie semana a semana")},
        ),
        ca=dict(
            what="Una cadena de vídeo automàtica",
            headline="Tres Shorts al dia. Ningú prem publicar.",
            standfirst=("La fàbrica de vídeos del canal d'escacs @BlunderLing. Cada trencaclosques s'importa, es "
                        "verifica, es renderitza, es titula i es puja a la seva hora. Cost per vídeo: zero."),
            facts=["**Horari a prova de canvis d'hora**: 13:17, 18:17 i 23:17, hora de Madrid.",
                   "**Passades de recuperació** per als dies que GitHub se salta un cron sense avisar.",
                   "**Un registre al repo** que impedeix publicar dues vegades un trencaclosques o una franja.",
                   "**Retenció setmanal** des de YouTube Analytics per decidir els A/B."],
            fig_caption="De les dades obertes de trencaclosques a un Short al canal, tres cops al dia.",
            mock_caption="Un Short recent: «{title}», publicat el {date}.",
            arch_caption="L'anàlisi del motor es fa un cop i queda fixada; una GitHub Action fa la resta cada dia.",
            fig={"data": ("Dades obertes", "Trencaclosques importats de Lichess, mai escrits a mà."),
                 "engine": ("Verificat amb motor", "Stockfish comprova cada línia un cop i queda fixada."),
                 "render": ("Renderitzat en codi", "Remotion dibuixa cada fotograma; la música se sintetitza."),
                 "publish": ("Pujat a la seva hora", "Tres franges al dia, hora de Madrid. Un registre al repo impedeix duplicats.")},
            mock={"hook": ["HE TOOK THE KNIGHT.", "QUEEN GONE."],
                  "slots": [("13:17", "Quina peça?", "Una peça està tapada i hi ha tres opcions. Només una fa mat."),
                            ("18:17", "Genial o error?", "Hi ha una jugada dibuixada. La meitat són paranys."),
                            ("23:17", "El parany", "Un parany d'obertura real de Lichess, castigat en pantalla.")]},
            arch={"analyst": "Un cop: trencaclosques i anàlisi, fixats al repo", "daily": "Cada dia, sense ningú", "baked": "anàlisi fixada",
                  "lichess": ("Lichess", "Trencaclosques i partides reals"), "stockfish": ("Stockfish", "Verifica i anota"),
                  "remotion": ("Remotion", "React, una per format"), "youtube": ("YouTube", "Pujada per Data API"),
                  "actions": ("GitHub Actions", "Tres franges, filtre d'horari i passades de recuperació"),
                  "ledger": ("published.json", "L'única memòria: què ha sortit i quan, de tornada al repo perquè res no surti dos cops"),
                  "weekly": "Cada dilluns", "stats": ("stats.ts", "Llegeix el registre"),
                  "analytics": ("YouTube Analytics", "Retenció per vídeo"), "statsjson": ("stats.json", "Sèrie setmana a setmana")},
        ),
    ),
    dict(
        key="agents", name="Template_Agents", link=None,
        stack="Python · FastAPI · PostgreSQL · pgvector · MCP · Next.js · OpenTelemetry",
        en=dict(
            what="An agent platform",
            headline="The code orchestrates. The model only reasons.",
            standfirst=("Template_Agents is a production foundation for conversational agents: support bots, sales "
                        "assistants, internal copilots. A new agent is a folder of data, not new code."),
            facts=["**Any model**: Anthropic, OpenAI, Azure, vLLM or Ollama, with fallback across providers.",
                   "**Tools and MCP servers** behind deterministic policies, with human approval.",
                   "**Durable runs**: a checkpoint after every step; another replica takes over after a crash.",
                   "**Hybrid RAG** with citations, per-user memory, row-level security and evals with a simulated user."],
            fig_caption="A folder of data defines the agent; the core runs it on any model.",
            mock_caption="The bundled chat: streaming answers, tool cards that wait for approval, and citations.",
            arch_caption="Ports and adapters: the core never talks to a provider directly.",
            fig={"providers": ["Anthropic", "OpenAI", "Azure", "vLLM", "Ollama"],
                 "folder": ("An agent is a folder", "YAML, a prompt, tools and evals. No new code."),
                 "core": ("A provider-free core", "The loop, policies, memory and multi-agent, with no SDKs."),
                 "models": ("Any model", "Swapped by configuration, with fallback across providers."),
                 "store": ("One database", "Postgres with pgvector: state, queue, search and memory.")},
            mock={"convos": "Conversations", "threads": ["Order status", "Refund policy", "Change of address"],
                  "question": "Where is my order 4417?", "args": "order_id: 4417",
                  "approval": "Needed your approval before it ran", "approved": "Approved", "by": "by you, 10:42",
                  "answer": "It shipped on Tuesday and should arrive on Friday. Returns are free for 30 days.",
                  "cite": "1 · shipping-policy.pdf", "input": "Message the support agent"},
            arch={"clients": ("Clients", [("Agent author", "YAML, prompts"), ("Web app", "Next.js"), ("API clients", "HTTP, SSE"), ("CI", "evals")]),
                  "core": ("Core", [("Runtime", "checkpoints"), ("Policies", "allow, ask"), ("Memory", "recall"), ("Multi-agent", "transfer")]),
                  "adapters": ("Adapters", [("Models", "any provider"), ("Tools", "local, MCP"), ("Knowledge", "hybrid"), ("Telemetry", "OTel")]),
                  "external": ("External", [("LLMs", "APIs, local"), ("MCP servers", "remote"), ("Postgres", "pgvector"), ("Langfuse", "traces")]),
                  "calls": {"clients": "run", "core": "calls through ports", "adapters": "replaceable by configuration"}},
        ),
        es=dict(
            what="Una plataforma de agentes",
            headline="El código orquesta. El modelo solo razona.",
            standfirst=("Template_Agents es una base de producción para agentes conversacionales: bots de soporte, "
                        "asistentes de ventas, copilotos internos. Un agente nuevo es una carpeta de datos, no código nuevo."),
            facts=["**Cualquier modelo**: Anthropic, OpenAI, Azure, vLLM u Ollama, con fallback entre proveedores.",
                   "**Herramientas y servidores MCP** tras políticas deterministas, con aprobación humana.",
                   "**Ejecuciones duraderas**: checkpoint en cada paso; si cae una réplica, otra la retoma.",
                   "**RAG híbrido** con citas, memoria por usuario, seguridad por filas y evals con usuario simulado."],
            fig_caption="Una carpeta de datos define el agente; el núcleo lo ejecuta con cualquier modelo.",
            mock_caption="El chat que trae: respuestas en streaming, herramientas que esperan aprobación y citas.",
            arch_caption="Puertos y adaptadores: el núcleo nunca habla directamente con un proveedor.",
            fig={"providers": ["Anthropic", "OpenAI", "Azure", "vLLM", "Ollama"],
                 "folder": ("Un agente es una carpeta", "YAML, un prompt, herramientas y evals. Sin código nuevo."),
                 "core": ("Un núcleo sin proveedor", "El bucle, las políticas, la memoria y los multiagentes, sin SDKs."),
                 "models": ("Cualquier modelo", "Se cambia por configuración, con fallback entre proveedores."),
                 "store": ("Una sola base de datos", "Postgres con pgvector: estado, cola, búsqueda y memoria.")},
            mock={"convos": "Conversaciones", "threads": ["Estado del pedido", "Devoluciones", "Cambio de dirección"],
                  "question": "¿Dónde está mi pedido 4417?", "args": "order_id: 4417",
                  "approval": "Necesitaba tu aprobación para ejecutarse", "approved": "Aprobada", "by": "por ti, 10:42",
                  "answer": "Salió el martes y debería llegar el viernes. Las devoluciones son gratis durante 30 días.",
                  "cite": "1 · shipping-policy.pdf", "input": "Escribe al agente de soporte"},
            arch={"clients": ("Clientes", [("Autor del agente", "YAML, prompts"), ("Web", "Next.js"), ("Clientes API", "HTTP, SSE"), ("CI", "evals")]),
                  "core": ("Núcleo", [("Runtime", "checkpoints"), ("Políticas", "permitir, preguntar"), ("Memoria", "recuerdo"), ("Multiagente", "traspaso")]),
                  "adapters": ("Adaptadores", [("Modelos", "cualquiera"), ("Herramientas", "locales, MCP"), ("Conocimiento", "híbrido"), ("Telemetría", "OTel")]),
                  "external": ("Externo", [("LLMs", "APIs, locales"), ("Servidores MCP", "remotos"), ("Postgres", "pgvector"), ("Langfuse", "trazas")]),
                  "calls": {"clients": "ejecutan", "core": "llama por puertos", "adapters": "se cambian por configuración"}},
        ),
        ca=dict(
            what="Una plataforma d'agents",
            headline="El codi orquestra. El model només raona.",
            standfirst=("Template_Agents és una base de producció per a agents conversacionals: bots de suport, "
                        "assistents de vendes, copilots interns. Un agent nou és una carpeta de dades, no codi nou."),
            facts=["**Qualsevol model**: Anthropic, OpenAI, Azure, vLLM o Ollama, amb fallback entre proveïdors.",
                   "**Eines i servidors MCP** darrere de polítiques deterministes, amb aprovació humana.",
                   "**Execucions durables**: checkpoint a cada pas; si cau una rèplica, una altra la reprèn.",
                   "**RAG híbrid** amb cites, memòria per usuari, seguretat per files i evals amb usuari simulat."],
            fig_caption="Una carpeta de dades defineix l'agent; el nucli l'executa amb qualsevol model.",
            mock_caption="El xat que porta: respostes en streaming, eines que esperen aprovació i cites.",
            arch_caption="Ports i adaptadors: el nucli no parla mai directament amb un proveïdor.",
            fig={"providers": ["Anthropic", "OpenAI", "Azure", "vLLM", "Ollama"],
                 "folder": ("Un agent és una carpeta", "YAML, un prompt, eines i evals. Sense codi nou."),
                 "core": ("Un nucli sense proveïdor", "El bucle, les polítiques, la memòria i els multiagents, sense SDKs."),
                 "models": ("Qualsevol model", "Es canvia per configuració, amb fallback entre proveïdors."),
                 "store": ("Una sola base de dades", "Postgres amb pgvector: estat, cua, cerca i memòria.")},
            mock={"convos": "Converses", "threads": ["Estat de la comanda", "Devolucions", "Canvi d'adreça"],
                  "question": "On és la meva comanda 4417?", "args": "order_id: 4417",
                  "approval": "Necessitava la teva aprovació per executar-se", "approved": "Aprovada", "by": "per tu, 10:42",
                  "answer": "Va sortir dimarts i hauria d'arribar divendres. Les devolucions són gratuïtes durant 30 dies.",
                  "cite": "1 · shipping-policy.pdf", "input": "Escriu a l'agent de suport"},
            arch={"clients": ("Clients", [("Autor de l'agent", "YAML, prompts"), ("Web", "Next.js"), ("Clients API", "HTTP, SSE"), ("CI", "evals")]),
                  "core": ("Nucli", [("Runtime", "checkpoints"), ("Polítiques", "permet, pregunta"), ("Memòria", "record"), ("Multiagent", "traspàs")]),
                  "adapters": ("Adaptadors", [("Models", "qualsevol"), ("Eines", "locals, MCP"), ("Coneixement", "híbrid"), ("Telemetria", "OTel")]),
                  "external": ("Extern", [("LLMs", "APIs, locals"), ("Servidors MCP", "remots"), ("Postgres", "pgvector"), ("Langfuse", "traces")]),
                  "calls": {"clients": "executen", "core": "crida per ports", "adapters": "es canvien per configuració"}},
        ),
    ),
    dict(
        key="wavesling", name="WavesLing", link=("https://wavesbyling.com", "wavesbyling.com"),
        stack="TypeScript · React · Vite · Vitest · Cloudflare",
        en=dict(
            what="A browser game",
            headline="Draws fell from 71.9% to 23%.",
            standfirst=("WavesLing is a daily 5×5 board puzzle where every tide moves your pieces and your rival's at "
                        "once. Its rules, its opening and the prices of its pieces were decided by simulating games, not by taste."),
            facts=["**One engine** in pure TypeScript, zero dependencies, shared by the web app, server, generator and simulator.",
                   "**A BFS solver** that guarantees every daily puzzle has a single solution.",
                   "**Bot Elo** calibrated in a round robin, and a minimax AI to play against.",
                   "**Works offline** and is served from Cloudflare."],
            fig_caption="Drawn games in simulated AI-versus-AI play, under the classic rules and under the tide rules.",
            mock_caption="The daily puzzle: pick a direction and every piece that answers it moves at once.",
            arch_caption="One engine, imported by everything else, so the rules can only live in one place.",
            fig={"before": "Classic rules", "after": "Tide rules",
                 "tide": ("One tide moves every piece", "Yours and your rival's, at the same time."),
                 "measure": ("Measured, not chosen", "Drawn games in simulated AI-versus-AI play.")},
            mock={"tabs": ["classic", "arcade", "crowd"], "heading": "each piece keeps its move",
                  "body": "A rook is still a rook. You send a tide, and every piece that travels that way goes at once.",
                  "caption": "rook · straight, until something stops it", "pad": "Eight directions"},
            arch={"engine": ("Engine", "Pure TypeScript, zero dependencies. tide.ts is the only way in."),
                  "web": ("Web app", "React and Vite"), "server": ("Server", "Cloudflare, leaderboards only"),
                  "game": ("Game modes", "Daily, arcade, duel and Elo"), "generator": ("Generator", "Writes the puzzle bank"),
                  "autoplay": ("Simulator", "AI against AI, to measure the rules"), "tests": ("Tests", "Normative vectors"),
                  "imports": "import"},
        ),
        es=dict(
            what="Un juego de navegador",
            headline="Las tablas bajaron del 71,9 % al 23 %.",
            standfirst=("WavesLing es un puzle diario en un tablero de 5×5 donde cada marea mueve a la vez tus piezas y "
                        "las del rival. Sus reglas, su apertura y los precios de sus piezas se decidieron simulando partidas, no por gusto."),
            facts=["**Un solo motor** en TypeScript puro, sin dependencias, compartido por la web, el servidor, el generador y el simulador.",
                   "**Un solver BFS** que garantiza que cada puzle diario tiene una única solución.",
                   "**Elo de los rivales** calibrado en un round robin, y una IA minimax contra la que jugar.",
                   "**Funciona sin conexión** y se sirve desde Cloudflare."],
            fig_caption="Partidas en tablas en juego simulado IA contra IA, con las reglas clásicas y con las de marea.",
            mock_caption="El puzle del día: eliges una dirección y todas las piezas que responden a ella se mueven a la vez.",
            arch_caption="Un solo motor, que importa todo lo demás, para que las reglas solo puedan vivir en un sitio.",
            fig={"before": "Reglas clásicas", "after": "Reglas de marea",
                 "tide": ("Una marea mueve todas las piezas", "Las tuyas y las del rival, a la vez."),
                 "measure": ("Medido, no elegido", "Partidas en tablas en juego simulado IA contra IA.")},
            mock={"tabs": ["classic", "arcade", "crowd"], "heading": "cada pieza conserva su movimiento",
                  "body": "Una torre sigue siendo una torre. Envías una marea y todas las piezas que van en esa dirección se mueven a la vez.",
                  "caption": "torre · recto, hasta que algo la para", "pad": "Ocho direcciones"},
            arch={"engine": ("Motor", "TypeScript puro, sin dependencias. tide.ts es la única puerta."),
                  "web": ("Web", "React y Vite"), "server": ("Servidor", "Cloudflare, solo clasificaciones"),
                  "game": ("Modos de juego", "Diario, arcade, duelo y Elo"), "generator": ("Generador", "Escribe el banco de puzles"),
                  "autoplay": ("Simulador", "IA contra IA, para medir las reglas"), "tests": ("Tests", "Vectores normativos"),
                  "imports": "importan"},
        ),
        ca=dict(
            what="Un joc de navegador",
            headline="Les taules van baixar del 71,9 % al 23 %.",
            standfirst=("WavesLing és un trencaclosques diari en un tauler de 5×5 on cada marea mou alhora les teves "
                        "peces i les del rival. Les regles, l'obertura i els preus de les peces es van decidir simulant partides, no per gust."),
            facts=["**Un sol motor** en TypeScript pur, sense dependències, compartit per la web, el servidor, el generador i el simulador.",
                   "**Un solver BFS** que garanteix que cada trencaclosques diari té una única solució.",
                   "**Elo dels rivals** calibrat en un round robin, i una IA minimax contra la qual jugar.",
                   "**Funciona sense connexió** i se serveix des de Cloudflare."],
            fig_caption="Partides en taules en joc simulat IA contra IA, amb les regles clàssiques i amb les de marea.",
            mock_caption="El trencaclosques del dia: tries una direcció i totes les peces que hi responen es mouen alhora.",
            arch_caption="Un sol motor, que importa tota la resta, perquè les regles només puguin viure en un lloc.",
            fig={"before": "Regles clàssiques", "after": "Regles de marea",
                 "tide": ("Una marea mou totes les peces", "Les teves i les del rival, alhora."),
                 "measure": ("Mesurat, no triat", "Partides en taules en joc simulat IA contra IA.")},
            mock={"tabs": ["classic", "arcade", "crowd"], "heading": "cada peça conserva el seu moviment",
                  "body": "Una torre continua sent una torre. Hi envies una marea i totes les peces que van en aquella direcció es mouen alhora.",
                  "caption": "torre · recte, fins que alguna cosa l'atura", "pad": "Vuit direccions"},
            arch={"engine": ("Motor", "TypeScript pur, sense dependències. tide.ts és l'única porta."),
                  "web": ("Web", "React i Vite"), "server": ("Servidor", "Cloudflare, només classificacions"),
                  "game": ("Modes de joc", "Diari, arcade, duel i Elo"), "generator": ("Generador", "Escriu el banc de trencaclosques"),
                  "autoplay": ("Simulador", "IA contra IA, per mesurar les regles"), "tests": ("Tests", "Vectors normatius"),
                  "imports": "importen"},
        ),
    ),
]
GROUND = {"kakurega": PAPER, "blunderling": STONE, "agents": PAPER, "wavesling": STONE}


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


def _short_bits(lang):
    d = dt.date.fromisoformat(SHORT["published"])
    return SHORT["title"], TXT[lang]["date"](d)


# ─── Piezas de página ────────────────────────────────────────────────────────
def arrow(x, y, color, s=11):
    return (f'<path d="M{x:.1f} {y:.1f}L{x + s:.1f} {y - s:.1f}M{x + 2:.1f} {y - s:.1f}H{x + s:.1f}V{y - 2:.1f}" '
            f'stroke="{color}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')


def headline(y, s, fill=INK, maxw=W - 2 * M, sizes=(84, 76, 68, 60, 54)):
    size, lines = fit(s, maxw, sizes, 800, 112, -0.03)
    out = []
    for i, ln in enumerate(lines):
        out.append(text(M - 3, y + size * CAP + i * size * 1.02, ln, size, fill, 800, 112, track=-0.03))
    return "".join(out), y + size * CAP + (len(lines) - 1) * size * 1.02


def _ink_bounds():
    """Huecos laterales de la M y de la L en la instancia del masthead, para medir la tinta y no la caja."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    f = instantiateVariableFont(TTFont(ROOT / "scripts" / "fonts" / "anybody.ttf"), {"wght": 900, "wdth": 150})
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    out = []
    for ch in "ML":
        pen = BoundsPen(gs)
        gs[cmap[ord(ch)]].draw(pen)
        out.append((pen.bounds, f["hmtx"][cmap[ord(ch)]][0]))
    (m_b, _), (l_b, l_adv) = out
    return m_b[0] / upm, (l_adv - l_b[2]) / upm


LSB, RSB = _ink_bounds()


def masthead(y, fill=INK):
    """MONREAL de margen a margen: la tinta, no la caja, ocupa exactamente la medida."""
    track = -0.01
    unit = width("MONREAL", 1, 900, 150, track) - track - LSB - RSB  # ancho de tinta por punto
    size = (W - 2 * M) / unit
    return (text(M - LSB * size, y + size * CAP, "MONREAL", round(size, 1), fill, 900, 150, track=track),
            y + size * CAP)


def caption(x, y, s, maxw=W - 2 * M, fill=MUTED):
    return block(x, y, s, 19, maxw, fill, 500, lead=1.4)


# ─── Láminas ─────────────────────────────────────────────────────────────────
def cover(lang):
    L = TXT[lang]
    b = []
    mh, y = masthead(40)
    b.append(mh)
    y += 46
    b.append(text(M, y, L["meta"], 22, INK, 600))
    h, y = headline(y + 50, L["headline"])
    b.append(h)
    s, y = block(M, y + 54, L["standfirst"], 28, 760, INK, 500, lead=1.35)
    b.append(s)
    top = y + 12
    fig, fh = figures.stack(L)
    b.append(f'<rect x="0" y="{top:.0f}" width="{W}" height="{fh + 60:.0f}" fill="{PAPER}"/>')
    b.append(f'<g transform="translate({M} {top + 30:.0f})">{fig}</g>')
    alt = f'MONREAL. {L["meta"]}. {L["headline"]} {L["standfirst"]}'
    return svg(top + fh + 60, "".join(b), alt, YELLOW)


def letter(lang):
    L = TXT[lang]
    h, y = headline(56, L["letter_title"], ON_INK, sizes=(64, 56, 48))
    b = [h]
    top = y + 56
    lead, ly = block(M, top, L["letter_lead"], 28, 420, ON_INK, 600, lead=1.35)
    body, ly = block(M, ly + 16, L["letter_body"], 22, 420, ON_INK, 400, lead=1.5)
    b += [lead, body, text(M, ly + 22, "Bruno Monreal", 26, YELLOW, 800, 110)]
    ly += 40
    rx = 540
    ry = top + 26
    for p in PROJECTS:
        P = p[lang]
        b.append(text(rx, ry, p["name"], 30, ON_INK, 800, 108))
        b.append(text(rx, ry + 30, P["what"], 20, ON_INK_SOFT))
        b.append(text(rx, ry + 56, p["link"][1] if p["link"] else L["private"], 20, ON_INK_SOFT, 600))
        ry += 98
    alt = f'{L["letter_title"]} {L["letter_lead"]} {L["letter_body"]}'
    return svg(max(ly, ry) + 30, "".join(b), alt, INK)


def feature_a(lang, p):
    """La primera página del reportaje: titular, entradilla y la figura de cómo funciona."""
    L, P = TXT[lang], p[lang]
    b = []
    h, y = headline(56, P["headline"])
    b.append(h)
    s, y = block(M, y + 54, P["standfirst"], 26, 800, INK, 500, lead=1.4)
    b.append(s)
    fig, fh = getattr(figures, p["key"])(dict(fig=P["fig"] | {"fmt": L["pct"]}, layers=L["layers"]))
    top = y + 20
    b.append(f'<g transform="translate({M} {top:.0f})">{fig}</g>')
    c, y = caption(M, top + fh + 30, P["fig_caption"])
    b.append(c)
    alt = f'{p["name"]}. {P["headline"]} {P["standfirst"]} {P["fig_caption"]}'
    return svg(y + 30, "".join(b), alt, GROUND[p["key"]])


def feature_b(lang, p):
    """La segunda: la maqueta del producto, su arquitectura y los datos."""
    L, P = TXT[lang], p[lang]
    ground = GROUND[p["key"]]
    b = []
    mock, mh = getattr(mockups, p["key"])(dict(mock=P["mock"] | ({"title": SHORT["title"]} if p["key"] == "blunderling" else {})))
    b.append(f'<g transform="translate({M} 48)">{mock}</g>')
    cap_text = P["mock_caption"]
    if "{title}" in cap_text:
        title, date = _short_bits(lang)
        cap_text = cap_text.format(title=title, date=date)
    c, y = caption(M, 48 + mh + 36, cap_text)
    b.append(c)
    arch_fn = getattr(diagrams, p["key"])
    diagrams.TINT = STONE if ground == PAPER else PAPER
    diagrams.GROUND = ground
    arch, ah = arch_fn(dict(arch=P["arch"]))
    top = y + 40
    b.append(f'<g transform="translate({M} {top:.0f})">{arch}</g>')
    c, y = caption(M, top + ah + 40, P["arch_caption"])
    b.append(c)
    # Los datos, en dos columnas
    y += 44
    colw = (W - 2 * M - 48) / 2
    ys = [y, y]
    for i, f in enumerate(P["facts"]):
        col = i % 2
        t, ny = rich(M + col * (colw + 48), ys[col], f, 22, colw, INK, INK, lead=1.45)
        b.append(t)
        ys[col] = ny + 18
    y = max(ys) + 10
    b.append(text(M, y, f'{L["built"]} {p["stack"]}', 19, MUTED, 600))
    y += 52
    if p["link"]:
        lab = p["link"][1]
        b.append(text(M, y, lab, 24, INK, 800) + arrow(M + width(lab, 24, 800) + 12, y - 3, INK, 12))
    else:
        b.append(text(M, y, L["private"], 24, MUTED, 700))
    alt = f'{p["name"]}. {P["mock_caption"].split(":")[0]}. {P["arch_caption"]} ' + " ".join(f.replace("**", "") for f in P["facts"])
    return svg(y + 48, "".join(b), alt, ground)


def back(lang):
    L = TXT[lang]
    h, y = headline(64, L["back_title"], sizes=(76, 68, 60, 54))
    b = [h]
    y += 70
    lab = LINKEDIN[1]
    b.append(text(M, y, lab, 30, INK, 800) + arrow(M + width(lab, 30, 800) + 14, y - 4, INK, 14))
    c, y = block(M, y + 50, L["colophon"], 20, 640, INK, 500, lead=1.45)
    b.append(c)
    mh, y = masthead(y + 40)
    b.append(mh)
    return svg(y + 44, "".join(b), f'{L["back_title"]} LinkedIn: {lab}', YELLOW)


def lang_link(code, on):
    w, h = 150, 46
    name = TXT[code]["name"]
    body = text(w / 2, 30, name, 20, YELLOW if on else INK, 800 if on else 600, anchor="middle")
    return svg(h, body, name, INK if on else YELLOW, w)


# ─── README ──────────────────────────────────────────────────────────────────
FILES = {"en": "README.md", "es": "README.es.md", "ca": "README.ca.md"}


def readme(lang):
    L = TXT[lang]

    def img(src, alt, href=None):
        tag = f'<img src="assets/{src}" width="100%" alt="{esc(alt)}" />'
        return f'<a href="{href}">{tag}</a>' if href else tag

    links = "\n  ".join(
        f'<a href="{REPO_URL}/{FILES[c]}"><img src="assets/lang-{c}-{"on" if c == lang else "off"}.svg" height="40" alt="{TXT[c]["name"]}" /></a>'
        for c in TXT)
    body = [f'<p align="right">\n  {links}\n</p>',
            img(f"cover-{lang}.svg", f'MONREAL. {L["meta"]}. {L["headline"]}'),
            img(f"letter-{lang}.svg", L["letter_title"])]
    for p in PROJECTS:
        href = p["link"][0] if p["link"] else None
        body.append(img(f'{p["key"]}-1-{lang}.svg', f'{p["name"]}. {p[lang]["headline"]}', href))
        body.append(img(f'{p["key"]}-2-{lang}.svg', f'{p["name"]}. {p[lang]["arch_caption"]}', href))
    body.append(img(f"back-{lang}.svg", L["back_title"], LINKEDIN[0]))
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
    extra = "".join(TXT[c]["date"](dt.date(2026, m, 28)) + TXT[c]["pct"](71.9) for c in TXT for m in range(1, 13))
    return walk([TXT, PROJECTS, LINKEDIN]) + SHORT["title"] + extra + "MONREAL"


def main():
    set_charset(_all_text())
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    out = {}
    for lang in TXT:
        out[f"cover-{lang}.svg"] = cover(lang)
        out[f"letter-{lang}.svg"] = letter(lang)
        for p in PROJECTS:
            out[f'{p["key"]}-1-{lang}.svg'] = feature_a(lang, p)
            out[f'{p["key"]}-2-{lang}.svg'] = feature_b(lang, p)
        out[f"back-{lang}.svg"] = back(lang)
        for on in (True, False):
            out[f"lang-{lang}-{'on' if on else 'off'}.svg"] = lang_link(lang, on)
        readme(lang)
    for name, content in out.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"{len(out)} SVGs · último Short: {SHORT['title']}")


if __name__ == "__main__":
    main()
