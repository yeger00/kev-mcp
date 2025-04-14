from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from typing import Optional, List, Dict
from pydantic import BaseModel

from .cisa_vuln_checker import get_recent_cves, check_cve_exists
from .rest_api import app

# Create and mount the FastAPI MCP server
mcp = FastApiMCP(
    app,
    name="CISA Vulnerability Checker",
    description="A server for checking CISA Known Exploited Vulnerabilities",
)
mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)