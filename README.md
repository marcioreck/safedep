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

## 🚀 How to Use (CLI)

```bash
# Analyze a package before installing
safedep check requests

# Analyze your entire project
safedep scan .
```

---

## 🗺️ Development Roadmap

### Phase 1: Foundation (MVP) - "The Scanner" 🏗️
Implementation of name similarity analysis (Anti-Typosquatting).
Reputation verification (package creation date, popularity, author history).
Static code scanner to find dangerous functions (eval(), os.system(), requests.post() in setup scripts).

### Phase 2: Intelligence (Beta) - "The Behavioralist" 🧠
Sandboxing: Integration with Docker/Podman to run setup.py and monitor system calls (syscalls).
Multi-language Support: Adding support for NPM (Node.js) and Cargo (Rust) in addition to Python.
CI/CD Integration: GitHub Actions to block PRs with suspicious dependencies.

### Phase 3: Community and Sustainability - "The Shield" 🛡️
SafeDep Hub: A community-driven database of "audited and clean" packages.
Security Badges: A system for repositories to display security trust seals.
Sponsorship Program: Launching the Sponsors program to maintain the heavy analysis infrastructure.

---

## 🤝 Contribute & Sponsor
This project is 100% free and community-focused.
If you believe in a safer software ecosystem, consider becoming a contributor or sponsor.
Give a ⭐ on GitHub
Report Bugs
Become a Sponsor: [GitHub Sponsors](https://github.com/sponsors/marcioreck) / [OpenCollective](https://opencollective.com/marcioreck)
Developed for those who prioritize security.
