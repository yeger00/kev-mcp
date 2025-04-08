import typer
from datetime import datetime, timedelta
from typing import Optional
import duckdb
from pathlib import Path

app = typer.Typer()

def get_recent_cves(days: Optional[int] = None, hours: Optional[int] = None) -> list[str]:
    """
    Get all CVEs added in the last X days or hours.
    
    Args:
        days: Number of days to look back
        hours: Number of hours to look back
        
    Returns:
        List of CVE IDs
    """
    if days is None and hours is None:
        raise ValueError("Either days or hours must be specified")
    
    # Calculate the cutoff date
    now = datetime.now()
    if days is not None:
        cutoff_date = now - timedelta(days=days)
    else:
        cutoff_date = now - timedelta(hours=hours)
    
    # Query the JSON file directly from URL using DuckDB
    conn = duckdb.connect()
    # Enable HTTPFS extension
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")
    
    query = f"""
    SELECT cveID
    FROM read_json_auto('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    WHERE dateAdded >= '{cutoff_date.strftime("%Y-%m-%d")}'
    """
    
    result = conn.execute(query).fetchall()
    conn.close()
    
    return [row[0] for row in result]

def check_cve_exists(cve_id: str) -> bool:
    """
    Check if a given CVE exists in the list.
    
    Args:
        cve_id: The CVE ID to check (e.g., "CVE-2023-1234")
        
    Returns:
        True if the CVE exists, False otherwise
    """
    conn = duckdb.connect()
    # Enable HTTPFS extension
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")
    
    query = f"""
    SELECT COUNT(*) as count
    FROM read_json_auto('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    WHERE cveID = '{cve_id}'
    """
    
    result = conn.execute(query).fetchone()
    conn.close()
    
    return result[0] > 0

@app.command()
def recent_cves(
    days: Optional[int] = typer.Option(None, help="Number of days to look back"),
    hours: Optional[int] = typer.Option(None, help="Number of hours to look back")
):
    """Get all CVEs added in the last X days or hours."""
    cves = get_recent_cves(days, hours)
    for cve in cves:
        print(cve)

@app.command()
def check_cve(cve_id: str = typer.Argument(..., help="The CVE ID to check (e.g., CVE-2023-1234)")):
    """Check if a given CVE exists in the list."""
    exists = check_cve_exists(cve_id)
    if exists:
        print(f"CVE {cve_id} exists in the list")
    else:
        print(f"CVE {cve_id} does not exist in the list")

if __name__ == "__main__":
    app() 