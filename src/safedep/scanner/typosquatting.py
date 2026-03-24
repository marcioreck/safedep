from difflib import SequenceMatcher

# Top 50 most popular Python packages (simplified list for MVP)
POPULAR_PACKAGES = [
    "requests", "numpy", "pandas", "matplotlib", "boto3", "six", "python-dateutil",
    "pyyaml", "s3transfer", "urllib3", "pip", "setuptools", "wheel", "certifi",
    "idna", "charset-normalizer", "requests", "flask", "django", "tensorflow",
    "pytorch", "scikit-learn", "scipy", "black", "pytest", "tox", "ansible",
    "celery", "redis", "pydantic", "fastapi", "sqlalchemy", "cryptography",
    "pyjwt", "aiohttp", "click", "rich", "tqdm", "pillow", "lxml", "pytz",
    "colorama", "packaging", "importlib-metadata", "zipp", "typing-extensions"
]

def check_typosquatting(package_name, threshold=0.8):
    """
    Check if a package name is suspiciously similar to a popular package.
    Returns the similar package name if found, else None.
    """
    package_name = package_name.lower().replace("_", "-")
    
    # If it's already a popular package, it's not typosquatting (it's the original)
    if package_name in POPULAR_PACKAGES:
        return None

    for popular in POPULAR_PACKAGES:
        # Check similarity
        similarity = SequenceMatcher(None, package_name, popular).ratio()
        if similarity >= threshold:
            return popular
            
    return None
