import logging

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, StreamEvent
from .mcp_servers import MCP_SERVERS



SYSTEM_PROMPT = """\
Eres un asistente general amigable y cercano que vive dentro de Telegram.
Tu objetivo es ayudar al usuario con cualquier pregunta o tarea que tenga, desde preguntas cotidianas hasta temas más complejos.

## Personalidad
- Usa un tono casual y amigable, como si fuera una conversación con un amigo inteligente
- Puedes usar emojis ocasionalmente para darle vida a las respuestas, pero sin exagerar
- Sé empático y muéstrate genuinamente interesado en ayudar

## Idioma
- Responde SIEMPRE en español, sin importar el idioma en que te escriban
- Usa un español natural y latinoamericano, evita sonar demasiado formal o rígido

## Contexto de la conversación
- Recuerda lo que se ha hablado anteriormente en la conversación y haz referencia a ello cuando sea relevante
- Si el usuario menciona algo sobre sí mismo (nombre, preferencias, situación), tenlo en cuenta para el resto de la conversación

## Formato
- Estás en Telegram, así que usa Markdown con moderación
- Para respuestas largas, usa listas o secciones cortas para que sea fácil de leer en móvil
- Evita respuestas innecesariamente largas; sé directo pero completo
"""


class ClaudeAgent:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.options = ClaudeAgentOptions(
            system_prompt=SYSTEM_PROMPT,
            allowed_tools=["Read", "Bash", "mcp__google-calendar__*", "mcp__obsidian__*"],
            permission_mode="bypassPermissions",
            include_partial_messages=True,
            mcp_servers=MCP_SERVERS
        )

    async def run_agent(self, user_message: str) -> str:
        agent_response = ""
        in_tool = False

        async for agent_message in query(prompt=user_message, options=self.options):
            if isinstance(agent_message, ResultMessage):
                if agent_message.subtype == "success":
                    agent_response = agent_message.result or ""

            elif isinstance(agent_message, StreamEvent):
                event = agent_message.event

                match event.get("type", ""):
                    case "content_block_start":
                        content_block = event.get("content_block", {})
                        if content_block.get("type") == "tool_use":
                            self.logger.info("Using tool %s...", content_block.get("name", ""))
                            in_tool = True

                    case "content_block_stop":
                        if in_tool:
                            self.logger.info("Tool usage done")
                            in_tool = False

        self.logger.info("Claude response: %s", agent_response)
        return agent_response
