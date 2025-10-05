#!/usr/bin/env python3

from kubernetes import client, config
import os
import sys

KUBECONFIG_FILEPATH = "/etc/rancher/k3s/k3s.yaml"
config.load_kube_config(config_file=KUBECONFIG_FILEPATH)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


RAW_MANIFESTS_PATH = os.path.join(SCRIPT_DIR, '../..', 'kubernetes')
MAIN_MANIFESTS_FOLDER = os.path.normpath(RAW_MANIFESTS_PATH)

all_manifests_content = []
for rootdir, dirs, files in os.walk(MAIN_MANIFESTS_FOLDER):
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] == ".yaml":
            full_path_of_file = os.path.join(rootdir, file)
            with open(full_path_of_file, "r") as f:
                content = f.read()
                all_manifests_content.append(content)
                print(all_manifests_content)
