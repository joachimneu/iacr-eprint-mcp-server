[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/doomdagadiggiedahdah-iacr-mcp-server-badge.png)](https://mseep.ai/app/doomdagadiggiedahdah-iacr-mcp-server)

# IACR Cryptology ePrint Archive MCP Server

[![smithery badge](https://smithery.ai/badge/iacr-mcp-server)](https://smithery.ai/server/iacr-mcp-server)

## Overview

This Model Context Protocol (MCP) server provides a programmatic interface to the IACR Cryptology ePrint Archive, enabling efficient retrieval of cryptographic research papers. **Now rewritten in modern, idiomatic Python!**

<a href="https://glama.ai/mcp/servers/e2oh3a96de"><img width="380" height="200" src="https://glama.ai/mcp/servers/e2oh3a96de/badge" alt="IACR Server MCP server" /></a>

## Features

- 🔍 Search cryptographic papers
- 📋 Retrieve paper metadata  
- 💾 Download papers in PDF or TXT format
- 🐍 Modern Python implementation with async/await
- 🔒 Type-safe with Pydantic models
- ⚡ Fast HTTP requests with httpx

## Prerequisites

- Python 3.11+
- pip or uv (recommended)

## Installation

### Installing via Smithery

To install IACR Cryptology ePrint Archive for Claude Desktop automatically via [Smithery](https://smithery.ai/server/iacr-mcp-server):

```bash
npx -y @smithery/cli install iacr-mcp-server --client claude
```

### Manual Installation

```bash
git clone https://github.com/joachimneu/iacr-eprint-mcp-server.git
cd iacr-eprint-mcp-server
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/joachimneu/iacr-eprint-mcp-server.git
cd iacr-eprint-mcp-server
pip install -e ".[dev]"
```

## Configuration

No additional configuration is required. The server uses the IACR ePrint Archive's RSS feed for data retrieval.

## Usage

### Running the Server

```bash
# Via module
python -m iacr_mcp_server

# Via installed script
iacr-eprint-mcp-server
```

### Available Tools

1. `search_papers`: Search for papers
   - Parameters:
     - `query`: Search term (required)
     - `year`: Publication year (optional)
     - `category`: Paper category (optional)
     - `max_results`: Maximum number of results (default: 20)

2. `get_paper_details`: Retrieve details for a specific paper
   - Parameters:
     - `paper_id`: Unique paper identifier (required)

3. `download_paper`: Download a paper in PDF or TXT format
   - Parameters:
     - `paper_id`: Unique paper identifier (required)
     - `format`: File format - 'pdf' or 'txt' (default: 'pdf')

## Development

### Code Quality

This project uses modern Python development practices:

- **Ruff** for code formatting and linting
- **Pydantic** for data validation and settings
- **Type hints** throughout the codebase
- **Async/await** for efficient I/O operations
- **httpx** for modern HTTP client functionality

### Running Tests

```bash
python -m unittest tests/ -v
```

### Code Formatting

```bash
ruff format src/ tests/
```

## Architecture

The server is structured as a modern Python package:

```
src/iacr_mcp_server/
├── __init__.py          # Package initialization and main entry point
├── server.py            # MCP server implementation
├── config.py            # Configuration management with Pydantic
├── models.py            # Data models and validation schemas
└── tools/              # Tool implementations
    ├── __init__.py
    ├── search.py       # Paper search functionality
    ├── details.py      # Paper details retrieval
    └── download.py     # Paper download functionality
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch  
5. Create a Pull Request

## Disclaimer

This is an unofficial tool. Always refer to the original IACR Cryptology ePrint Archive for the most accurate and up-to-date research publications.

## Contact

For issues, questions, or suggestions, please open a GitHub issue.
