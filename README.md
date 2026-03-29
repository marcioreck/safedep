# 🛡️ SafeDep: Your Dependency Guardian

**SafeDep** is an open-source tool designed to protect developers from Supply Chain Attacks. It analyzes packages and dependencies for malicious behavior, data exfiltration, and hidden vulnerabilities before you even install them.

> "Don't just scan for known vulnerabilities. Detect suspicious behavior."

---

## ✨ Why SafeDep?

The package ecosystem (PyPI, NPM, Cargo) is under constant attack from *Typosquatting*, *Dependency Injection*, and *Trojan Horses*. SafeDep goes beyond standard vulnerability databases (CVEs) by analyzing both the **static and dynamic behavior** of the code.

### Key Features
- 🔍 **Pre-install Sandbox**: Runs installation scripts in an isolated environment to monitor what they attempt to access.
- 📡 **Network Monitor**: Alerts you if a "text processing" package tries to make requests to unknown IP addresses.
- 🔑 **Secret Leak Detection**: Identifies if a package attempts to read your environment variables (`.env`) or API keys.
- 🏷️ **Typosquatting Protection**: Checks if a package name is dangerously similar to a popular one.

---

## 🛠️ Getting Started

To use **SafeDep** locally, clone the repository and install it in editable mode:

```bash
# create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install SafeDep in editable mode (so code changes are reflected immediately)
pip install -e .
```

### Sandbox Requirements
For behavioral analysis, **Docker** or **Podman** must be installed and running.
```bash
# Check if docker is available
docker --version
```

## 🚀 How to Use (CLI)

SafeDep provides several commands:


### 1. Check a package before installing
Analyzes a package (remote) for typosquatting and reputation risks.

**Python (default):**
```bash
safedep check <package_name>
```

**Python Typosquatting Example:**
```bash
# Detects similarity to 'requests'
safedep check requesst
```

**NPM:**
```bash
safedep check <package_name> --ecosystem npm
```

**Cargo (Rust):**
```bash
safedep check <package_name> --ecosystem cargo
```

### 2. Scan a local directory
Scans local files (**Python, JS, TS, NPM, Cargo**) for dangerous code patterns or suspicious dependencies (in `requirements.txt`, `package.json`, `Cargo.toml`). 

SafeDep automatically excludes common dependency and internal directories like `venv`, `node_modules`, and `.git` to focus on your project's source code.
```bash
safedep scan <path_to_directory>
```

### 3. Behavioral Analysis (Sandbox)
Runs a package installation in a Docker container and monitors for suspicious system calls.

**Python:**
```bash
safedep check <package_name> --sandbox
```

**NPM:**
```bash
safedep check <package_name> --ecosystem npm --sandbox
```

**Cargo:**
```bash
safedep check <package_name> --ecosystem cargo --sandbox
```

---

## 🗺️ Development Roadmap

### Phase 1: Foundation (MVP) - "The Scanner" ✅ (Implemented)
- ✅ Implementation of name similarity analysis (Anti-Typosquatting).
- ✅ Reputation verification (package creation date, author history).
- ✅ Static code scanner for dangerous functions.

### Phase 2: Intelligence (Beta) - "The Behavioralist" 🧠 ✅ (Implemented)
- ✅ Sandboxing: Integration with Docker/Podman to run setup.py and monitor system calls (syscalls).
- ✅ Multi-language Support: Support for NPM (Node.js) and Cargo (Rust) in addition to Python.
- ✅ CI/CD Integration: GitHub Actions to block PRs with suspicious dependencies.

### Phase 3: Community and Sustainability - "The Shield" 🛡️  [/] (In Progress)
- [x] **SafeDep Hub**: A community-driven database of "audited and clean" packages.
- [x] **Security Badges**: A system for repositories to display security trust seals.
- [/] **Sponsorship Program**: Launching the Sponsors program to maintain the heavy analysis infrastructure.

---

## 🛡️ The Shield: SafeDep Hub

The **SafeDep Hub** is a crowdsourced database of packages that have been manually audited by the community and verified as safe. 

### How it works:
1. When you run `safedep check <package>`, the tool queries the Hub.
2. If the package is found, you'll see the **SafeDep Shield** and a Markdown snippet to add a trust badge to your repo.
3. Contributions are made via Pull Requests to the `hub/audited_packages.json` file.

### Get your Security Badge
If your package is audited, display your trust seal:
`[![SafeDep Audited](https://img.shields.io/badge/SafeDep-Audited-green?logo=github)](https://github.com/marcioreck/safedep)`

---

## 🤝 Contribute & Sponsor
SafeDep is a **zerocost marketing** open-source initiative. We rely on community audits to grow "The Shield".

### How to Help
- **Audit a Package**: Submit a PR to the [Hub](https://github.com/marcioreck/safedep/tree/main/hub).
- **Give a ⭐**: Help us reach more developers.
- **Report Bugs**: Help us improve the scanner.
- **Become a Sponsor**: Support the infrastructure for deep behavioral analysis. 
  - [GitHub Sponsors](https://github.com/sponsors/marcioreck)
  - [OpenCollective](https://opencollective.com/marcio-reck)

Developed for those who prioritize security.
