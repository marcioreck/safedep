import subprocess
import os
import json

class SandboxScanner:
    def __init__(self, image="python:3.10-slim"):
        self.image = image

    def run_package_install(self, package_name, ecosystem="python"):
        """
        Runs the package installation in a Docker sandbox and monitors system calls.
        """
        ecosystem_config = {
            "python": {
                "image": "python:3.10-slim",
                "cmd": f"python3 -m venv /tmp/venv && source /tmp/venv/bin/activate && pip install {package_name}"
            },
            "npm": {
                "image": "node:18-slim",
                "cmd": f"cd /tmp && npm init -y && npm install {package_name}"
            },
            "cargo": {
                "image": "rust:1-slim",
                "cmd": f"cd /tmp && cargo new temp_app && cd temp_app && cargo add {package_name} && cargo build"
            }

        }

        config = ecosystem_config.get(ecosystem, ecosystem_config["python"])
        image = config["image"]
        cmd = config["cmd"]

        docker_cmd = [
            "docker", "run", "--rm",
            image,
            "bash", "-c",
            f"apt-get update && apt-get install -y strace curl build-essential && "
            f"strace -e trace=network,file -o /tmp/strace.log bash -c '{cmd}' && "
            f"cat /tmp/strace.log"
        ]




        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, check=True)
            return self._parse_strace(result.stdout)
        except subprocess.CalledProcessError as e:
            return {"error": f"Sandbox execution failed: {e.stderr}"}
        except FileNotFoundError:
            return {"error": "Docker not found. Please ensure Docker is installed and running."}

    def _parse_strace(self, log_content):
        """
        Parses strace logs for suspicious behavior with noise reduction.
        """
        findings = []
        lines = log_content.splitlines()
        
        # Paths and patterns that are considered safe/standard during installation
        IGNORE_PATTERNS = [
            "/etc/ld.so.cache", "/lib/", "/usr/lib/", "/usr/share/locale/",
            "/etc/localtime", "/etc/os-release", "/etc/debian_version",
            "/etc/nsswitch.conf", "/etc/host.conf", "/etc/resolv.conf", "/etc/hosts",
            "/tmp/venv/", "/tmp/pip-", "pyvenv.cfg", "pybuilddir.txt",
            "/usr/bin/python3", "/root/.cache/pip", "O_RDONLY", "ENOENT",
            "/dev/null", "/dev/tty", "/dev/urandom", "/dev/random",
            "/tmp/npm-", "/tmp/cargo", "node_modules", "target/",
            "/tmp/tmp", "/tmp/h8o", "/root/.npm",
            "/usr/local/cargo/registry", "/usr/local/cargo/.package-cache",
            "/usr/local/cargo/.global-cache", ".cargo-ok", "CACHEDIR.TAG", ".rustc_info.json"
        ]




        # Standard network behavior for package managers (DNS and Repo HTTPS)
        SAFE_NETWORK_PATTERNS = [
            "sin_port=htons(53)", "sin_port=htons(443)",      # IPv4 DNS/HTTPS
            "sin6_port=htons(53)", "sin6_port=htons(443)",     # IPv6 DNS/HTTPS
            "sa_family=AF_UNSPEC"                             # Resolution noise
        ]


        suspicious_patterns = {
            "connect": "Network connection attempted",
            "openat": "Sensitive file access",
            "unlink": "File deletion attempted",
            "unlinkat": "File deletion attempted"
        }


        for line in lines:
            if len(findings) >= 50:
                findings.append("... [further findings truncated for brevity]")
                break
                
            is_ignored = False

            for pattern in IGNORE_PATTERNS:
                if pattern in line:
                    is_ignored = True
                    break
            
            if is_ignored:
                continue

            for pattern, description in suspicious_patterns.items():
                if pattern in line:
                    # Special handling for network filtering
                    if pattern == "connect":
                        if any(p in line for p in SAFE_NETWORK_PATTERNS):
                            continue
                    
                    findings.append(f"{description}: {line.strip()}")

        return findings

