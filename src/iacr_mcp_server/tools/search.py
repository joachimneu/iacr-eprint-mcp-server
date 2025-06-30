"""Search functionality for the IACR MCP server."""

import httpx
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import xmltodict

import mcp.types as types
from ..config import Settings
from ..models import SearchPapersRequest, IACRPaper, PaperSearchResult

settings = Settings()
logger = logging.getLogger(__name__)

search_tool = types.Tool(
    name="search_papers",
    description="Search for papers in the IACR Cryptology ePrint Archive",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "year": {"type": "number"},
            "category": {"type": "string"},
            "max_results": {"type": "number", "default": 20}
        },
        "required": ["query"],
    },
)


async def handle_search(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle paper search requests."""
    try:
        # Validate input using Pydantic
        validated_args = SearchPapersRequest(**arguments)
        
        # Fetch RSS feed with comprehensive headers
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(
                settings.IACR_RSS_URL,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/xml,text/xml,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
            )
            response.raise_for_status()
            
        # Parse XML feed
        parsed_feed = xmltodict.parse(response.text)
        
        # Ensure items exist
        if not parsed_feed.get('rss', {}).get('channel', {}).get('item'):
            logger.warning('No items found in RSS feed')
            return [types.TextContent(type="text", text="[]")]
            
        # Current year for filtering
        current_year = datetime.now().year
        
        # Extract and filter papers
        items = parsed_feed['rss']['channel']['item']
        if not isinstance(items, list):
            items = [items]  # Handle single item case
            
        papers = []
        for item in items:
            # Create paper object
            paper = IACRPaper(
                id=item['link'].split('/')[-1],
                title=item['title'],
                authors=item.get('dc:creator', 'Unknown'),
                link=item['link'],
                description=item['description'],
                pub_date=item['pubDate']
            )
            
            # Apply filters
            title_lower = paper.title.lower()
            description_lower = paper.description.lower()
            query_lower = validated_args.query.lower()
            
            # Query matching
            if not (query_lower in title_lower or query_lower in description_lower):
                continue
                
            # Year filtering
            paper_year = datetime.strptime(paper.pub_date, '%a, %d %b %Y %H:%M:%S %z').year
            if validated_args.year and paper_year != validated_args.year:
                continue
            elif not validated_args.year and paper_year < current_year - 10:
                continue
                
            # Create result object
            result = PaperSearchResult(
                id=paper.id,
                title=paper.title,
                authors=paper.authors,
                year=paper_year,
                link=paper.link,
                abstract=paper.description
            )
            papers.append(result.model_dump())
            
            if len(papers) >= validated_args.max_results:
                break
                
        # Log results for debugging
        logger.info(f'Search Results: Found {len(papers)} papers for query "{validated_args.query}"')
        
        return [types.TextContent(type="text", text=json.dumps(papers, indent=2))]
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]