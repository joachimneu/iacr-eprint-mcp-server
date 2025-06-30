"""Paper download functionality for the IACR MCP server."""

import base64
import logging

import httpx

from ..config import Settings
from ..models import DownloadPaperRequest

settings = Settings()
logger = logging.getLogger(__name__)


async def download_paper(request: DownloadPaperRequest) -> str:
    """Download a paper in PDF or TXT format."""
    try:
        # Construct download URL
        download_url = f"https://eprint.iacr.org/{request.paper_id}.{request.format}"

        # Download the paper
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(download_url)
            response.raise_for_status()

        # Encode as base64
        encoded_data = base64.b64encode(response.content).decode("utf-8")

        # Return as file content
        return (
            f"File: {request.paper_id}.{request.format}\n"
            f"Size: {len(response.content)} bytes\n"
            f"Data: {encoded_data}"
        )

    except Exception as e:
        logger.error(f"Paper download error: {str(e)}")
        return f"Error: {str(e)}"
