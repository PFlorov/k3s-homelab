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

# ---firewall config---

if [ "$FIREWALL_TOOL" == "ufw" ]; then
    echo "configuring ufw"
    if ! sudo ufw status | grep -q "Status: active"; then
        sudo ufw enable --force &> /dev/null
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
    sudo firewall-cmd --reload || { echo "Error: failed to reload firewalld rules" >&2; exit 1; }

else
    echo "Unrecognised firewall tool, firewall not configured" >&2
    exit 1

fi

echo "firewall config compleated"

# ---k3s installation---

K3S_BINARY_FOUND=false
K3S_SERVICE_ACTIVE=false


if command -v k3s &> /dev/null; then
    K3S_BINARY_FOUND=true
    if systemctl is-active --quiet k3s; then
        K3S_SERVICE_ACTIVE=true
    fi
fi

if "$K3S_BINARY_FOUND" && "$K3S_SERVICE_ACTIVE"; then
    echo "k3s binary found and service is active. Skipping installation."

elif "$K3S_BINARY_FOUND" && ! "$K3S_SERVICE_ACTIVE"; then
    echo "k3s binary found but service is not running"
    echo "attempting to start service"
    sudo systemctl start k3s || { echo "Error: failed to start k3s" >&2; exit 1; }
    echo "service started installation skipped"

else
    echo "k3s not found starting installation"
    sudo curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    echo "k3s install command executed"
fi

echo "Setting kubeconfig permissions"
sudo chmod 644 /etc/rancher/k3s/k3s.yaml || { echo "Error: failed to set permissions" >&2; exit 1; }
echo "Kubeconfig permissions set"

echo "k3s installation script finished"
