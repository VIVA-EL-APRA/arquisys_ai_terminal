"""
Generación silenciosa de diagramas de muestra para el informe Sprint 5.
Usa el pipeline completo (Analista -> Arquitecto -> Validador -> Render).
No requiere interacción TUI.
"""
import sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["OPENCODE_API_KEY"] = "sk-xhzhqS9Z0Ak7oOrPY9FAGmcJbbYMwKkDnIMUcKnGnjz79DCaVC7oOCTZ3KYXfZg0"
os.environ["ARQUISYS_MODEL"] = "north-mini-code-free"

from rich.console import Console
from core.session import DiagramSession
from agents.architect import ArchitectAgent
from agents.validator import ValidatorAgent
from tools.multi_diagram import PACKAGE_TYPES, _run_package
from config import AVAILABLE_MODELS

console = Console()
OUTPUT_DIR = Path("documentos/sprint5_report")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    session = DiagramSession()
    session.output_dir = str(OUTPUT_DIR)
    session.output_dir_confirmed = True
    session.export_format = "mermaid"
    session.forced_type = None

    # Contexto de ejemplo académico
    session.add_code_context(
        "Sistema de gestión universitaria. "
        "Actores: Estudiante, Profesor, Administrador, Bibliotecario. "
        "Procesos: matrícula, registro de cursos, gestión de biblioteca, pagos. "
        "Entidades: Estudiante, Curso, Matricula, Pago, Libro, Prestamo. "
        "El sistema debe permitir a estudiantes matricularse, consultar notas, "
        "reservar libros; a profesores registrar notas y cursos; "
        "a administradores gestionar usuarios y pagos.",
        "contexto-academico"
    )
    session.add_code_context(
        "La universidad tiene 3 facultades: Ingenieria, Ciencias, Letras. "
        "Cada facultad tiene sus propios cursos. "
        "Los estudiantes pueden pertenecer a una sola facultad. "
        "El año academico se divide en 2 semestres.",
        "contexto-universidad"
    )

    architect = ArchitectAgent()
    validator = ValidatorAgent()
    # Refresh model list and pick a working free model
    for agent in [architect, validator]:
        registry = agent.client.refresh_free_models()
        for alias in ["north", "nemotron", "deepseek", "mimo", "minimax"]:
            if alias in registry:
                agent.client.switch_model(alias, registry)
                print(f"  {type(agent).__name__} usando: {registry.get(alias)} (alias: {alias})")
                break

    logger = lambda level, msg: print(f"[{level.upper()}] {msg}")
    code_logger = lambda label, code, dtype: None

    console.rule("[cyan]Generando diagramas de muestra - Sprint 5[/cyan]")
    results = _run_package(session, architect, validator, PACKAGE_TYPES, logger, code_logger)

    console.print("\n[green]Resumen final:[/green]")
    for r in results:
        status = "✓" if r.get("png") else "✗"
        console.print(f"  {status} {r['label']:40} PNG: {r.get('png','ERROR')}")

if __name__ == "__main__":
    main()
