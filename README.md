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

## Requisitos previos

- **Node.js** v16 o superior
- **Python** 3.10 o superior
- **pip** (gestor de paquetes de Python)

## Descarga e instalación

### Opción 1: Instalación vía npm (recomendada)

```bash
npm install -g arquisys-ai
```

Esto instalará el paquete globalmente y ejecutará el script de configuración automáticamente.

### Opción 2: Instalación manual desde GitHub

```bash
# Clonar el repositorio
git clone https://github.com/VIVA-EL-APRA/arquisys_ai_terminal.git

# Entrar al directorio
cd arquisys_ai_terminal

# Instalar dependencias de Python
pip install -r requirements.txt
```

## Configuración de API Key

1. Obtén una API key gratuita en [https://opencode.ai](https://opencode.ai) (crea una cuenta gratis)
2. Crea el archivo de configuración en tu carpeta de usuario:

   **Windows:**
   ```bash
   copy nul %USERPROFILE%\.arquisys-ai.env
   ```

   **Linux / Mac:**
   ```bash
   touch ~/.arquisys-ai.env
   ```

3. Abre el archivo `C:\Users\TuUsuario\.arquisys-ai.env` (Windows) o `~/.arquisys-ai.env` (Linux/Mac) y agrega:

   ```
   OPENCODE_API_KEY=tu-api-key-aqui
   ```

   Reemplaza `tu-api-key-aqui` por la API key que obtuviste en opencode.ai.

## Iniciar el sistema

### Si instalaste vía npm:

```bash
arquisys-ai
```

### Si clonaste el repositorio manualmente:

```bash
python main.py
```

### Si instalaste vía npm pero no funciona el comando:

```bash
npx arquisys-ai
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
