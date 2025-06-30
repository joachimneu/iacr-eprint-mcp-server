"""Paper details functionality for the IACR MCP server."""

import json
import logging

import httpx
import xmltodict

from ..config import Settings
from ..models import GetPaperDetailsRequest, PaperDetails

settings = Settings()
logger = logging.getLogger(__name__)


async def get_paper_details(request: GetPaperDetailsRequest) -> str:
    """Retrieve details of a specific paper by its ID."""
    try:
        # Fetch RSS feed
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(settings.IACR_RSS_URL)
            response.raise_for_status()

        # Parse XML feed
        parsed_feed = xmltodict.parse(response.text)

        # Find the specific paper
        items = parsed_feed.get("rss", {}).get("channel", {}).get("item", [])
        if not isinstance(items, list):
            items = [items]  # Handle single item case

        paper_item = None
        for item in items:
            if item["link"].split("/")[-1] == request.paper_id:
                paper_item = item
                break

        if not paper_item:
            return f"Error: Paper {request.paper_id} not found"

        # Create paper details
        paper_details = PaperDetails(
            id=request.paper_id,
            title=paper_item["title"],
            authors=paper_item.get("dc:creator", "Unknown"),
            abstract=paper_item["description"],
            link=paper_item["link"],
            date=paper_item["pubDate"],
        )

        return json.dumps(paper_details.model_dump(), indent=2)

    except Exception as e:
        logger.error(f"Paper details error: {str(e)}")
        return f"Error: {str(e)}"
