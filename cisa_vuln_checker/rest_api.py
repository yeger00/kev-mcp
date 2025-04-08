from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import json
from datetime import datetime, timedelta, date
from .cisa_vuln_checker import check_cve_exists as check_cve, get_recent_cves as get_cves

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

def create_json_response(data):
    return JSONResponse(
        content=json.loads(json.dumps(data, cls=CustomJSONEncoder))
    )

async def health_check(request):
    return create_json_response({
        "status": "healthy",
        "version": "1.0.0"
    })

async def get_status(request):
    return create_json_response({
        "server_status": "running",
        "endpoints": {
            "sse": "/sse",
            "rest": "/rest/*",
            "docs": "/rest/docs"
        }
    })

async def check_cve_exists(request):
    cve_id = request.query_params.get('cve_id')
    if not cve_id:
        return create_json_response({
            "error": "Missing required parameter: cve_id"
        }, status_code=400)
    
    result = check_cve(cve_id)
    if result is None:
        return create_json_response({"exists": False})
    
    return create_json_response({
        "exists": True,
        "details": result
    })

async def get_recent_cves(request):
    days = request.query_params.get('days', '7')
    
    try:
        days = int(days)
        if days < 1 or days > 30:
            return create_json_response({
                "error": "Days parameter must be between 1 and 30"
            }, status_code=400)
    except ValueError:
        return create_json_response({
            "error": "Invalid days parameter"
        }, status_code=400)
    
    cves = get_cves(days=days)
    
    return create_json_response({
        "total": len(cves),
        "days_range": days,
        "cves": cves
    })

async def docs(request):
    api_docs = {
        "openapi": "3.0.0",
        "info": {
            "title": "MCP REST API",
            "version": "1.0.0",
            "description": "REST API endpoints for the Model Control Protocol and CISA Known Exploited Vulnerabilities"
        },
        "paths": {
            "/rest/health": {
                "get": {
                    "summary": "Health check endpoint",
                    "responses": {
                        "200": {
                            "description": "Server health status"
                        }
                    }
                }
            },
            "/rest/status": {
                "get": {
                    "summary": "Server status and available endpoints",
                    "responses": {
                        "200": {
                            "description": "Current server status and endpoint listing"
                        }
                    }
                }
            },
            "/rest/check-cve": {
                "get": {
                    "summary": "Check if a specific CVE exists in CISA KEV catalog",
                    "parameters": [
                        {
                            "name": "cve_id",
                            "in": "query",
                            "required": true,
                            "schema": {
                                "type": "string"
                            },
                            "description": "The CVE ID to check (e.g., CVE-2024-1234)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "CVE existence check result with full details if found"
                        },
                        "400": {
                            "description": "Invalid or missing CVE ID"
                        }
                    }
                }
            },
            "/rest/recent-cves": {
                "get": {
                    "summary": "Get recent CVEs from CISA KEV catalog",
                    "parameters": [
                        {
                            "name": "days",
                            "in": "query",
                            "required": false,
                            "schema": {
                                "type": "integer",
                                "default": 7,
                                "minimum": 1,
                                "maximum": 30
                            },
                            "description": "Number of days to look back (1-30)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of recent CVEs from CISA KEV catalog"
                        },
                        "400": {
                            "description": "Invalid parameters"
                        }
                    }
                }
            }
        }
    }
    return create_json_response(api_docs)

def create_rest_app():
    return Starlette(routes=[
        Route('/health', health_check),
        Route('/status', get_status),
        Route('/docs', docs),
        Route('/check-cve', check_cve_exists),
        Route('/recent-cves', get_recent_cves),
    ]) 