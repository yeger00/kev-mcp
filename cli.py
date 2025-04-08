import typer
from typing import Optional
from cisa_vuln_checker import get_recent_cves, check_cve_exists
import json

app = typer.Typer()

@app.command()
def recent_cves(
    days: Optional[int] = typer.Option(None, help="Number of days to look back"),
    hours: Optional[int] = typer.Option(None, help="Number of hours to look back"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format")
):
    """Get all CVEs added in the last X days or hours."""
    vulnerabilities = get_recent_cves(days, hours)
    
    if json_output:
        print(json.dumps(vulnerabilities, indent=2))
    else:
        for vuln in vulnerabilities:
            print(f"\nCVE ID: {vuln['cveID']}")
            print(f"Vendor/Project: {vuln['vendorProject']}")
            print(f"Product: {vuln['product']}")
            print(f"Vulnerability Name: {vuln['vulnerabilityName']}")
            print(f"Date Added: {vuln['dateAdded']}")
            print(f"Description: {vuln['shortDescription']}")
            print(f"Required Action: {vuln['requiredAction']}")
            print(f"Due Date: {vuln['dueDate']}")
            if vuln['knownRansomwareCampaignUse']:
                print(f"Ransomware Campaign Use: {vuln['knownRansomwareCampaignUse']}")
            if vuln['notes']:
                print(f"Notes: {vuln['notes']}")
            if vuln['cwes']:
                print(f"CWEs: {', '.join(vuln['cwes'])}")
            print("-" * 80)

@app.command()
def check_cve(
    cve_id: str = typer.Argument(..., help="The CVE ID to check (e.g., CVE-2023-1234)"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format")
):
    """Check if a given CVE exists in the list and display its details."""
    vulnerability = check_cve_exists(cve_id)
    
    if vulnerability:
        if json_output:
            print(json.dumps(vulnerability, indent=2))
        else:
            print(f"\nCVE ID: {vulnerability['cveID']}")
            print(f"Vendor/Project: {vulnerability['vendorProject']}")
            print(f"Product: {vulnerability['product']}")
            print(f"Vulnerability Name: {vulnerability['vulnerabilityName']}")
            print(f"Date Added: {vulnerability['dateAdded']}")
            print(f"Description: {vulnerability['shortDescription']}")
            print(f"Required Action: {vulnerability['requiredAction']}")
            print(f"Due Date: {vulnerability['dueDate']}")
            if vulnerability['knownRansomwareCampaignUse']:
                print(f"Ransomware Campaign Use: {vulnerability['knownRansomwareCampaignUse']}")
            if vulnerability['notes']:
                print(f"Notes: {vulnerability['notes']}")
            if vulnerability['cwes']:
                print(f"CWEs: {', '.join(vulnerability['cwes'])}")
    else:
        print(f"CVE {cve_id} does not exist in the list")

if __name__ == "__main__":
    app() 