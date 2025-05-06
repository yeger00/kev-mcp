import typer
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import duckdb

app = typer.Typer()

def get_recent_cves(days: Optional[int] = None, hours: Optional[int] = None) -> List[Dict]:
    """
    Get all CVEs added in the last X days or hours.
    
    Args:
        days: Number of days to look back
        hours: Number of hours to look back
        
    Returns:
        List of dictionaries containing vulnerability details
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
    WITH vulnerabilities AS (
        SELECT unnest(data.vulnerabilities) as vuln
        FROM read_json_auto('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json') as data
    )
    SELECT 
        vuln.cveID,
        vuln.vendorProject,
        vuln.product,
        vuln.vulnerabilityName,
        vuln.dateAdded,
        vuln.shortDescription,
        vuln.requiredAction,
        vuln.dueDate,
        vuln.knownRansomwareCampaignUse,
        vuln.notes,
        vuln.cwes
    FROM vulnerabilities
    WHERE vuln.dateAdded >= '{cutoff_date.strftime("%Y-%m-%d")}'
    """
    
    result = conn.execute(query).fetchall()
    conn.close()
    
    # Convert the result to a list of dictionaries
    vulnerabilities = []
    for row in result:
        vulnerability = {
            "cveID": row[0],
            "vendorProject": row[1],
            "product": row[2],
            "vulnerabilityName": row[3],
            "dateAdded": row[4],
            "shortDescription": row[5],
            "requiredAction": row[6],
            "dueDate": row[7],
            "knownRansomwareCampaignUse": row[8],
            "notes": row[9],
            "cwes": row[10]
        }
        vulnerabilities.append(vulnerability)
    
    return vulnerabilities

def check_cve_exists(cve_id: str) -> Optional[Dict]:
    """
    Check if a given CVE exists in the list and return its details.
    
    Args:
        cve_id: The CVE ID to check (e.g., "CVE-2023-1234")
        
    Returns:
        Dictionary containing vulnerability details if found, None otherwise
    """
    conn = duckdb.connect()
    # Enable HTTPFS extension
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")
    
    query = f"""
    WITH vulnerabilities AS (
        SELECT unnest(data.vulnerabilities) as vuln
        FROM read_json_auto('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json') as data
    )
    SELECT 
        vuln.cveID,
        vuln.vendorProject,
        vuln.product,
        vuln.vulnerabilityName,
        vuln.dateAdded,
        vuln.shortDescription,
        vuln.requiredAction,
        vuln.dueDate,
        vuln.knownRansomwareCampaignUse,
        vuln.notes,
        vuln.cwes
    FROM vulnerabilities
    WHERE vuln.cveID = '{cve_id}'
    """
    
    result = conn.execute(query).fetchone()
    conn.close()
    
    if result:
        return {
            "cveID": result[0],
            "vendorProject": result[1],
            "product": result[2],
            "vulnerabilityName": result[3],
            "dateAdded": result[4],
            "shortDescription": result[5],
            "requiredAction": result[6],
            "dueDate": result[7],
            "knownRansomwareCampaignUse": result[8],
            "notes": result[9],
            "cwes": result[10]
        }
    return None