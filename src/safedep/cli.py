import click
from rich.console import Console
from rich.table import Table
from .utils.pypi_client import get_package_info
from .scanner.typosquatting import check_typosquatting
from .scanner.reputation import analyze_reputation
from .scanner.static_analysis import scan_static_code
import os

console = Console()

@click.group()
def cli():
    """SafeDep: Your Dependency Guardian."""
    pass

@cli.command()
@click.argument('package_name')
def check(package_name):
    """Analyze a package before installing."""
    console.print(f"[bold blue]Safedep Analysis for: {package_name}[/bold blue]\n")
    
    # 1. Typosquatting
    console.print("[yellow]Checking for Typosquatting...[/yellow]")
    similar = check_typosquatting(package_name)
    if similar:
        console.print(f"[bold red]⚠ WARNING: This package is very similar to the popular package '{similar}'![/bold red]")
    else:
        console.print("[green]✓ No typosquatting detected.[/green]")
        
    # 2. Reputation
    console.print("\n[yellow]Checking Reputation...[/yellow]")
    info = get_package_info(package_name)
    score, findings = analyze_reputation(info)
    
    color = "red" if score < 50 else "yellow" if score < 80 else "green"
    console.print(f"Reputation Score: [bold {color}]{score}/100[/bold {color}]")
    for finding in findings:
        console.print(f" - {finding}")
        
    console.print("\n[bold green]Analysis Complete.[/bold green]")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def scan(path):
    """Scan local files for dangerous code."""
    console.print(f"[bold blue]Scanning directory: {path}[/bold blue]\n")
    
    findings_found = False
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_static_code(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path}:[/bold red]")
                        for f in findings:
                            console.print(f"  - Line {f['line']}: Call to {f['function']}")
                            
    if not findings_found:
        console.print("[green]✓ No dangerous code patterns found.[/green]")

def main():
    cli()

if __name__ == "__main__":
    main()
