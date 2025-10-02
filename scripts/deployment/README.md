To run the deployment script, apply these commands

** Prereq **
* Ensure python 3.x is installed 
* venv module for python must be avalible
* if not install it with your systems package manager 
    sudo apt install python3.12-venv

*** Steps to run the script ***

1 ** Navigate to scrip dir **
  cd /path/to/k3s-homelab/scripts/deployment

2 ** Create venv **
  python3 -m venv venv

3 ** Activate the venv **
  source venv/bin/activate

4 ** Install the required python packages **
  pip install -r requirements.txt

5 ** Run the deploy script **
  ./deploy_k8s_resources.py

6 ** (Not manditory) Deactivate the venv when done **
  deactivate
