"""
Agente 1 — Analista
Entiende la intención del usuario, detecta el tipo de diagrama,
valida el contexto cargado y genera preguntas clarificadoras
inteligentes usando la IA.
"""
import json
import re
from rich.console import Console
from core.api_client import OpenCodeClient
from core.session import DiagramSession

console = Console()


class AnalystAgent:

    SYSTEM = (
        "Eres el Agente Analista de ArquiSysAI, un sistema de generacion de diagramas tecnicos. "
        "Tu unica tarea es analizar la solicitud del usuario y el contexto disponible, "
        "y responder SOLO con JSON valido, sin markdown, sin texto extra.\n\n"
        "TUS RESPONSABILIDADES:\n"
        "1. DETECTAR EL TIPO DE DIAGRAMA: Examina la solicitud y el contexto para determinar "
        "que tipo de diagrama corresponde. Usa palabras clave en el texto (entidad, relacion, "
        "tablas -> ER; actor, caso de uso -> Casos de Uso; secuencia, interaccion, mensaje -> "
        "Secuencia; proceso, flujo de trabajo, BPMN -> BPMN; clase, objeto, atributo -> Clase; "
        "arquitectura, sistema, componente -> Arquitectura/C4). Si no es claro, usa 'desconocido'.\n\n"
        "2. VALIDAR EL CONTEXTO: Revisa si el contexto cargado tiene sentido.\n"
        "   - Si NO HAY contexto: incluye en pregunta_faltante que el usuario debe cargar contexto "
        "primero (via /ctx, /read, o /carpeta) y especificar que quiere modelar.\n"
        "   - Si el contexto es INSUFICIENTE o VAGO (ej: solo 'sistema de ventas' sin mas detalle): "
        "pregunta especificamente que procesos, entidades o actores quiere incluir.\n"
        "   - Si el contexto esta en blanco, es irrelevante o no tiene sentido: indica "
        "'El contexto cargado no es util para generar un diagrama' en pregunta_faltante.\n\n"
        "3. GENERAR PREGUNTAS INTELIGENTES: No uses preguntas genericas. Analiza el contexto "
        "y la solicitud REAL y formula preguntas ESPECIFICAS sobre lo que falta. "
        "Por ejemplo, si el contexto menciona 'restaurante' pero no dice procesos, pregunta "
        "'He visto que el contexto habla de un restaurante. 'Que procesos especificos quieres "
        "modelar?: 1) Toma de pedidos, 2) Preparacion de platos, 3) Facturacion, 4) Gestion "
        "de inventario, 5) Reservas?'. "
        "Usa el vocabulario y dominio del contexto para hacer las preguntas relevantes.\n\n"
        "4. Siempre incluye como ULTIMA opcion: 'O quieres que genere el diagrama a mi criterio?' "
        "(en la lista de opciones_clarificacion).\n"
        "5. Si la informacion es suficiente, devuelve tiene_suficiente_info=true y "
        "pregunta_faltante=null.\n\n"
        "6. OPCIONES INTERACTIVAS: En lugar de solo texto en 'pregunta_faltante', debes generar "
        "una lista de opciones_clarificacion que son POSIBLES RESPUESTAS que el usuario puede "
        "elegir interactivamente. El sistema mostrara estas opciones como una lista seleccionable.\n"
        "   - Cada opcion debe ser una frase completa, clara y util.\n"
        "   - Las opciones deben ser sugerencias INTELIGENTES basadas en el contexto y la solicitud.\n"
        "   - Ejemplo para restaurante: ['Modelar solo el proceso de toma de pedidos', "
        "'Modelar la preparacion de alimentos y facturacion', 'Modelar todo el flujo del restaurante']\n"
        "   - Siempre incluir como ultima opcion: 'Generar el diagrama a mi criterio'\n"
        "   - Minimo 2 opciones, maximo 6.\n\n"
        "Esquema de respuesta:\n"
        '{\n'
        '  "tipo_diagrama": "<uml-clase|uml-secuencia|uml-caso-uso|uml-flujo|bpmn|er|c4-contexto|c4-contenedor|arquitectura|desconocido>",\n'
        '  "tiene_suficiente_info": <true|false>,\n'
        '  "pregunta_faltante": "<pregunta detallada generada por IA o null>",\n'
        '  "opciones_clarificacion": ["<opcion 1>", "<opcion 2>", ...] o null,\n'
        '  "formato_sugerido": "<mermaid|plantuml>",\n'
        '  "confianza": "<alta|media|baja>",\n'
        '  "solicitud_enriquecida": "<descripcion expandida de lo que hay que generar>"\n'
        "}"
    )

    def __init__(self):
        self.client = OpenCodeClient(model_key="default")

    def analyze(self, user_input: str, session: DiagramSession) -> dict:
        prompt = f'Solicitud del usuario: "{user_input}"'
        if session.forced_type:
            prompt += f'\nTipo forzado por el usuario: {session.forced_type}'

        ctx = session.code_context.strip()
        if ctx:
            snippet = ctx[:2000]
            prompt += f'\n\nContexto cargado por el usuario:\n{snippet}'
        else:
            prompt += '\n\nContexto: NO HAY CONTEXTO CARGADO. El usuario no ha proporcionado codigo ni descripcion del sistema.'

        # List all clarification rounds already done
        aclaraciones = [e for e in session.context_entries if e.get("source") == "aclaracion-usuario"]
        if aclaraciones:
            prompt += '\n\nAclaraciones previas del usuario:\n'
            for i, e in enumerate(aclaraciones, 1):
                prompt += f"{i}. {e['content']}\n"

        try:
            text = self.client.chat_text(
                messages=[
                    {"role": "system", "content": self.SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                max_tokens=500,
            )
            text = re.sub(r"```json|```", "", text).strip()
            return json.loads(text)
        except Exception as e:
            console.print(f"[yellow]Analyst fallback: {e}[/yellow]")
            return {
                "tipo_diagrama":         session.forced_type or "desconocido",
                "tiene_suficiente_info": True,
                "pregunta_faltante":     None,
                "formato_sugerido":      session.export_format or "mermaid",
                "confianza":             "baja",
                "solicitud_enriquecida": user_input,
            }
