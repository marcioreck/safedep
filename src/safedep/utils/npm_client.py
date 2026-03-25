import requests

def get_npm_package_info(package_name):
    """Fetch package metadata from NPM Registry."""
    url = f"https://registry.npmjs.org/{package_name}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None
