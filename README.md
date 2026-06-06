# Parrot OS 7.2 HTB Edition - Build Automation Playbook

This repository contains an updated and modernized Ansible playbook (originally designed by Ippsec) to automate the configuration and customization of a **Parrot OS 7.2 HTB Edition** virtual machine or local install.

It configures a complete, high-productivity ethical hacking and development environment with custom terminal styling, browser extensions, global proxy configurations, logging rules, VSCode plugins, and modern security tools.

---

## What's Configured?

### 1. Terminal Customization
- **Shell (`.bashrc`):** 
  - Forces terminal session encoding to `UTF-8` globally (resolving Python/Ansible encoding errors).
  - Custom multi-line prompt that parses active network interfaces, IP addresses, and Hack The Box VPN connection status dynamically.
  - Adds helpful shortcuts (like `_` as an alias for `sudo` and `_i` for `sudo -i`).
  - Pre-configures search `PATH` to include `~/go/bin` and `~/.local/bin`.
- **MATE Terminal Profile:** Restores Ippsec's custom "Video" profile (large high-contrast fonts, custom palette) for visibility and streaming.
- **Tmux:** Custom status bar styles, vi-mode window navigation, clipboard integration (`xclip`), and join/send pane shortcuts.

### 2. VSCode Configuration
- Native installation of Visual Studio Code (`code`) using Microsoft's official signing keys and repositories.
- Automatic, idempotent installation of security and programming extensions:
  - **Snyk Security** (vulnerability scanner)
  - **Python** (IntelliSense and debugging)
  - **Go** (Golang syntax and utilities)
  - **C/C++** (native compilation tools support)
  - **PHP Tools** (PHP language support)
  - **GitHub Copilot** (AI assistance)
  - **Code Spell Checker**
  - **YAML** (Ansible playbook syntax highlighting)

### 3. Browser & Proxy Setup (Burp Suite & Firefox)
- **Burp Suite:**
  - Automated headless JRE/Java launch to generate the Burp CA certificate dynamically.
  - Registers the CA certificate in the system trust store (`update-ca-certificates`) so system CLI tools trust Burp traffic.
  - Copies and applies the default custom dark-themed community config, setting SOCKS configurations, layout styles, and optimal hotkeys.
- **Firefox:**
  - Configures system-wide Firefox Enterprise policies.
  - Automatically installs and locks trusted Burp Suite CA certificates.
  - Auto-installs critical pentesting and utility extensions:
    - **FoxyProxy Standard** (quick proxy switcher)
    - **Hack-Tools** (payload cheat sheet and generator)
    - **Cookie-Editor** (cookie inspector/editor)
    - **Wappalyzer** (web technology detector)
    - **Dark Reader** (forced dark modes)

### 4. Hacking & Development Tools
- **Pipx Packages (Python CLI):**
  - `impacket` (latest Git version)
  - `netexec` (successor to CME, installed via pipx to avoid package conflicts)
  - `certipy-ad` (Active Directory Certificate Services tool)
  - `bloodhound-ce` (Python collector for BloodHound Community Edition)
- **Go Installed Binaries:**
  - `kerbrute` (Active Directory Kerberos brute-forcing tool)
- **Ruby Gems:**
  - `evil-winrm` (interactive WinRM shell) along with essential WinRM and parsing library dependencies.
- **Standalone Binaries:**
  - `chisel` (TCP/UDP tunnels over HTTP, Linux & Windows amd64 binaries in `/opt/chisel`)
  - `PEASS-ng` (`linpeas.sh` and `winPEASx64.exe` binaries in `/opt/peas`)
  - `chainsaw` (rapid event log analysis tool in `/opt/chainsaw`)
  - `BloodHound Legacy GUI` (standalone client extractor in `/opt/BloodHound-Legacy`)
- **BloodHound Community Edition (CE):**
  - Configures localized docker-compose servers in `/opt/bloodhound/server`.
  - Runs BloodHound CE via Docker, binds the interface port to `8088`, and logs the initial generated admin password to `/opt/bloodhound/server/initial-password.txt`.

### 5. System & Logging Configuration
- Configures passwordless `sudo` rights (`NOPASSWD`) for the invoking user.
- Installs and enables `rsyslog` and `ufw` firewall rules (logging TCP SYN packets in the input chain).
- Installs `auditd` and sets up optimized audit rules.
- Installs **Laurel v0.7.3** (JSON logging plugin for auditd) ensuring modern glibc compatibility with Parrot OS 7.2.

---

## Instructions

To build and customize your environment in one command, simply run the bootstrap script:

1. Clone and enter the repository:
   ```bash
   git clone https://github.com/yokesh-kumar-M/parrot-build.git
   cd parrot-build
   ```

2. Make the bootstrap script executable:
   ```bash
   chmod +x setup.sh
   ```

3. Run the bootstrap runner:
   ```bash
   ./setup.sh
   ```

The script will automatically refresh your sudo credentials, configure your terminal to use UTF-8, install base compilers and package dependencies (including `Ansible`), and run the custom playbook.
