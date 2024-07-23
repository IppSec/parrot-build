** Make sure to pip install ansible, apt has an older copy **

Due to the newer versions of Ansible and Parrot OS, the Playbook couldn't run smoothly. I found two workarounds, one using pipx and the other installing Ansible system-wide. I think that the second workaround is more accurate with the end system that IppSec gets, so that's why I used the second approach instead of installing Ansible using pipx and isolating the app.

# Instructions updated (Ansible 9 \[core 2.17.2\] + Parrot OS Version 6.1 Lorikeet)
* Start with Parrot HTB Edition
* Install Ansible (python3 -m pip install ansible --break-system-packages)
* Clone and enter the repo (git clone)
* ansible-galaxy install -r requirements.yml
* ansible-playbook main.yml -K (-K for a prompt for the sudo password)

# Off-Video Changes
* Mate-Terminal Colors, I show how to configure it here (https://www.youtube.com/watch?v=2y68gluYTcc). I just did the steps in that video on my old VM to backup the color scheme, then copied it to this repo.
* Evil-Winrm/Certipy/SharpCollection/CME/Impacket, will make a video for these soon
* Updated BurpSuite Activation. Later versions of ansible would hang if a shell script started a process that didn't die. Put a timeout on the java process
