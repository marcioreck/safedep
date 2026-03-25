from .typosquatting import check_typosquatting

def scan_python_manifest(content):
    """
    Scan requirements.txt for typosquatted packages.
    """
    findings = []
    lines = content.splitlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Basic parsing: package==version or just package
        package = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
        
        similar = check_typosquatting(package, ecosystem="python")
        if similar:
            findings.append({
                "package": package,
                "reason": f"Potential typosquatting for '{similar}'"
            })

            
    return findings
