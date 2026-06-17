import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".arquisys-ai.env")

# ── API OpenCode Zen ────────────────────────────────────────────────
OPENCODE_API_KEY  = os.getenv("OPENCODE_API_KEY", "")
OPENCODE_BASE_URL = "https://opencode.ai/zen/v1"

AVAILABLE_MODELS = {
    "north":    "north-mini-code-free",
    "nemotron": "nemotron-3-ultra-free",
    "minimax":  "minimax-m3-free",
    "default":  "north-mini-code-free",
}

FREE_MODEL_MARKERS = ("free", "gratis")

# ── App ────────────────────────────────────────────────────────────
APP_NAME    = "ArquiSysAI"
APP_VERSION = "5.0.0"

# ── Sesión ─────────────────────────────────────────────────────────
MAX_HISTORY = 20
SESSION_DIR = "sessions"

# ── Diagramas ──────────────────────────────────────────────────────
OUTPUT_DIR     = "output_diagrams"
DEFAULT_FORMAT = "mermaid"   # "mermaid" | "plantuml"
MAX_VALIDATION_ITERATIONS = 3

SUPPORTED_DIAGRAM_TYPES = [
    "uml-clase", "uml-secuencia", "uml-caso-uso", "uml-flujo",
    "bpmn", "er", "c4-contexto", "c4-contenedor", "arquitectura",
]

RECOMMENDED_FORMAT_BY_TYPE = {
    "uml-caso-uso": "plantuml",
    "bpmn":         "mermaid",
}

# ── Exportación PNG ────────────────────────────────────────────────
# Servidor público PlantUML para renderizar PNG
PLANTUML_SERVER = "https://www.plantuml.com/plantuml"
# Servidor Mermaid.ink para renderizar PNG
MERMAID_INK_URL = "https://mermaid.ink"
# Kroki como fallback para Mermaid y PlantUML
KROKI_URL = "https://kroki.io"
