"""
IACR MCP Server
==============

This module implements an MCP server for interacting with the IACR Cryptology ePrint Archive.
"""

import logging
import mcp.types as types
from typing import Dict, Any, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from mcp.server.stdio import stdio_server
from .config import Settings
from .tools import (
    handle_search, search_tool,
    handle_get_paper_details, get_paper_details_tool,
    handle_download_paper, download_paper_tool
)

settings = Settings()
logger = logging.getLogger("iacr-mcp-server")
logger.setLevel(logging.INFO)
server = Server(settings.APP_NAME)


@server.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available IACR research tools."""
    return [search_tool, get_paper_details_tool, download_paper_tool]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls for IACR research functionality."""
    logger.debug(f"Calling tool {name} with arguments {arguments}")
    try:
        if name == "search_papers":
            return await handle_search(arguments)
        elif name == "get_paper_details":
            return await handle_get_paper_details(arguments)
        elif name == "download_paper":
            return await handle_download_paper(arguments)
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool {name}")]
    except Exception as e:
        logger.error(f"Tool error: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the server async context."""
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name=settings.APP_NAME,
                server_version=settings.APP_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(resources_changed=False),
                    experimental_capabilities={},
                ),
            ),
        )