from pathlib import Path
import os
from dotenv import load_dotenv
from claude_agent_sdk import McpServerConfig

load_dotenv()
# Absolute path to the Google OAuth credentials, resolved from this file's
# location so it works regardless of the bot's working directory.
GOOGLE_OAUTH_CREDENTIALS = str(
    Path(__file__).resolve().parent.parent / "credentials" / "gcp-oauth.keys.json"
)

OBSIDIAN_BEARER_TOKEN = os.getenv("OBSIDIAN_BEARER_TOKEN")

MCP_SERVERS:dict[str, McpServerConfig]  = {
    "google-calendar": {
        "command": "npx",
        "args": ["@cocal/google-calendar-mcp"],
        "env": {"GOOGLE_OAUTH_CREDENTIALS": GOOGLE_OAUTH_CREDENTIALS},
    },
    "obsidian": {
        "type": "http",
        "url": "http://127.0.0.1:27123/mcp/",
        "headers": {
            "Authorization": f"Bearer {OBSIDIAN_BEARER_TOKEN}"
        },
    },
}
