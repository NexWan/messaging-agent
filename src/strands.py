from strands import Agent
from strands.models.ollama import OllamaModel
from strands.types.exceptions import MaxTokensReachedException
import os
from .mcp_servers import MCP_SERVERS
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client
import logging
import json
from .claude import SYSTEM_PROMPT

class LocalAgent:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        ollama_model = OllamaModel(
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            model_id=os.getenv("OLLAMA_MODEL", ""),
            max_tokens=2048,
            temperature=0.6,
            options={
                "num_ctx": 16384,
                "presence_penalty": 0.0,
            },
            additional_args={"think": False},
        )
        self._configure_mcps()

        self.strands_agent = Agent(
            model=ollama_model,
            tools=[self.calendar_mcp_client, self.obsidian_mpc],
            system_prompt=SYSTEM_PROMPT
        )

    def _configure_mcps(self):
        calendar_mcp_settings = MCP_SERVERS.get("google-calendar", {})
        self.calendar_mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command=calendar_mcp_settings.get("command", ""),
                args=calendar_mcp_settings.get("args", []),
                env=calendar_mcp_settings.get("env")
            )
        ))
        obsidian_mcp_settings = MCP_SERVERS.get("obsidian", {})
        self.obsidian_mpc = MCPClient(lambda: streamablehttp_client(
            url=obsidian_mcp_settings.get("url", ""),
            headers=obsidian_mcp_settings.get("headers", {})
        ))

    def filter_event(self, event: dict) -> dict | None:
        """Filter streaming events to only forward relevant data over the wire."""
        # Forward text deltas for real-time display
        if "data" in event:
            return {"type": "text", "data": event["data"]}

        # Forward tool usage for progress indicators
        if "current_tool_use" in event and event["current_tool_use"].get("name"):
            return {"type": "tool", "name": event["current_tool_use"]["name"]}

        # Forward the final result
        if "result" in event:
            return {"type": "result", "stop_reason": str(event["result"].stop_reason)}

        # Skip everything else (lifecycle signals, raw deltas, reasoning, etc.)
        return None
    
    async def run_agent(self, user_message: str) -> str:
        agent_response = ""

        try:
            async for event in self.strands_agent.stream_async(user_message):
                filtered = self.filter_event(event)
                if filtered:
                    self.logger.info("AI logs: %s", json.dumps(filtered))

                # Accumulate text deltas into the final response
                if filtered and filtered["type"] == "text":
                    agent_response += filtered["data"]
        except MaxTokensReachedException:
            # The model exhausted its token budget mid-response. Don't crash the
            # handler; return whatever text we have plus a friendly note.
            self.logger.warning("Agent hit max_tokens; returning partial response")
            note = "\n\n(Me quedé sin espacio para responder. ¿Puedes reformular o acotar tu pregunta?)"
            return (agent_response + note) if agent_response else note.strip()

        return agent_response
                
                


