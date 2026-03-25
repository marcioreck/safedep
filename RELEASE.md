# SafeDep Release Guide

This document outlines the steps to release a new version of SafeDep to GitHub and PyPI.

## 1. Local Manual Release

To manually build and upload the package to PyPI, ensure you have `build` and `twine` installed:

```bash
pip install build twine
```

### Build the Package
```bash
python3 -m build
```

### Upload to PyPI
```bash
# Upload to TestPyPI first (recommended)
python3 -m twine upload --repository testpypi dist/*

# Upload to PyPI
python3 -m twine upload dist/*
```

---

## 2. Automated Release (GitHub Actions)

SafeDep is configured to automatically publish to PyPI and create a GitHub Release when a new tag is pushed.

### Triggering a Release
1. Update the version in `pyproject.toml`:
   ```toml
   version = "0.1.1" # Update to the new version
   ```
2. Commit and push the change.
3. Create and push a new tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

### Required GitHub Secrets
To make the automated release work, you must add the following secret to your GitHub repository:
- `PYPI_API_TOKEN`: Your PyPI API token.

The workflow is defined in `.github/workflows/release.yml`.
