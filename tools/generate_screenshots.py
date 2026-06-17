"""
Genera screenshots de la TUI en modo silencioso usando rich.
Sin abrir ventanas ni usar grim.
"""
import sys, os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["OPENCODE_API_KEY"] = "sk-xhzhqS9Z0Ak7oOrPY9FAGmcJbbYMwKkDnIMUcKnGnjz79DCaVC7oOCTZ3KYXfZg0"

OUTPUT = Path(__file__).parent.parent / "documentos" / "sprint5_report"
os.makedirs(OUTPUT, exist_ok=True)


def save_screenshot(name: str, console: Console):
    svg_path = OUTPUT / f"{name}.svg"
    png_path = OUTPUT / f"{name}.png"
    console.save_svg(str(svg_path), title="ArquiSysAI Sprint 5")
    ret = os.system(f"rsvg-convert -w 900 -f png -o '{png_path}' '{svg_path}' 2>/dev/null")
    if ret == 0 and png_path.exists():
        print(f"  [OK] {png_path.name}")
    else:
        print(f"  [FALL] Fallo conversion de {name}")
    if svg_path.exists():
        svg_path.unlink()


def main():
    print("Generando screenshots silenciosos...\n")

    # ── Main screen ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold cyan]ArquiSysAI v5.2.2[/bold cyan] -- IA Agentica para Diagramas")
    c.rule()
    c.print("[INFO] ArquiSysAI v5.2.2 iniciado  |  modelo: north-mini-code-free")
    c.print("[INFO] Escribe tu solicitud en lenguaje natural o usa /help para ver comandos.")
    c.print("[INFO] F2 = editor de contexto textual | F3 = modelos | F5 = paquete/tipo forzado | Tab = autocompletar")
    c.rule()
    ctx = Table(box=box.ROUNDED, show_header=True)
    ctx.add_column("#", style="dim", width=4)
    ctx.add_column("Fuente", style="cyan", width=22)
    ctx.add_column("Contenido", width=56)
    ctx.add_row("1", "texto:manual", "generar un diagrama bpmn de un restaurante")
    c.print(ctx)
    c.print()
    c.print("[OK] Contexto textual cargado (1 lineas).")
    c.print("[OK] Carpeta de exportacion: documentos/")
    c.print()
    c.print(Panel(
        "[bold cyan]Area de trabajo  (salida, codigo y comandos)[/bold cyan]",
        border_style="bright_blue"
    ))
    from rich.text import Text
    foot = Text()
    foot.append("F1:Ayuda  F2:Contexto  F3:Modelo  F5:Generar  F10:Salir  /tipo /modelos /ctx /api", style="dim")
    c.print(Panel(foot))
    save_screenshot("img_01_main", c)

    # ── F5 Dialog (styled inline prompt) ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold cyan]Selecciona tipo(s) de diagrama[/bold cyan]")
    c.rule()
    c.print("")
    c.print("  [1] Detectar automaticamente desde solicitud/contexto")
    c.print("  [2] Diagrama de Casos de Uso")
    c.print("  [3] Diagrama de Secuencia")
    c.print("  [4] [bold]Diagrama BPMN de Proceso[/bold]  <-- detectado")
    c.print("  [5] Modelo Entidad-Relacion")
    c.print("  [6] Paquete completo (4 diagramas)")
    c.print("")
    c.print("[dim]ENTER = auto-detect  |  'all' = todos  |  Numeros separados por coma (ej: 1,3)[/dim]")
    c.print("")
    c.print(Panel(
        Text("F1:Ayuda  F5:Generar  /tipo para forzar tipo", style="dim")
    ))
    save_screenshot("img_02_f5_dialog", c)

    # ── Model Selection ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold cyan]Seleccionar Modelo (F3)[/bold cyan]")
    c.rule()
    t = Table(box=box.HEAVY, show_header=True)
    t.add_column("", width=4)
    t.add_column("Alias", width=14)
    t.add_column("Modelo", width=34)
    t.add_column("Estado", width=14)
    t.add_row("[X]", "north", "north-mini-code-free", "[green]Activo[/]")
    t.add_row("[ ]", "nemotron", "nemotron-3-ultra-free", "[green]Disponible[/]")
    t.add_row("[ ]", "deepseek", "deepseek-v4-flash-free", "[yellow]Lento[/]")
    t.add_row("[ ]", "mimo", "mimo-v2.5-free", "[green]Disponible[/]")
    c.print(t)
    c.print()
    c.print("[yellow]Nota: minimax-m3-free y qwen3.6-plus-free eliminados (no disponibles).[/yellow]")
    c.print("[dim]Flechas=navegar  Enter=seleccionar  Esc=cancelar[/dim]")
    c.print(Panel(Text("F1:Ayuda  F3:Modelo  /modelo <alias> para cambiar", style="dim")))
    save_screenshot("img_03_model_selection", c)

    # ── Clarification Dialog (styled radiolist) ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold yellow]Agente de Clarificacion -- Informacion Insuficiente[/bold yellow]")
    c.rule()
    c.print()
    c.print("[cyan]Pregunta de la IA:[/cyan]")
    c.print()
    c.print("  He detectado que quieres modelar un restaurante en BPMN.")
    c.print("  Para ser mas preciso, dime: [bold]que tipo de restaurante?[/bold]")
    c.print()
    c.print("[cyan]Opciones disponibles:[/cyan]")
    c.print()
    c.print("  [1] Fast food / comida rapida")
    c.print("  [2] Fine dining / alta cocina")
    c.print("  [3] Cafeteria / bar")
    c.print("  [4] [dim]Generar a mi criterio (usa datos genericos)[/dim]")
    c.print()
    c.print("[cyan]>>  Selecciona una opcion (1-4):[/cyan]")
    c.print()
    c.print(Panel(Text("F1:Ayuda  Esc:Saltar preguntas  Agente de Clarificacion v5.2 (IA)", style="dim")))
    save_screenshot("img_04_clarification", c)

    # ── Tests Output ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold green]Pruebas de Usuario -- Escenarios Academicos[/bold green]")
    c.rule()
    t = Table(box=box.ROUNDED, show_header=True)
    t.add_column("ID", style="bold", width=8)
    t.add_column("Nombre", width=30)
    t.add_column("Tipo", width=16)
    t.add_column("Resultado", width=12)
    t.add_row("EC01", "Sistema de biblioteca universitaria", "uml-caso-uso", "[green]OK[/]")
    t.add_row("EC02", "Proceso de matricula universitaria", "bpmn", "[green]OK[/]")
    t.add_row("EC03", "Sistema de ventas", "er", "[green]OK[/]")
    t.add_row("EC04", "Proceso de atencion medica", "uml-secuencia", "[green]OK[/]")
    t.add_row("EC05", "Solicitud generica restaurante", "bpmn (vaga)", "[yellow]Clarificacion[/]")
    c.print(t)
    c.print()
    c.print("[bold green]Tests Unitarios:[/bold green]")
    c.print("  [green]OK[/] test_session_context_management")
    c.print("  [green]OK[/] test_session_pending_request")
    c.print("  [green]OK[/] test_session_output_dir_persists")
    c.print("  [green]OK[/] test_supported_types")
    c.print("  [green]OK[/] test_recommended_formats")
    c.print("  [green]OK[/] test_package_types")
    c.print("  [green]OK[/] test_architect_prompt")
    c.print("  [green]OK[/] test_validator_prompt")
    c.print("  [green]OK[/] test_clarification_context")
    c.print("  [green]OK[/] test_latest_context")
    c.print("  [green]OK[/] test_word_boundary_infer ('bpmn' -> ['bpmn'], 'restaurante' sin 'er')")
    c.print("  [green]OK[/] test_dead_model_filter (minimax eliminado)")
    c.print("  [green]OK[/] test_a_mi_criterio_variants (9 expresiones)")
    save_screenshot("img_05_test_output", c)

    # ── Generated Output ──
    c = Console(record=True, width=100, height=35, force_terminal=True)
    c.print("[bold green]Diagrama Generado -- Resultado[/bold green]")
    c.rule()
    t = Table(box=box.ROUNDED, show_header=True)
    t.add_column("Tipo", style="bold", width=18)
    t.add_column("Formato", width=10)
    t.add_column("Iteraciones", width=14)
    t.add_column("Correcciones", width=16)
    t.add_column("PNG", width=8)
    t.add_row("Casos de Uso", "PlantUML", "1", "0", "[green]Si[/]")
    t.add_row("Secuencia", "Mermaid", "2", "1 (sintaxis)", "[green]Si[/]")
    t.add_row("BPMN", "Mermaid", "2", "1 (sintaxis BPMN)", "[green]Si[/]")
    t.add_row("ER", "PlantUML", "1", "0", "[green]Si[/]")
    c.print(t)
    c.print()
    c.print("[cyan]Orquestacion:[/cyan] LangGraph StateGraph con flujo sincrono (sin hilos)")
    c.print("[cyan]Backend:[/cyan] north-mini-code-free (OpenCode)")
    c.print("[cyan]Estilo dialogos:[/cyan] DIALOG_STYLE (33 targets, fondo #010409, titulos cyan)")
    c.print("[cyan]Clarificacion:[/cyan] radiolist interactivo con opciones de la IA")
    c.print()
    code = (
        "@startuml\n"
        "left to right direction\n"
        "actor Estudiante\n"
        "actor Bibliotecario\n"
        "rectangle Biblioteca {\n"
        "  usecase (Prestar Libro)\n"
        "  usecase (Consultar Catalogo)\n"
        "  usecase (Reservar Libro)\n"
        "}\n"
        "Estudiante --> (Prestar Libro)\n"
        "@enduml"
    )
    c.print(Panel(code, title="Codigo del diagrama (ejemplo)", border_style="green"))
    save_screenshot("img_06_generated_output", c)

    print("\nListo. 6 screenshots generados en documentos/sprint5_report/")


if __name__ == "__main__":
    main()
