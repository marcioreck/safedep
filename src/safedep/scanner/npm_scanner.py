import json

from .typosquatting import check_typosquatting

def scan_npm_package(content):
    """
    Scans a package.json file for suspicious dependencies.
    """
    try:
        data = json.loads(content)
        dependencies = data.get("dependencies", {})
        dev_dependencies = data.get("devDependencies", {})
        
        all_deps = {**dependencies, **dev_dependencies}
        findings = []
        
        for dep in all_deps:
            similar = check_typosquatting(dep, ecosystem="npm")
            if similar:
                 findings.append({
                    "package": dep,
                    "reason": f"Potential typosquatting for '{similar}'"
                })

        
        return findings
    except json.JSONDecodeError:
        return [{"error": "Invalid package.json"}]

