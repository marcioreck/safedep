import re

DANGEROUS_JS_PATTERNS = {
    r"\beval\s*\(": "Evaluation of strings as code (eval)",
    r"\bexec\s*\(": "Execution of external commands (exec)",
    r"\bchild_process\.exec\s*\(": "Execution of external commands (child_process.exec)",
    r"\bchild_process\.spawn\s*\(": "Spawning of new processes (child_process.spawn)",
    r"\bprocess\.env\b": "Accessing environment variables",
    r"\bsetInterval\s*\(.*['\"].*['\"]\s*,\s*\d+\s*\)": "Potential code injection in setInterval",
    r"\bsetTimeout\s*\(.*['\"].*['\"]\s*,\s*\d+\s*\)": "Potential code injection in setTimeout"
}

def scan_js_code(content):
    """
    Scan JS/TS code for dangerous patterns using regex.
    """
    findings = []
    lines = content.splitlines()
    
    for i, line in enumerate(lines):
        # Skip comments
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            continue
            
        for pattern, description in DANGEROUS_JS_PATTERNS.items():
            if re.search(pattern, line):
                findings.append({
                    "pattern": pattern,
                    "description": description,
                    "line": i + 1
                })
                
    return findings
