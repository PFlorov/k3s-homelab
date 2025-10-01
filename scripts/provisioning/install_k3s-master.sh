#!/bin/bash
set -e # Exit if some of the commands fail

installCheck=$(which k3s) >> /dev/null

if [ "$installCheck" == "/usr/local/bin/k3s" ]; then
  echo "k3s already isntalled, exiting script"
  exit 0
fi

echo "The installation will begin now..."
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
echo "k3s installation executed"

echo "Setting kubeconfig permissions"
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
echo "Kubeconfig permissions set"


echo "setting firewall permissions for interacting with the cluster"
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16
sudo firewall-cmd --permanent --zone=trusted --add-source=10.43.0.0/16
sudo firewall-cmd --reload
echo "firewall configured"

echo "k3s installation script finished"
