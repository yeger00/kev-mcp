from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict
from pydantic import BaseModel

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pydantic import Field

from .cisa_vuln_checker import check_cve_exists as check_cve, get_recent_cves as get_cves


class CVEResponse(BaseModel):
    exists: bool
    details: Optional[Dict[str, Any]] = None

class RecentCVEsResponse(BaseModel):
    total: int
    days_range: int
    cves: List[Dict[str, Any]]


# This is a bit of weird place to choose the port
# Create server with database lifecycle management
mcp = FastMCP(
    "CISA KEV MCP",
    port=8080
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
async def get_recent_cves(days: int = Field(7, ge=1, le=30, description="Number of days to look back (1-30)")):
    cves = get_cves(days=days)
    
    return {
        "total": len(cves),
        "days_range": days,
        "cves": cves
    }