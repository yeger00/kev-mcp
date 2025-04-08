from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict

from .cisa_vuln_checker import get_recent_cves, check_cve_exists

# Create an MCP server
mcp = FastMCP("CISA Vulnerability Checker")

@mcp.tool()
def get_vulnerabilities(days: Optional[int] = None, hours: Optional[int] = None) -> List[Dict]:
    """
    Get all CVEs added in the last X days or hours.
    
    Args:
        days: Number of days to look back
        hours: Number of hours to look back
        
    Returns:
        List of dictionaries containing vulnerability details
    """
    return get_recent_cves(days=days, hours=hours)

@mcp.tool()
def check_vulnerability(cve_id: str) -> Optional[Dict]:
    """
    Check if a given CVE exists in the list and return its details.
    
    Args:
        cve_id: The CVE ID to check (e.g., "CVE-2023-1234")
        
    Returns:
        Dictionary containing vulnerability details if found, None otherwise
    """
    return check_cve_exists(cve_id=cve_id)

@mcp.prompt()
def generate_remediation_plan(cve_id: str) -> str:
    """
    Generate a remediation plan for a specific vulnerability.
    
    Args:
        cve_id: The CVE ID to generate a plan for
        
    Returns:
        A string containing the remediation plan
    """
    vuln = check_cve_exists(cve_id)
    if not vuln:
        return f"No remediation plan available - CVE {cve_id} not found in CISA KEV catalog."
    
    return f"""Remediation Plan for {cve_id}

Vulnerability: {vuln['vulnerabilityName']}
Affected Product: {vuln['product']} by {vuln['vendorProject']}

Required Action:
{vuln['requiredAction']}

Due Date: {vuln['dueDate']}

Additional Information:
- Description: {vuln['shortDescription']}
{f"- Known Ransomware Use: {vuln['knownRansomwareCampaignUse']}" if vuln['knownRansomwareCampaignUse'] else ""}
{f"- Notes: {vuln['notes']}" if vuln['notes'] else ""}
{f"- Associated CWEs: {', '.join(vuln['cwes'])}" if vuln['cwes'] else ""}

Please ensure to:
1. Identify all instances of the affected product in your environment
2. Test the remediation in a staging environment first
3. Apply the fix before the due date
4. Verify the fix has been successfully applied
5. Document all actions taken
"""