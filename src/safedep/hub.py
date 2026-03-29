import os
import json
import requests
from pathlib import Path

HUB_URL = "https://raw.githubusercontent.com/marcioreck/safedep/main/hub/audited_packages.json"
CACHE_DIR = Path.home() / ".safedep"
CACHE_FILE = CACHE_DIR / "hub.json"

def fetch_hub_data():
    """Fetch audited packages from the Hub and cache them locally."""
    # Local development fallback
    local_hub = Path(__file__).parent.parent.parent / "hub" / "audited_packages.json"
    if local_hub.exists():
        try:
            with open(local_hub, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    try:
        response = requests.get(HUB_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Ensure cache directory exists
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return data
    except Exception:
        pass
    
    # Load from cache if fetch fails
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    return {"packages": []}

def get_audited_package(package_name, ecosystem="python"):
    """Check if a package is audited in the Hub."""
    data = fetch_hub_data()
    for pkg in data.get("packages", []):
        if pkg["name"].lower() == package_name.lower() and pkg["ecosystem"] == ecosystem:
            return pkg
    return None
