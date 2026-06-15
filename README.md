# Messaging Agent

## Vista general
Este proyecto es un simple proyecto Demo para explorar la libreria `claude_agent_sdk` de Claude.

El proyecto consiste en un bot simple de telegram el cual recibe input de un usuario y en base a el input puede utilizar MCPs para lo siguiente:

- Obsidian - Leer notas desde la boveda que se encuentra en el local host del usuario
- Google Calendar - Acceder a el Calendario de Google del usuario (necesita autenticacion manual primero)

Ademas de servir como un agente de proposito general, para hacer preguntas, agendar eventos, crear notas en obsidian, leer notas, etc...

## Estructura del proyecto

```
messaging-agent/
├── src/
│   ├── __init__.py
│   ├── main.py            # Punto de entrada
│   ├── telegram.py        # Manejador del bot de Telegram
│   ├── claude.py          # Agente de Claude
│   ├── mcp_servers.py     # Configuración de los servidores MCP
│   └── logging_config.py  # Configuración de los logs
├── credentials/
│   └── gcp-oauth.keys.json  # Credenciales OAuth de Google
├── .env                   # Variables de entorno (tokens, IDs)
├── pyproject.toml         # Metadatos y dependencias del proyecto
├── telegram.log           # Archivo de logs generado en ejecución
└── README.md
```

### Descripción de cada archivo

- **`src/main.py`** — Punto de entrada del proyecto. Configura el logging e inicia el bot.
- **`src/telegram.py`** — Conecta con Telegram. Recibe los mensajes del usuario, valida que provengan del usuario autorizado, se los pasa al agente y devuelve la respuesta ya formateada.
- **`src/claude.py`** — Define el agente de Claude. Configura las opciones (`ClaudeAgentOptions`), ejecuta la consulta con el SDK y registra el uso de herramientas y la respuesta.
- **`src/mcp_servers.py`** — Define los servidores MCP disponibles (Google Calendar y Obsidian) junto con sus credenciales y endpoints.
- **`src/logging_config.py`** — Configura el sistema de logs: archivo de salida, formato con fecha y silencia los logs ruidosos de las librerías (Telegram, httpx).
- **`credentials/gcp-oauth.keys.json`** — Credenciales OAuth de Google que usa el servidor MCP de Google Calendar.
- **`.env`** — Variables de entorno: token del bot de Telegram, ID del usuario autorizado y token de Obsidian.
- **`pyproject.toml`** — Metadatos del proyecto, dependencias y el comando `messaging-agent`.
- **`telegram.log`** — Archivo donde se guardan los logs durante la ejecución.

## Requerimientos

- [UV Package manager](https://docs.astral.sh/uv/)
- [Python > 3.14](https://www.python.org/downloads/)
- [Claude Code](https://claude.com/product/claude-code)
   - Subscripcion a una cuenta pro o max/API Key
- [Un bot de telegram y su API key](https://core.telegram.org/bots/tutorial)

### Opcional
Si quieres usar los MCPs configurados de momento (Calendar y Obsidian) necesitaras lo siguiente:

- Un proyecto de Google Cloud ([console.cloud.google.com](https://console.cloud.google.com/))
    - Una API key para Google Calendar
- Obsidian
    - Activar los Community plugins
    - Instalar el plugin "Local REST API with MCP" 

Una guia mas detallada para cada uno de los procesos:
- [Google Calendar MCP ](https://github.com/nspady/google-calendar-mcp)
- [Configuracion de Obsidian con MCPs ](https://github.com/coddingtonbear/obsidian-local-rest-api#mcp-clients)

## Como usar el proyecto

Clonar el repositorio.   
```shell
git clone https://github.com/NexWan/messaging-agent.git
```

Acceder al proyecto
```shell
cd messaging-agent
```

Instalar dependencias con uv sync
```shell
uv sync
```

Copia el .env.example a tu .env y configura las credenciales necesarias.
```shell
cp .env.example .env 

TELEGRAM_TOKEN=your-token
....
```

Inicializa el proyecto
```shell
uv run messaging-agent
```

## Usando Ollama

Se agrego soporte para Ollama para poder correr el bot con modelos LLM locales, sin necesidad de una cuenta de Claude.

Para poder usar Ollama, necesitaras lo siguiente:
- [Ollama ](https://ollama.com/)
- Un modelo de Ollama que soporte tools calling
    - [https://ollama.com/search?c=tools](https://ollama.com/search?c=tools)
- Correr tu modelo localmente
```shell
# Haz pull a tu modelo
ollama pull qwen3.5:9b # Ejemplo
# Correr tu modello
ollama run qwen3.5:9b

# Verifica que tu modelo este corriendo
ollama ps # Ver que modelos estan corriendo localmente en Ollama
```

- Configurar tus env variables
    - `OLLAMA_HOST` = host donde esta corriendo tu modelo (default=http://localhost:11434)
    - `OLLAMA_MODEL` = Modelo que descargaste para usar en ollama

Y listo, si quieres configurar ciertos elementos especificamente para tu modelo de Ollama, puedes modificar el archivo:
[strands.py](/messaging-agent/src/strands.py), aqui se encuentra toda la configuracion de el agente local utilizando [Strands Agents SDK de Amazon](https://strandsagents.com/docs/user-guide/quickstart/python/)
