# ArquiSysAI

**IA Agéntica para generación de diagramas técnicos**

ArquiSysAI es una herramienta de inteligencia artificial agéntica que genera diagramas técnicos (UML, BPMN, ER, C4, Arquitectura) a partir de descripciones en lenguaje natural. Utiliza un sistema multi-agente con agentes analista, arquitecto y validador para producir diagramas precisos y bien formateados.

## Características

- **Múltiples tipos de diagrama**: UML (clase, secuencia, caso de uso, flujo), BPMN, ER, C4 (contexto, contenedor), Arquitectura
- **Sistema multi-agente**: Analista, Arquitecto y Validador trabajan en conjunto
- **Formato Mermaid y PlantUML**: Elige el formato que prefieras
- **Exportación a PNG**: Renderiza tus diagramas como imágenes
- **Interfaz TUI**: Terminal interactiva con historial de sesiones
- **Multi-diagrama**: Genera varios diagramas en una misma sesión

## Instalación

### Requisitos previos

- **Node.js** v16 o superior
- **Python** 3.10 o superior
- **pip** (gestor de paquetes de Python)

### Instalación global vía npm

```bash
npm install -g arquisys-ai
```

Esto instalará el paquete y ejecutará el script de configuración automáticamente.

### Configuración de API Key

1. Obtén una API key gratuita en [https://opencode.ai](https://opencode.ai)
2. El instalador crea automáticamente un archivo de configuración en `~/.arquisys-ai.env`
3. Edita ese archivo y reemplaza `sk-placeholder-requires-setup` con tu API key:

```
OPENCODE_API_KEY=tu-api-key-aqui
```

### Instalación manual (sin npm)

```bash
# Clonar el repositorio
git clone https://github.com/VIVA-EL-APRA/arquisys_ai_terminal.git
cd arquisys_ai_terminal

# Instalar dependencias de Python
pip install -r requirements.txt

# Crear archivo de configuración
copy %USERPROFILE%\.arquisys-ai.env
# O en Linux/Mac: cp /dev/null ~/.arquisys-ai.env
# Luego edita el archivo y agrega tu OPENCODE_API_KEY
```

## Uso

```bash
arquisys-ai
```

O si clonaste el repositorio manualmente:

```bash
python main.py
```

### Comandos disponibles en la TUI

| Comando | Descripción |
|---------|-------------|
| `/diagrama` | Generar un nuevo diagrama |
| `/modelo <nombre>` | Cambiar el modelo de IA |
| `/formato <mermaid\|plantuml>` | Cambiar el formato de salida |
| `/<tipo>` | Especificar tipo de diagrama (uml-clase, bpmn, er, etc.) |
| `/multi` | Activar modo multi-diagrama |
| `/historial` | Ver historial de la sesión |
| `/exportar` | Exportar diagrama a PNG |
| `/ayuda` | Mostrar ayuda |
| `/salir` | Salir de la aplicación |

## Estructura del proyecto

```
arquisys_ai_terminal/
├── agents/           # Agentes de IA (analista, arquitecto, validador)
├── core/             # Núcleo (cliente API, orquestador, renderizador, sesión)
├── tools/            # Herramientas (comandos, entrada de contexto, multi-diagrama)
├── ui/               # Interfaz de usuario (TUI)
├── cli.js            # Entry point de Node.js
├── setup.js          # Script de configuración post-instalación
├── main.py           # Entry point de Python
├── config.py         # Configuración de la aplicación
├── package.json      # Configuración del paquete npm
└── requirements.txt  # Dependencias de Python
```

## Modelos disponibles

| Alias | Modelo |
|-------|--------|
| `hy3` | hy3-preview-free |
| `nemotron` | nemotron-3-super-free |
| `minimax` | minimax-m2.5-free |
| `default` | minimax-m2.5-free |

## Licencia

MIT
