# CISA Vulnerability Checker

A Python tool that uses DuckDB to query CISA's Known Exploited Vulnerabilities catalog.

## Features

- Get all CVEs added in the last X days or hours
- Check if a specific CVE exists in the list
- Uses DuckDB's HTTPFS extension to read the JSON file directly from CISA's website

## Installation

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

## Docker
Build the image:
```
docker build -t cisa-vuln-checker .
```

Run the container:
```
docker run -p 8080:8080 cisa-vuln-checker
```

## Usage

### Get Recent CVEs

Get CVEs from the last 7 days:
```bash
cisa-vuln-checker recent-cves --days 7
```

Get CVEs from the last 24 hours:
```bash
cisa-vuln-checker recent-cves --hours 24
```

### Check if a CVE Exists

```bash
cisa-vuln-checker check-cve CVE-2023-1234
```

### Running the Server

To run the Model Context Protocol server:

```bash
uvicorn cisa_vuln_checker.server:app
```

This will start the server on the default port (8000). You can then interact with the CISA vulnerability checking tools through the MCP interface (`/sse`) or RESR (`/rest`).

### Configuring the Server
#### Claude
To configure Claude to use the CISA vulnerability checker server, add the following to your Claude configuration file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json`):

```
{
  "mcpServers": {
    "cisa": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/sse"
      ]
    }
  }
} 
```

## Development

### Running Tests

The project includes integration tests that test the CLI commands. To run the tests:

1. Make sure you have the package installed in development mode (see Installation step 4)
2. Run the tests:
```bash
pytest tests/
```

The tests will:
- Test getting recent CVEs by days and hours
- Test error handling when no arguments are provided
- Test checking for existing and non-existing CVEs