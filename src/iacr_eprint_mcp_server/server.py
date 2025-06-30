"""
IACR MCP Server
==============

This module implements an MCP server for interacting with the
IACR Cryptology ePrint Archive.
"""

import logging

from mcp.server.fastmcp import FastMCP

from .config import Settings
from .tools import download_paper, get_paper_details, search_papers

settings = Settings()
logger = logging.getLogger("iacr-eprint-mcp-server")
logger.setLevel(logging.INFO)

# Create FastMCP server instance
mcp = FastMCP(settings.APP_NAME)

# Register tools using FastMCP's add_tool method
mcp.add_tool(
    search_papers,
    name="search_papers",
    description="Search for papers in the IACR Cryptology ePrint Archive",
)

mcp.add_tool(
    get_paper_details,
    name="get_paper_details",
    description="Retrieve details of a specific paper by its ID",
)

mcp.add_tool(
    download_paper,
    name="download_paper",
    description="Download a paper in PDF or TXT format",
)


async def main():
    """Run the server using FastMCP."""
    await mcp.run()
