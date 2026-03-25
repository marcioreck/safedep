from datetime import datetime

def analyze_reputation(package_info, ecosystem="python"):
    """
    General entry point for reputation analysis across ecosystems.
    """
    if not package_info:
        return 0, [f"Package not found in {ecosystem} registry."]
        
    if ecosystem == "npm":
        return analyze_npm_reputation(package_info)
    elif ecosystem == "cargo":
        return analyze_cargo_reputation(package_info)
    else:
        return analyze_python_reputation(package_info)

def analyze_python_reputation(package_info):
    """Analyze Python/PyPI reputation."""
    info = package_info.get("info", {})
    releases = package_info.get("releases", {})
    
    score = 100
    findings = []
    
def analyze_python_reputation(package_info):
    """Analyze Python/PyPI reputation."""
    info = package_info.get("info", {})
    releases = package_info.get("releases", {})
    
    score = 100
    findings = []
    
    # 1. Age check & Staleness
    first_release_time = None
    latest_release_time = None
    
    for version in releases:
        if releases[version]:
            upload_time = releases[version][0].get("upload_time_iso_8601")
            if upload_time:
                dt = datetime.fromisoformat(upload_time.replace("Z", "+00:00"))
                if first_release_time is None or dt < first_release_time:
                    first_release_time = dt
                if latest_release_time is None or dt > latest_release_time:
                    latest_release_time = dt
    
    score, age_findings = _calculate_age_score(first_release_time, score)
    findings.extend(age_findings)
    
    score, stale_findings = _calculate_stale_score(latest_release_time, score)
    findings.extend(stale_findings)


    # 2. Author check
    author = info.get("author")
    if not author or author.lower() in ["none", "unknown", ""]:
        score -= 20
        findings.append("Missing or anonymous author.")

    return max(0, score), findings

def analyze_npm_reputation(package_info):
    """Analyze NPM reputation."""
    score = 100
    findings = []
    
    # 1. Age check & Staleness
    time_info = package_info.get("time", {})
    created_time = time_info.get("created")
    modified_time = time_info.get("modified")
    
    first_release_time = None
    if created_time:
        first_release_time = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
    
    latest_release_time = None
    if modified_time:
        latest_release_time = datetime.fromisoformat(modified_time.replace("Z", "+00:00"))

    score, age_findings = _calculate_age_score(first_release_time, score)
    findings.extend(age_findings)
    
    score, stale_findings = _calculate_stale_score(latest_release_time, score)
    findings.extend(stale_findings)


    # 2. Author check
    author = package_info.get("author", {})
    author_name = str(author) if isinstance(author, str) else author.get("name")
    if not author_name:
        score -= 20
        findings.append("Missing or anonymous author.")

    return max(0, score), findings

def analyze_cargo_reputation(package_info):
    """Analyze Cargo reputation."""
    crate = package_info.get("crate", {})
    score = 100
    findings = []
    
    # 1. Age check & Staleness
    created_at = crate.get("created_at")
    updated_at = crate.get("updated_at")
    
    first_release_time = None
    if created_at:
        first_release_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        
    latest_release_time = None
    if updated_at:
        latest_release_time = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

    score, age_findings = _calculate_age_score(first_release_time, score)
    findings.extend(age_findings)
    
    score, stale_findings = _calculate_stale_score(latest_release_time, score)
    findings.extend(stale_findings)


    # 2. Downloads check (Crates.io provides this)
    downloads = crate.get("downloads", 0)
    if downloads < 1000:
        score -= 30
        findings.append(f"Low download count: {downloads}")

    return max(0, score), findings

def _calculate_age_score(first_release_time, score):
    """Helper to calculate age score for any ecosystem."""
    findings = []
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
    return score, findings

def _calculate_stale_score(latest_release_time, score):
    """Helper to calculate staleness score."""
    findings = []
    if latest_release_time:
        days_stale = (datetime.now(latest_release_time.tzinfo) - latest_release_time).days
        if days_stale > 730:
            score -= 50
            findings.append(f"Extremely stale package: last updated {days_stale} days ago.")
        elif days_stale > 365:
            score -= 30
            findings.append(f"Stale package: last updated {days_stale} days ago.")
    return score, findings
