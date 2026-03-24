from datetime import datetime

def analyze_reputation(package_info):
    """
    Analyze package reputation based on PyPI metadata.
    Returns a score (0-100) and a list of findings.
    """
    if not package_info:
        return 0, ["Package not found on PyPI."]
        
    info = package_info.get("info", {})
    releases = package_info.get("releases", {})
    
    score = 100
    findings = []
    
    # 1. Age check
    first_release_time = None
    for version in releases:
        if releases[version]:
            upload_time = releases[version][0].get("upload_time_iso_8601")
            if upload_time:
                dt = datetime.fromisoformat(upload_time.replace("Z", "+00:00"))
                if first_release_time is None or dt < first_release_time:
                    first_release_time = dt
    
    if first_release_time:
        days_old = (datetime.now(first_release_time.tzinfo) - first_release_time).days
        if days_old < 30:
            score -= 40
            findings.append(f"Very young package: {days_old} days old.")
        elif days_old < 180:
            score -= 20
            findings.append(f"Relatively new package: {days_old} days old.")
    else:
        score -= 50
        findings.append("Could not determine package age.")

    # 2. Author check
    author = info.get("author")
    if not author or author.lower() in ["none", "unknown", ""]:
        score -= 20
        findings.append("Missing or anonymous author.")

    # 3. Maintainer count (if available in a real scenario, here we'll simplify)
    
    return max(0, score), findings
