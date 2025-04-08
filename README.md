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

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Get Recent CVEs

Get CVEs from the last 7 days:
```bash
python cli.py recent-cves --days 7
```

Get CVEs from the last 24 hours:
```bash
python cli.py recent-cves --hours 24
```

### Check if a CVE Exists

```bash
python cli.py check-cve CVE-2023-1234
```

## Running Tests

The project includes integration tests that test the CLI commands. To run the tests:

1. Make sure you have pytest installed:
```bash
pip install pytest
```

2. Run the tests:
```bash
pytest tests/
```

The tests will:
- Test getting recent CVEs by days and hours
- Test error handling when no arguments are provided
- Test checking for existing and non-existing CVEs

## Project Structure

- `cisa_vuln_checker.py`: Core logic for querying the CISA database
- `cli.py`: Command-line interface using Typer
- `tests/test_cli.py`: Integration tests for the CLI commands

## Dependencies

- Python 3.7+
- duckdb
- typer
- pytest (for running tests) 