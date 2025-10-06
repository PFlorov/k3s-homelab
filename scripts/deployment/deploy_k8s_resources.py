#!/usr/bin/env python3

from kubernetes import client, config
import os
import sys
import yaml

all_manifests_content = []

KUBECONFIG_FILEPATH = "/etc/rancher/k3s/k3s.yaml"
config.load_kube_config(config_file=KUBECONFIG_FILEPATH)

api = client.CoreV1Api()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_MANIFESTS_PATH = os.path.join(SCRIPT_DIR, '../..', 'kubernetes')
MAIN_MANIFESTS_FOLDER = os.path.normpath(RAW_MANIFESTS_PATH)

for rootdir, dirs, files in os.walk(MAIN_MANIFESTS_FOLDER):
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] == ".yaml":
            full_path_of_file = os.path.join(rootdir, file)
            with open(full_path_of_file, "r") as f:
                content = f.read()
                all_manifests_content.append(content)
                # print(all_manifests_content)

all_parsed_manifests = []

for raw_yaml_string in all_manifests_content:
    for doc in yaml.safe_load_all(raw_yaml_string):
        if doc:
            kind = doc.get('kind')
            api_version = doc.get('apiVersion')
            metadata = doc.get('metadata', {})
            name = metadata.get('name')
            namespace = doc.get('namespace', 'default')

            if kind and api_version and name:
                all_parsed_manifests.append({
                    'kind': kind,
                    'apiVersion': api_version,
                    'name': name,
                    'namespace': namespace,
                    'full_manifest': doc
                })
print(f"Successfully parsed {len(all_parsed_manifests)} Kubernetes resources.")
