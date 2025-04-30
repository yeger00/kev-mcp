import uvicorn
from cisa_vuln_checker.server import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug"
    )