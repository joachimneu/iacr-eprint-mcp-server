"""Data models for the IACR MCP server."""

from typing import Literal

from pydantic import BaseModel, Field

DownloadFormat = Literal["pdf", "txt"]


class SearchPapersRequest(BaseModel):
    """Request model for searching papers."""

    query: str = Field(description="Search query string")
    year: int | None = Field(None, description="Filter by publication year")
    category: str | None = Field(None, description="Filter by category")
    max_results: int = Field(20, description="Maximum number of results")


class GetPaperDetailsRequest(BaseModel):
    """Request model for getting paper details."""

    paper_id: str = Field(description="Unique paper identifier")


class DownloadPaperRequest(BaseModel):
    """Request model for downloading a paper."""

    paper_id: str = Field(description="Unique paper identifier")
    format: DownloadFormat = Field(
        "pdf",
        description="Download format (pdf or txt)",
    )


class IACRPaper(BaseModel):
    """Model for an IACR paper."""

    id: str
    title: str
    authors: str
    link: str
    description: str
    pub_date: str


class PaperSearchResult(BaseModel):
    """Model for paper search results."""

    id: str
    title: str
    authors: str
    year: int
    link: str
    abstract: str


class PaperDetails(BaseModel):
    """Model for detailed paper information."""

    id: str
    title: str
    authors: str
    abstract: str
    link: str
    date: str
