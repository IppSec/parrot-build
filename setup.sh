#!/bin/bash
# ==============================================================================
#  Parrot OS 7.2 HTB Edition - Build Automation Bootstrap Script
#  Author: Antigravity AI
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Force terminal session to UTF-8 to resolve Ansible/Python locale errors
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

echo -e "\e[1;34m"
echo "=========================================================="
echo "    Parrot OS 7.2 HTB Edition - Automation Bootstrap       "
echo "=========================================================="
echo -e "\e[0m"

# Ensure sudo token is active
echo -e "\e[1;33m[*] Refreshing sudo credentials...\e[0m"
sudo -v

# Clean up conflicting legacy VS Code keys and sources from previous runs
for file in /etc/apt/sources.list /etc/apt/sources.list.d/*; do
    if [ -f "$file" ] && sudo grep -q "packages.microsoft.gpg" "$file"; then
        echo -e "\e[1;33m[*] Removing conflicting VS Code repository config in $file...\e[0m"
        sudo rm -f "$file"
    fi
done
if [ -f /etc/apt/keyrings/packages.microsoft.gpg ]; then
    sudo rm -f /etc/apt/keyrings/packages.microsoft.gpg
fi

# Check for updates and install base dependencies
echo -e "\e[1;33m[*] Updating package list & installing base dependencies...\e[0m"
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git curl dconf-cli build-essential ruby ruby-dev golang-go

# Install Ansible safely (handling PEP 668 / Debian 12 Managed Environment)
if ! command -v ansible-playbook &> /dev/null; then
    echo -e "\e[1;33m[*] Ansible is not installed. Installing...\e[0m"
    sudo apt-get install -y ansible || \
    python3 -m pip install --break-system-packages --user ansible || \
    python3 -m pip install --user ansible
else
    echo -e "\e[1;32m[+] Ansible is already installed.\e[0m"
fi

# Run the playbook
echo -e "\e[1;32m[+] Starting Parrot Customization Playbook...\e[0m"
ansible-playbook main.yml

echo -e "\e[1;32m[+] Bootstrap completed successfully!\e[0m"
