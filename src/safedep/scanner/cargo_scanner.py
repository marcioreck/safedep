import re

from .typosquatting import check_typosquatting

def scan_cargo_package(content):
    """
    Scans a Cargo.toml file for suspicious dependencies.
    """
    findings = []
    
    # Simple regex to find dependencies in Cargo.toml
    # [dependencies]
    # serde = "1.0"
    dep_pattern = re.compile(r'^(\w+)\s*=\s*".+"', re.MULTILINE)
    
    dependencies = dep_pattern.findall(content)
    
    for dep in dependencies:
        similar = check_typosquatting(dep, ecosystem="cargo")
        if similar:
            findings.append({
                "package": dep,
                "reason": f"Potential typosquatting for '{similar}'"
            })

            
    return findings

