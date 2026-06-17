"""Genera un diagrama ER en PlantUML (que se renderiza mejor que mermaid ER)."""
import sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["OPENCODE_API_KEY"] = "sk-xhzhqS9Z0Ak7oOrPY9FAGmcJbbYMwKkDnIMUcKnGnjz79DCaVC7oOCTZ3KYXfZg0"

from rich.console import Console
from core.session import DiagramSession
from agents.architect import ArchitectAgent
from agents.validator import ValidatorAgent
from core.orchestrator import generate_validated_diagram
from core.renderer import save_diagram

console = Console()
OUTPUT_DIR = Path("documentos/sprint5_report")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    session = DiagramSession()
    session.output_dir = str(OUTPUT_DIR)
    session.output_dir_confirmed = True
    session.export_format = "plantuml"  # Force PlantUML for ER
    session.forced_type = "er"

    session.add_code_context(
        "Sistema de gestión universitaria. Entidades: Estudiante (id, nombre, email, facultad_id), "
        "Curso (id, titulo, creditos, facultad_id), Profesor (id, nombre, email, facultad_id), "
        "Facultad (id, nombre), Matricula (id, estudiante_id, curso_id, semestre, fecha, estado), "
        "Pago (id, estudiante_id, monto, fecha, estado). "
        "Un Estudiante pertenece a una Facultad. Un Curso pertenece a una Facultad. "
        "Un Profesor pertenece a una Facultad. "
        "Un Estudiante se matricula en muchos Cursos via Matricula. "
        "Un Estudiante realiza muchos Pagos.",
        "contexto-er"
    )

    architect = ArchitectAgent()
    validator = ValidatorAgent()

    for agent in [architect, validator]:
        registry = agent.client.refresh_free_models()
        for alias in ["north", "nemotron", "deepseek", "mimo"]:
            if alias in registry:
                agent.client.switch_model(alias, registry)
                print(f"  {type(agent).__name__} usando: {registry.get(alias)}")
                break

    analysis = {
        "tipo_diagrama": "er",
        "tiene_suficiente_info": True,
        "pregunta_faltante": None,
        "formato_sugerido": "plantuml",
        "confianza": "alta",
        "solicitud_enriquecida": (
            "Genera un diagrama Entidad-Relación en PlantUML. "
            "Usa sintaxis PlantUML con entidades y relaciones claras. "
            "Entidades: Estudiante, Curso, Profesor, Facultad, Matricula, Pago."
        ),
    }

    prompt = analysis["solicitud_enriquecida"]
    result = generate_validated_diagram(
        prompt, session, analysis, architect, validator,
        logger=lambda l, m: print(f"[{l}] {m}"),
        error_handler=lambda m: print(f"[ERR] {m}"),
    )

    if result.code:
        saved = save_diagram(result.code, result.dtype, "er", output_dir=str(OUTPUT_DIR))
        print(f"Texto: {saved['text']}")
        if saved["png"]:
            print(f"PNG: {saved['png']}")
        else:
            print(f"PNG Error: {saved.get('error', 'N/A')}")
    else:
        print("No se generó código.")

if __name__ == "__main__":
    main()
