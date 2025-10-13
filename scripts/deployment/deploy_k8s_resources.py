#!/usr/bin/env python3

from kubernetes import client, config
import os
import sys
import yaml


def load_kubeconfig(kubeconfig_path):
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        print(f"Successfully loaded config file")
    except FileNotFoundError:
        print(
            f"Error: Kubeconfig file not found at {kubeconfig_path}", file=sys.stderr)
        sys.exit(1)
    except config.config_exception.ConfigException as e:
        print(
            f"Error loading kubeconfig from {kubeconfig_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred while loading kubeconfig: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":

    KUBECONFIG_FILEPATH = "/etc/rancher/k3s/k3s.yaml"
    load_kubeconfig(KUBECONFIG_FILEPATH)

    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    networking_v1 = client.NetworkingV1Api()
    custom_api = client.CustomObjectsApi()

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_MANIFESTS_PATH = os.path.join(SCRIPT_DIR, '../..', 'kubernetes')
    MAIN_MANIFESTS_FOLDER = os.path.normpath(RAW_MANIFESTS_PATH)

    all_manifests_content = []
    for rootdir, dirs, files in os.walk(MAIN_MANIFESTS_FOLDER):
        for file_name in files:
            extension = os.path.splitext(file_name)[1].lower()
            if extension in (".yaml", ".yml"):
                full_path_of_file = os.path.join(rootdir, file_name)
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
    print(
        f"Successfully parsed {len(all_parsed_manifests)} Kubernetes resources.")

    order_of_manifests = ['Namespace', 'ConfigMap', 'Secret', 'SealedSecret', 'PersistentVolume',
                          'PersistentVolumeClaim', 'ServiceAccount', 'ClusterRole', 'ClusterRoleBinding',
                          'Deployment', 'DaemonSet', 'Service', 'Ingress', 'ClusterIssuer', ]

    grouped_manifests = {kind: [] for kind in order_of_manifests}

    for manifest_info in all_parsed_manifests:
        kind = manifest_info['kind']
        if kind in grouped_manifests:
            grouped_manifests[kind].append(manifest_info['full_manifest'])
        else:
            print(
                f"resource of kind '{kind}' found but not in defined order_of_manifests. Skipping", file=sys.stderr)

    print("\n--- Applying kubernetes resources ---")

    for kind in order_of_manifests:
        print(f"Applying {kind} resources..")
        if not grouped_manifests.get(kind):
            continue

        for manifest in grouped_manifests[kind]:
            name = manifest['metadata']['name']
            namespace = manifest['metadata'].get('namespace')

            is_namespaced = namespace and kind not in [
                'Namespace', 'PersistentVolume', 'ClusterRole', 'ClusterRoleBinding', 'ClusterIssuer']

            if is_namespaced:
                if kind == 'ConfigMap':
                    try:
                        v1.read_namespaced_config_map(
                            name=name, namespace=namespace)
                        v1.patch_namespaced_config_map(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched ConfigMap/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespaced_config_map(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created ConfigMap/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'Secret':
                    try:
                        v1.read_namespaced_secret(
                            name=name, namespace=namespace)
                        v1.patch_namespaced_secret(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched Secret/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespaced_secret(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created Secret/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'Service':
                    try:
                        v1.read_namespaced_service(
                            name=name, namespace=namespace)
                        v1.patch_namespaced_service(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched Service/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespaced_service(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created Service/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'Deployment':
                    try:
                        apps_v1.read_namespaced_deployment(
                            name=name, namespace=namespace)
                        apps_v1.patch_namespaced_deployment(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched Deployment/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            apps_v1.create_namespaced_deployment(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created Deployment/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'Ingress':
                    try:
                        networking_v1.read_namespaced_ingress(
                            name=name, namespace=namespace)
                        networking_v1.patch_namespaced_ingress(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched Ingress/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            networking_v1.create_namespaced_ingress(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created Ingress/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'SealedSecret':
                    group = manifest['apiVersion'].split('/')[0]
                    version = manifest['apiVersion'].split('/')[-1]
                    plural = 'sealedsecrets'  # Hardcode plural for SealedSecret - could be more dynamic

                    try:
                        custom_api.get_namespaced_custom_object(
                            group=group, version=version, name=name, plural=plural, namespace=namespace)
                        custom_api.patch_namespaced_custom_object(
                            group=group, version=version, name=name, plural=plural, namespace=namespace, body=manifest)
                        print(
                            f"  Patched SealedSecret/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            custom_api.create_namespaced_custom_object(
                                group=group, version=version, namespace=namespace, plural=plural, body=manifest)
                            print(
                                f"  Created SealedSecret/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'PersistentVolumeClaim':
                    try:
                        v1.read_namespaced_persistent_volume_claim(
                            name=name, namespace=namespace)
                        v1.patch_namespaced_persistent_volume_claim(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched PersistentVolumeClaim/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespaced_persistent_volume_claim(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created PersistentVolumeClaim/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'ServiceAccount':
                    try:
                        v1.read_namespaced_service_account(
                            name=name, namespace=namespace)
                        v1.patch_namespaced_service_account(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched ServiceAccount/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespaced_service_account(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created ServiceAccount/{name} in namespace {namespace}")
                        else:
                            raise
                elif kind == 'DaemonSet':
                    try:
                        apps_v1.read_namespaced_daemon_set(
                            name=name, namespace=namespace)
                        apps_v1.patch_namespaced_daemon_set(
                            name=name, namespace=namespace, body=manifest)
                        print(
                            f"  Patched DaemonSet/{name} in namespace {namespace}")
                    except client.ApiException as e:
                        if e.status == 404:
                            apps_v1.create_namespaced_daemon_set(
                                namespace=namespace, body=manifest)
                            print(
                                f"  Created DaemonSet/{name} in namespace {namespace}")
                        else:
                            raise
                else:
                    print(
                        f"Warning: No specific apply logic implemented for namespaced kind: {kind}/{name}. Skipping.", file=sys.stderr)

            else:
                if kind == 'Namespace':
                    try:
                        v1.read_namespace(name=name)
                        print(
                            f"  Namespace/{name} already exists. Skipping (patch usually not needed).")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_namespace(body=manifest)
                            print(f"  Created Namespace/{name}")
                        else:
                            raise
                elif kind == 'PersistentVolume':
                    try:
                        v1.read_persistent_volume(name=name)
                        v1.patch_persistent_volume(name=name, body=manifest)
                        print(f"  Patched PersistentVolume/{name}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_persistent_volume(body=manifest)
                            print(f"  Created PersistentVolume/{name}")
                        else:
                            raise
                elif kind == 'ClusterRole':
                    try:
                        v1.read_cluster_role(name=name)
                        v1.patch_cluster_role(name=name, body=manifest)
                        print(f"  Patched ClusterRole/{name}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_cluster_role(body=manifest)
                            print(f"  Created ClusterRole/{name}")
                        else:
                            raise
                elif kind == 'ClusterRoleBinding':
                    try:
                        v1.read_cluster_role_binding(name=name)
                        v1.patch_cluster_role_binding(name=name, body=manifest)
                        print(f"  Patched ClusterRoleBinding/{name}")
                    except client.ApiException as e:
                        if e.status == 404:
                            v1.create_cluster_role_binding(body=manifest)
                            print(f"  Created ClusterRoleBinding/{name}")
                        else:
                            raise
                elif kind == 'ClusterIssuer':
                    group = manifest['apiVersion'].split('/')[0]
                    version = manifest['apiVersion'].split('/')[-1]
                    plural = 'clusterissuers'  # Hardcode plural for ClusterIssuer

                    try:

                        custom_api.get_cluster_custom_object(
                            group=group, version=version, name=name, plural=plural)
                        custom_api.patch_cluster_custom_object(
                            group=group, version=version, name=name, plural=plural, body=manifest)
                        print(f"  Patched ClusterIssuer/{name}")
                    except client.ApiException as e:
                        if e.status == 404:
                            custom_api.create_cluster_custom_object(
                                group=group, version=version, plural=plural, body=manifest)
                            print(f"  Created ClusterIssuer/{name}")
                        else:
                            raise
                else:
                    print(
                        f"Warning: No specific apply logic implemented for cluster-scoped kind: {kind}/{name}. Skipping.", file=sys.stderr)
