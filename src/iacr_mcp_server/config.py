"""Configuration for the IACR MCP server."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = Field(default="iacr-mcp-server", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    IACR_RSS_URL: str = Field(
        default="https://eprint.iacr.org/rss/rss.xml?order=recent",
        description="IACR RSS feed URL",
    )
    MAX_RESULTS: int = Field(
        default=100,
        description="Maximum number of search results",
    )
    REQUEST_TIMEOUT: int = Field(
        default=15,
        description="HTTP request timeout in seconds",
    )

    class Config:
        """Pydantic config."""

        env_file = ".env"
