# Instructions
1. Install Parrot HTB Edition
2. Run following commands
```
#Install Ansible
python3 -m pip install ansible --break-system-packages

#Add Ansible to PATH
export PATH="$PATH:$HOME/.local/bin"

#Clone repo
git clone https://github.com/n0isegat3/parrot-build
cd parrot-build

#Install requirements
ansible-galaxy install -r requirements.yml

#Make sure to have a sudo token
sudo whoami

#Run playbook
ansible-playbook main.yml
```
3. Enjoy

# Credits
Thank you ippsec for initial automation! You can find his repo on github.com/ippsec/parrot-build