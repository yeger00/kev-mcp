from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os

from .mcp_server import mcp

async def homepage(request):
    return FileResponse('cisa_vuln_checker/static/index.html')

app = Starlette(
    routes=[
        Route('/', endpoint=homepage),
        Mount('/sse', app=mcp.sse_app()),
        Mount('/static', app=StaticFiles(directory='cisa_vuln_checker/static'), name='static')
    ]
)

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("MCP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)