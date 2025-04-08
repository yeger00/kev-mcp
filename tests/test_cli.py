import pytest
from typer.testing import CliRunner
from cisa_vuln_checker.cli import app

runner = CliRunner()

def test_recent_cves_days():
    """Test getting recent CVEs by days."""
    result = runner.invoke(app, ["recent-cves", "--days", "1"])
    assert result.exit_code == 0
    # We can't predict the exact output, but we can check the format
    if result.stdout:
        assert "CVE-" in result.stdout

def test_recent_cves_hours():
    """Test getting recent CVEs by hours."""
    result = runner.invoke(app, ["recent-cves", "--hours", "24"])
    assert result.exit_code == 0
    if result.stdout:
        assert "CVE-" in result.stdout

def test_recent_cves_no_args():
    """Test that providing no arguments raises an error."""
    result = runner.invoke(app, ["recent-cves"])
    assert result.exit_code != 0
    assert "Either days or hours must be specified" in result.stdout

def test_check_cve_exists():
    """Test checking for an existing CVE."""
    # First get a real CVE from the recent list
    result = runner.invoke(app, ["recent-cves", "--days", "1"])
    if result.stdout:
        # Take the first CVE from the list
        cve = result.stdout.strip().split("\n")[0].split(": ")[1]
        # Now check if it exists
        result = runner.invoke(app, ["check-cve", cve])
        assert result.exit_code == 0
        assert "CVE ID:" in result.stdout

def test_check_cve_not_exists():
    """Test checking for a non-existent CVE."""
    result = runner.invoke(app, ["check-cve", "CVE-9999-9999"])
    assert result.exit_code == 0
    assert "CVE CVE-9999-9999 does not exist in the list" in result.stdout 