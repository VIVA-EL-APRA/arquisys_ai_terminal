# ArquiSysAI — Instrucciones para el agente

## Versionado

- Usar **versionado semántico pero conservador**: `5.X.X`
- Para bugs/correcciones menores: subir el **patch** (`5.1.0` → `5.1.1`)
- Para features nuevas: subir el **minor** (`5.1.0` → `5.2.0`)
- **NO** subir major (`6.0.0`) a menos que sea un cambio realmente grande
- Mantener sincronizados `package.json` (npm) y `config.py` (`APP_VERSION`)
- Después de cada commit con cambios funcionales: `npm publish`

## Publicación

- `git add`, `git commit`, `git push origin main`
- `npm publish` (requiere token en `~/.npmrc`)
- Versión de npm determinada por `package.json`

## Convenciones de código

- `agents/analyst.py`: Agente Analista — detecta tipo de diagrama, valida contexto, genera preguntas clarificadoras via IA
- `agents/architect.py`: Agente Arquitecto — genera código Mermaid/PlantUML
- `agents/validator.py`: Agente Validador — corrige sintaxis del diagrama
- `core/orchestrator.py`: Pipeline de generación con LangGraph
- `ui/tui.py`: Interfaz TUI con prompt_toolkit
- Los prompts de agentes se construyen en `core/session.py`

## Modelos

- Los modelos gratuitos cambian frecuentemente. Usar `refresh_free_models()` del `OpenCodeClient`
- Modelos funcionales actuales (jun 2026): `north-mini-code-free`, `nemotron-3-ultra-free`, `deepseek-v4-flash-free`
- Actualizar `AVAILABLE_MODELS` en `config.py` si un modelo deja de funcionar

## Reportes

- Los informes Sprint se generan via `tools/generate_sprint*_report.py`
- Las capturas de pantalla se generan en **modo silencioso** con Rich (SVG → PNG via `rsvg-convert`), sin abrir ventanas TUI
- Scripts de generación: `tools/generate_screenshots.py`
