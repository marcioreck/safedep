import requests

def get_package_info(package_name):
    """Fetch package metadata from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None
