from setuptools import setup, find_packages

setup(
    name="cisa-vuln-checker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "duckdb",
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "cisa-vuln-checker=cisa_vuln_checker.cli:app",
        ],
    },
) 