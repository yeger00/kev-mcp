from cisa_vuln_checker.server import mcp


if __name__ == "__main__":
    mcp.run(transport="sse")