"""Paper download functionality for the IACR MCP server."""

import httpx
import base64
import logging
from typing import Dict, Any, List

import mcp.types as types
from ..config import Settings
from ..models import DownloadPaperRequest

settings = Settings()
logger = logging.getLogger(__name__)

download_paper_tool = types.Tool(
    name="download_paper",
    description="Download a paper in PDF or TXT format",
    inputSchema={
        "type": "object",
        "properties": {
            "paper_id": {"type": "string"},
            "format": {
                "type": "string",
                "enum": ["pdf", "txt"],
                "default": "pdf"
            }
        },
        "required": ["paper_id"],
    },
)


async def handle_download_paper(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle paper download requests."""
    try:
        # Validate input using Pydantic
        validated_args = DownloadPaperRequest(**arguments)
        
        # Construct download URL
        download_url = f"https://eprint.iacr.org/{validated_args.paper_id}.{validated_args.format}"
        
        # Download the paper
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(download_url)
            response.raise_for_status()
            
        # Encode as base64
        encoded_data = base64.b64encode(response.content).decode('utf-8')
        
        # Return as file content
        return [
            types.TextContent(
                type="text",
                text=f"File: {validated_args.paper_id}.{validated_args.format}\nSize: {len(response.content)} bytes\nData: {encoded_data}"
            )
        ]
        
    except Exception as e:
        logger.error(f"Paper download error: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]