import os
import json
import asyncio
import subprocess
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from smolagents import tool

# Configuration for the Playwright MCP Server
PLAYWRIGHT_MCP_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@playwright/mcp@latest", "--headless"],
    env=os.environ.copy()
)

@tool
def playwright_mcp(action: str, params: dict = None) -> str:
    """
    Executes an action using the Playwright MCP Server.
    Available actions: navigate, click, type, fill, screenshot, take_snapshot.
    Args:
        action: The MCP tool name to call.
        params: Dictionary of parameters for the tool.
    """
    async def run():
        try:
            async with stdio_client(PLAYWRIGHT_MCP_PARAMS) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    if action == "list_tools":
                        tools = await session.list_tools()
                        return str(tools)
                    
                    result = await session.call_tool(action, params or {})
                    return str(result.content)
        except Exception as e:
            return f"MCP Error: {e}"

    return asyncio.run(run())

@tool
def fill_web_form(url: str, fields: dict) -> str:
    """
    Navigates to a URL and fills out a form with the provided data.
    Args:
        url: The target website URL.
        fields: A dictionary mapping element selectors/labels to values.
    """
    nav = playwright_mcp("navigate", {"url": url})
    fill = playwright_mcp("fill", fields)
    return f"Navigation: {nav}\nFill: {fill}"