import click
from rich.console import Console
from rich.table import Table
from .utils.pypi_client import get_package_info
from .utils.npm_client import get_npm_package_info
from .utils.cargo_client import get_cargo_package_info
from .scanner.typosquatting import check_typosquatting
from .scanner.reputation import analyze_reputation
from .scanner.static_analysis import scan_static_code
from .scanner.sandbox import SandboxScanner
from .scanner.npm_scanner import scan_npm_package
from .scanner.cargo_scanner import scan_cargo_package
from .scanner.js_scanner import scan_js_code
from .scanner.python_scanner import scan_python_manifest
from .hub import get_audited_package
import os

console = Console()

@click.group()
def cli():
    """SafeDep: Your Dependency Guardian."""
    pass

@cli.command()
@click.argument('package_name')
@click.option('--sandbox', is_flag=True, help='Run installation in a sandbox to monitor behavior.')
@click.option('--ecosystem', type=click.Choice(['python', 'npm', 'cargo']), default='python', help='Package ecosystem.')
def check(package_name, sandbox, ecosystem):
    """Analyze a package before installing."""
    console.print(f"[bold blue]SafeDep Analysis for: {package_name} ({ecosystem})[/bold blue]\n")
    
    # 1. Typosquatting
    console.print("[yellow]Checking for Typosquatting...[/yellow]")
    similar = check_typosquatting(package_name, ecosystem=ecosystem)

    if similar:
        console.print(f"[bold red]⚠ WARNING: This package is very similar to the popular package '{similar}'![/bold red]")
    else:
        console.print("[green]✓ No typosquatting detected.[/green]")
        
    # 2. Reputation
    console.print("\n[yellow]Checking Reputation...[/yellow]")
    if ecosystem == "python":
        info = get_package_info(package_name)
    elif ecosystem == "npm":
        info = get_npm_package_info(package_name)
    elif ecosystem == "cargo":
        info = get_cargo_package_info(package_name)
    
    score, findings = analyze_reputation(info, ecosystem=ecosystem)

    
    color = "red" if score < 50 else "yellow" if score < 80 else "green"
    console.print(f"Reputation Score: [bold {color}]{score}/100[/bold {color}]")
    for finding in findings:
        console.print(f" - {finding}")
        
    # 3. Sandboxing (Optional)
    if sandbox:
        console.print(f"\n[yellow]Starting Sandbox Analysis ({ecosystem})...[/yellow]")
        scanner = SandboxScanner()
        behavioral_findings = scanner.run_package_install(package_name, ecosystem=ecosystem)
        
        if isinstance(behavioral_findings, dict) and "error" in behavioral_findings:
            console.print(f"[bold red]⚠ Sandbox Error: {behavioral_findings['error']}[/bold red]")
        elif behavioral_findings:
            console.print("[bold red]⚠ BEHAVIORAL WARNINGS DETECTED:[/bold red]")
            for finding in behavioral_findings:
                console.print(f" - {finding}")
        else:
            console.print("[green]✓ No suspicious behavior detected in sandbox.[/green]")
        
    # --- SafeDep Hub & Shield ---
    console.print("\n[yellow]Checking SafeDep Hub...[/yellow]")
    audited_info = get_audited_package(package_name, ecosystem=ecosystem)
    
    if audited_info:
        console.print("🛡️ [bold green]SafeDep Shield: AUDITED & CLEAN[/bold green]")
        console.print(f"[dim]Last Audit: {audited_info.get('last_audit', 'Unknown')}[/dim]")
        console.print(f"[dim]Notes: {audited_info.get('notes', 'No notes available.')}[/dim]")
        
        # Security Badge Snippet
        badge_url = f"https://img.shields.io/badge/SafeDep-Audited-green?logo=github"
        console.print(f"\n[bold blue]Add this Security Badge to your README:[/bold blue]")
        console.print(f"Markdown: `[![SafeDep Audited]({badge_url})](https://github.com/marcioreck/safedep)`")
    else:
        console.print("[dim]This package is not yet in the SafeDep Hub. Community audits are welcome![/dim]")

    console.print("\n[bold green]Analysis Complete.[/bold green]")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def scan(path):
    """Scan local files for dangerous code."""
    console.print(f"[bold blue]Scanning directory: {path}[/bold blue]\n")
    
    findings_found = False
    
    # Directories to exclude from scanning
    EXCLUDED_DIRS = {"venv", ".venv", "node_modules", ".git", "__pycache__", ".pytest_cache"}
    
    for root, dirs, files in os.walk(path):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # --- Python Static Analysis ---
            if file.endswith(".py"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_static_code(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path} (Python):[/bold red]")
                        for f in findings:
                            console.print(f"  - Line {f['line']}: Call to {f['function']}")
            
            # --- JS/TS Static Analysis ---
            elif file.endswith(".js") or file.endswith(".ts"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_js_code(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path} (JS/TS):[/bold red]")
                        for f in findings:
                            console.print(f"  - Line {f['line']}: {f['description']}")
            
            # --- Python Manifest Analysis ---
            elif file == "requirements.txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_python_manifest(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path} (Python):[/bold red]")
                        for f in findings:
                            console.print(f"  - {f['package']}: {f['reason']}")

            # --- NPM Manifest Analysis ---


            elif file == "package.json":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_npm_package(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path} (NPM):[/bold red]")
                        for f in findings:
                            console.print(f"  - {f['package']}: {f['reason']}")

            # --- Cargo Manifest Analysis ---
            elif file == "Cargo.toml":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    findings = scan_cargo_package(content)
                    if findings:
                        findings_found = True
                        console.print(f"[bold red]⚠ Found {len(findings)} issues in {file_path} (Cargo):[/bold red]")
                        for f in findings:
                            console.print(f"  - {f['package']}: {f['reason']}")
                            
    if not findings_found:
        console.print("[green]✓ No dangerous patterns or suspicious dependencies found.[/green]")


def main():
    cli()

if __name__ == "__main__":
    main()
