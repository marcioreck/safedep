from difflib import SequenceMatcher

# Popular packages grouped by ecosystem
POPULAR_PACKAGES = {
    "python": [
        "requests", "numpy", "pandas", "matplotlib", "boto3", "six", "python-dateutil",
        "pyyaml", "s3transfer", "urllib3", "pip", "setuptools", "wheel", "certifi",
        "idna", "charset-normalizer", "flask", "django", "tensorflow",
        "pytorch", "scikit-learn", "scipy", "black", "pytest", "tox", "ansible",
        "celery", "redis", "pydantic", "fastapi", "sqlalchemy", "cryptography",
        "pyjwt", "aiohttp", "click", "rich", "tqdm", "pillow", "lxml", "pytz",
        "colorama", "packaging", "importlib-metadata", "zipp", "typing-extensions"
    ],
    "npm": [
        "react", "lodash", "express", "commander", "chalk", "tslib", "axios",
        "moment", "debug", "fs-extra", "bluebird", "async", "prop-types", "request"
    ],
    "cargo": [
        "tokio", "serde", "rand", "syn", "quote", "log", "serde_json", "anyhow",
        "regex", "clap", "itertools", "lazy_static", "futures", "hyper"
    ]
}

def check_typosquatting(package_name, ecosystem="python", threshold=0.8):
    """
    Check if a package name is suspiciously similar to a popular package in its ecosystem.
    Returns the similar package name if found, else None.
    """
    package_name = package_name.lower().replace("_", "-")
    popular_list = POPULAR_PACKAGES.get(ecosystem, POPULAR_PACKAGES["python"])
    
    # If it's already a popular package in this ecosystem, it's not typosquatting
    if package_name in popular_list:
        return None

    for popular in popular_list:
        # Check similarity
        similarity = SequenceMatcher(None, package_name, popular).ratio()
        if similarity >= threshold:
            return popular
            
    return None

