from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict
from pydantic import BaseModel

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pydantic import Field
import uvicorn

from .cisa_vuln_checker import check_cve_exists as check_cve, get_recent_cves as get_cves


class CVEResponse(BaseModel):
    exists: bool
    details: Optional[Dict[str, Any]] = None

class RecentCVEsResponse(BaseModel):
    total: int
    days_range: int
    cves: List[Dict[str, Any]]


async def homepage(request):
    return FileResponse('cisa_vuln_checker/static/index.html')

class CisaKevMCP(FastMCP):
    async def run_sse_async(self) -> None:
        """Run the server using SSE transport."""
        starlette_app = self.sse_app()

        # TODO: there is no place to put other mounts to the starlette_app,
        # so we need to mount the static files manually
        starlette_app.add_route("/cisa-kev", route=homepage)
        starlette_app.mount("/static", app=StaticFiles(directory="cisa_vuln_checker/static"), name="static")
        config = uvicorn.Config(
            starlette_app,
            host=self.settings.host,
            port=self.settings.port,
            log_level=self.settings.log_level.lower(),
        )
        server = uvicorn.Server(config)
        await server.serve()

def create_fast_mcp():
    mcp = CisaKevMCP(
        "CISA KEV MCP",
        port=8080,
        sse_path="/cisa-kev/sse",
        message_path="/cisa-kev/messages/",
    )


    @mcp.tool("check-cve", description="Check if a given CVE exists in the list.")
    async def check_cve_exists(
        cve_id: str = Field(description="The CVE ID to check (e.g., CVE-2024-1234)"),
    ) -> CVEResponse:
        result = check_cve(cve_id)
        if result is None:
            return {"exists": False}
        
        return {
            "exists": True,
            "details": result
        }
        

    @mcp.tool("recent-cves", description="Get all CVEs added in the last X days.")
    async def get_recent_cves(
        days: int = Field(7, ge=1, le=30, description="Number of days to look back (1-30)"),
    ) -> RecentCVEsResponse:
        cves = get_cves(days=days)
        
        return {
            "total": len(cves),
            "days_range": days,
            "cves": cves
        }

    return mcp
