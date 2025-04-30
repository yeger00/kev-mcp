from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi_mcp import FastApiMCP
from typing import Optional, List, Dict
from pydantic import BaseModel
import os
from .cisa_vuln_checker import get_recent_cves, check_cve_exists
from .routers.cisa import router as cisa_router


class HealthResponse(BaseModel):
    status: str
    version: str

class StatusResponse(BaseModel):
    server_status: str
    endpoints: Dict[str, str]


app = FastAPI(
    title="MCP REST API",
    description="REST API endpoints for the Model Control Protocol and CISA Known Exploited Vulnerabilities",
    version="1.0.0",
)


app.include_router(cisa_router)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    return {
        "server_status": "running",
        "endpoints": {
            "sse": "/sse",
            "rest": "/rest/*",
            "docs": "/rest/docs"
        }
    }


# Create and mount the FastAPI MCP server
mcp = FastApiMCP(
    app,
    name="CISA Vulnerability Checker",
    description="A server for checking CISA Known Exploited Vulnerabilities",
    base_url="/cisa-kev/"
)
mcp.mount()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
