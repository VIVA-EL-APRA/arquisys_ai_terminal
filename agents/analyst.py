"""
Agente 1 — Analista
Entiende la intención del usuario, detecta el tipo de diagrama
y señala si falta información crítica.
"""
import json
import re
from rich.console import Console
from core.api_client import OpenCodeClient
from core.session import DiagramSession

console = Console()


class AnalystAgent:

    SYSTEM = (
        "Eres el Agente Analista de ArquiSysAI. "
        "Tu única tarea es analizar solicitudes de diagramas y responder SOLO con JSON válido, "
        "sin markdown, sin texto extra, sin comillas adicionales.\n\n"
        "REGLAS:\n"
        "- Si la solicitud es muy GENERICA o VAGA (ej: 'diagrama bpmn de un restaurante', "
        "'haz un diagrama de un sistema de ventas'), NO asumas detalles que el usuario no dio.\n"
        "- En lugar de inventar procesos, entidades o actores, devuelve "
        'tiene_suficiente_info=false y una pregunta_faltante clara y CONCRETA '
        "que ayude al usuario a especificar.\n"
        "- La pregunta debe ser UTIL: pide detalles que realmente importan "
        "(procesos, actores, entidades, relaciones).\n"
        "- Si hay MULTIPLES aspectos faltantes, ofrece opciones numeradas.\n"
        "- Siempre incluye como ULTIMA opcion: 'O quieres que genere el diagrama a mi criterio?'\n"
        "- Si el usuario ya dio detalles suficientes, devuelve tiene_suficiente_info=true.\n\n"
        "Esquema de respuesta:\n"
        '{\n'
        '  "tipo_diagrama": "<uml-clase|uml-secuencia|uml-caso-uso|uml-flujo|bpmn|er|c4-contexto|c4-contenedor|arquitectura|desconocido>",\n'
        '  "tiene_suficiente_info": <true|false>,\n'
        '  "pregunta_faltante": "<pregunta detallada con opciones o null>",\n'
        '  "formato_sugerido": "<mermaid|plantuml>",\n'
        '  "confianza": "<alta|media|baja>",\n'
        '  "solicitud_enriquecida": "<descripción expandida de lo que hay que generar>"\n'
        "}"
    )

    def __init__(self):
        self.client = OpenCodeClient(model_key="default")

    def analyze(self, user_input: str, session: DiagramSession) -> dict:
        prompt = f'Solicitud: "{user_input}"'
        if session.forced_type:
            prompt += f'\nTipo forzado por el usuario: {session.forced_type}'
        if session.code_context:
            snippet = session.code_context[:1500]
            prompt += f'\n\nResumen del código fuente disponible:\n{snippet}'

        try:
            text = self.client.chat_text(
                messages=[
                    {"role": "system", "content": self.SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.1,
                max_tokens=400,
            )
            text = re.sub(r"```json|```", "", text).strip()
            return json.loads(text)
        except Exception:
            return {
                "tipo_diagrama":         session.forced_type or "desconocido",
                "tiene_suficiente_info": True,
                "pregunta_faltante":     None,
                "formato_sugerido":      session.export_format or "mermaid",
                "confianza":             "baja",
                "solicitud_enriquecida": user_input,
            }
