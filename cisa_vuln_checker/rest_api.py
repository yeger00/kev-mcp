from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from .cisa_vuln_checker import check_cve_exists as check_cve, get_recent_cves as get_cves

class HealthResponse(BaseModel):
    status: str
    version: str

class StatusResponse(BaseModel):
    server_status: str
    endpoints: Dict[str, str]

class CVEResponse(BaseModel):
    exists: bool
    details: Optional[Dict[str, Any]] = None

class RecentCVEsResponse(BaseModel):
    total: int
    days_range: int
    cves: List[Dict[str, Any]]

app = FastAPI(
    title="MCP REST API",
    description="REST API endpoints for the Model Control Protocol and CISA Known Exploited Vulnerabilities",
    version="1.0.0"
)

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

@app.get("/check-cve", response_model=CVEResponse)
async def check_cve_exists(cve_id: str = Query(..., description="The CVE ID to check (e.g., CVE-2024-1234)")):
    if not cve_id:
        raise HTTPException(status_code=400, detail="Missing required parameter: cve_id")
    
    result = check_cve(cve_id)
    if result is None:
        return {"exists": False}
    
    return {
        "exists": True,
        "details": result
    }

@app.get("/recent-cves", response_model=RecentCVEsResponse)
async def get_recent_cves(days: int = Query(7, ge=1, le=30, description="Number of days to look back (1-30)")):
    cves = get_cves(days=days)
    
    return {
        "total": len(cves),
        "days_range": days,
        "cves": cves
    }

def create_rest_app():
    return app 