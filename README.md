# CISA Vulnerability Checker MCP Server

A Model Control Protocol (MCP) server that provides access to CISA's Known Exploited Vulnerabilities (KEV) catalog through Claude and Cursor integration.

## MCP Server Functionality

The MCP server provides real-time access to CISA's KEV catalog through Claude and Cursor integration. It enables:
- Real-time CVE checking and monitoring
- Integration with Claude for enhanced security analysis
- Access to the complete CISA KEV catalog

### Production Deployment

The MCP server is available at: `https://amcipi.com/cisa-kev/`

To configure Claude to use the CISA vulnerability checker server, add the following to your Claude configuration file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cisa": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://amcipi.com/cisa-kev/mcp"
      ]
    }
  }
}
```

## Installation Options

### Option 1: Install from Repository

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Option 2: Run Directly from Repository

To run the MCP server directly:

```bash
uvicorn cisa_vuln_checker.server:app
```

This will start the server on the default port (8000).

### Option 3: Run with Docker

Build the image:
```bash
docker build -t cisa-vuln-checker .
```

Run the container:
```bash
docker run -p 8080:8080 cisa-vuln-checker
```

## API Functionality

### REST API Endpoints

- Health Check: `GET /rest/health`
- Server Status: `GET /rest/status`
- Check CVE: `GET /rest/check-cve?cve_id=CVE-2024-1234`
- Recent CVEs: `GET /rest/recent-cves?days=7`
- API Documentation: `GET /rest/docs`

### CLI Commands

Get CVEs from the last 7 days:
```bash
cisa-vuln-checker recent-cves --days 7
```

Get CVEs from the last 24 hours:
```bash
cisa-vuln-checker recent-cves --hours 24
```

Check if a CVE exists:
```bash
cisa-vuln-checker check-cve CVE-2023-1234
```

## Development

### Running Tests

The project includes integration tests that test the CLI commands. To run the tests:

1. Make sure you have the package installed in development mode
2. Run the tests:
```bash
pytest tests/
```

The tests will:
- Test getting recent CVEs by days and hours
- Test error handling when no arguments are provided
- Test checking for existing and non-existing CVEs