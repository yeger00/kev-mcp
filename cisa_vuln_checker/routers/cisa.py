from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..cisa_vuln_checker import check_cve_exists as check_cve, get_recent_cves as get_cves


router = APIRouter()


class CVEResponse(BaseModel):
    exists: bool
    details: Optional[Dict[str, Any]] = None

class RecentCVEsResponse(BaseModel):
    total: int
    days_range: int
    cves: List[Dict[str, Any]]


@router.get("/check-cve", response_model=CVEResponse)
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

@router.get("/recent-cves", response_model=RecentCVEsResponse)
async def get_recent_cves(days: int = Query(7, ge=1, le=30, description="Number of days to look back (1-30)")):
    cves = get_cves(days=days)
    
    return {
        "total": len(cves),
        "days_range": days,
        "cves": cves
    }