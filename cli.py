import typer
from typing import Optional
from cisa_vuln_checker import get_recent_cves, check_cve_exists

app = typer.Typer()

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