#!/bin/bash
set -e # Exit if some of the commands fail

FIREWALL_TOOL=""

if command -v ufw &> /dev/null; then
    FIREWALL_TOOL="ufw"
elif command -v firewalld &> /dev/null; then
    FIREWALL_TOOL="firewalld"
else
    echo "no supported firewall tool found (ufw or firewalld) skipping firewall config" >&2
    exit 1
fi

if [ "$FIREWALL_TOOL" == "ufw" ]; then
    echo "configuring ufw"
    if ! sudo ufw status | grep -q "Status: active"; then
        sudo ufw enable &> /dev/null
    fi
    sudo ufw allow 6443/tcp
    sudo ufw allow from 10.42.0.0/16 to any
    sudo ufw allow from 10.43.0.0/16 to any
    echo "ufw configured"

elif [ "$FIREWALL_TOOL" == "firewalld" ]; then
    echo "configuring firewalld"
    if ! systemctl is-active --quiet firewalld; then
        echo "Starting firewalld"
        sudo systemctl start firewalld && sudo systemctl enable firewalld 
    fi

    sudo firewall-cmd --permanent --add-port=6443/tcp
    sudo firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16
    sudo firewall-cmd --permanent --zone=trusted --add-source=10.43.0.0/16
    sudo firewall-cmd --reload

else
    echo "Unrecognised firewall tool, firewall not configured"
    exit 1

fi


if command -v k3s &> /dev/null; then
    if systemctl is-active --quiet k3s; then
        echo "k3s binary found and service is running, skipping installation"

    else
        echo "k3s binary found, but service is not running, proceeding with start attempt"
        systemctl start k3s &> /dev/null
        systemctl status k3s &> /dev/null
    fi
else
    echo "k3s not found, starting installation"
fi


if ! command -v k3s &> /dev/null || ! systemctl is-active --quiet k3s; then
    echo "Downloading and installing k3s"
    sudo curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    echo "k3s installation executed"
else
    echo "k3s installation skipped, already present"
fi


echo "Setting kubeconfig permissions"
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
echo "Kubeconfig permissions set"

echo "k3s installation script finished"
