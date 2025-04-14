from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi_mcp import FastApiMCP
from typing import Optional, List, Dict
from pydantic import BaseModel
import os
from .cisa_vuln_checker import get_recent_cves, check_cve_exists
from .rest_api import app

# Create and mount the FastAPI MCP server
mcp = FastApiMCP(
    app,
    name="CISA Vulnerability Checker",
    description="A server for checking CISA Known Exploited Vulnerabilities",
)
mcp.mount()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)