from cisa_vuln_checker.server import create_fast_mcp


if __name__ == "__main__":
    mcp = create_fast_mcp()
    mcp.run(transport="sse")