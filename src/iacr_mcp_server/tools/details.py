"""Paper details functionality for the IACR MCP server."""

import httpx
import json
import logging
from typing import Dict, Any, List
import xmltodict

import mcp.types as types
from ..config import Settings
from ..models import GetPaperDetailsRequest, IACRPaper, PaperDetails

settings = Settings()
logger = logging.getLogger(__name__)

get_paper_details_tool = types.Tool(
    name="get_paper_details",
    description="Retrieve details of a specific paper by its ID",
    inputSchema={
        "type": "object",
        "properties": {
            "paper_id": {"type": "string"}
        },
        "required": ["paper_id"],
    },
)


async def handle_get_paper_details(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle paper details requests."""
    try:
        # Validate input using Pydantic
        validated_args = GetPaperDetailsRequest(**arguments)
        
        # Fetch RSS feed
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(settings.IACR_RSS_URL)
            response.raise_for_status()
            
        # Parse XML feed
        parsed_feed = xmltodict.parse(response.text)
        
        # Find the specific paper
        items = parsed_feed.get('rss', {}).get('channel', {}).get('item', [])
        if not isinstance(items, list):
            items = [items]  # Handle single item case
            
        paper_item = None
        for item in items:
            if item['link'].split('/')[-1] == validated_args.paper_id:
                paper_item = item
                break
                
        if not paper_item:
            return [types.TextContent(type="text", text=f"Error: Paper {validated_args.paper_id} not found")]
            
        # Create paper details
        paper_details = PaperDetails(
            id=validated_args.paper_id,
            title=paper_item['title'],
            authors=paper_item.get('dc:creator', 'Unknown'),
            abstract=paper_item['description'],
            link=paper_item['link'],
            date=paper_item['pubDate']
        )
        
        return [types.TextContent(type="text", text=json.dumps(paper_details.model_dump(), indent=2))]
        
    except Exception as e:
        logger.error(f"Paper details error: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]