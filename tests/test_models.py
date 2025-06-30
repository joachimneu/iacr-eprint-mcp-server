"""Tests for the IACR MCP server."""

import unittest
from iacr_mcp_server.models import SearchPapersRequest, GetPaperDetailsRequest, DownloadPaperRequest


class TestModels(unittest.TestCase):
    """Test the data models."""

    def test_search_papers_request(self):
        """Test SearchPapersRequest model."""
        request = SearchPapersRequest(query="cryptography")
        self.assertEqual(request.query, "cryptography")
        self.assertEqual(request.max_results, 20)
        
        request_with_options = SearchPapersRequest(
            query="blockchain", 
            year=2023, 
            max_results=10
        )
        self.assertEqual(request_with_options.year, 2023)
        self.assertEqual(request_with_options.max_results, 10)

    def test_get_paper_details_request(self):
        """Test GetPaperDetailsRequest model."""
        request = GetPaperDetailsRequest(paper_id="2023/123")
        self.assertEqual(request.paper_id, "2023/123")

    def test_download_paper_request(self):
        """Test DownloadPaperRequest model."""
        request = DownloadPaperRequest(paper_id="2023/123")
        self.assertEqual(request.paper_id, "2023/123")
        self.assertEqual(request.format, "pdf")
        
        request_txt = DownloadPaperRequest(paper_id="2023/123", format="txt")
        self.assertEqual(request_txt.format, "txt")


if __name__ == "__main__":
    unittest.main()