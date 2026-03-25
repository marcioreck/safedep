import requests

def get_cargo_package_info(package_name):
    """Fetch package metadata from Crates.io."""
    url = f"https://crates.io/api/v1/crates/{package_name}"
    headers = {"User-Agent": "SafeDep (https://github.com/marcioreck/safedep)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None
