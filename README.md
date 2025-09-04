# 🚀 Plamen's K3s Home Lab Journey 🚀

## Welcome!

This repository documents my ongoing journey in building, optimizing, and experimenting with a home lab server. As an aspiring DevOps professional, this lab serves as my personal playground for learning Kubernetes (K3s), Docker, Linux server administration, networking, automation, and various cloud-native technologies in a hands-on environment.

## 🎯 My Goals

*   **Learn Kubernetes:** Gain deep practical experience with container orchestration.
*   **Build Automation Skills:** Practice Infrastructure as Code (IaC) and scripting.
*   **Master Linux Server Administration:** Enhance my command-line proficiency and system management.
*   **Explore Cloud-Native Tools:** Experiment with monitoring, logging, CI/CD, and more.
*   **Document Everything:** Create a valuable resource for myself and others who might embark on a similar journey.

---

## 💻 The Hardware

My home lab is built on repurposed old laptops, optimized for 24/7 operation.

### Master/Worker Node 1

*   **Model:** Toshiba Satellite P50-A-11L
*   **CPU:** Intel Core i7-4700MQ (4 cores, 8 threads)
*   **RAM:** 16GB DDR3L-1600MHz SO-DIMM
*   **Storage:** 500GB Samsung 870 EVO SATA SSD
*   **Network:** Wired Gigabit Ethernet (static IP)

### Worker Node 2

*   **Model:** Acer Aspire 5738Z
*   **CPU:** Intel Pentium T4300 (2 cores, 2 threads)
*   **RAM:** 4GB DDR2-800MHz SO-DIMM / Plan for Upgrade [Depending on cost]
*   **Storage:** 1TB HDD / Plan for Upgrade to SSD
*   **Network:** Wired Gigabit Ethernet (static IP)

---

## 🌐 Networking & Access

Ensuring reliable and secure access to my server is crucial.

*   **OS:** Ubuntu Server 24.04.3 LTS
*   **Local IP:** Static Wired Ethernet
*   **External Access:** [Tailscale](https://tailscale.com/) (Zero-Config VPN)
    *   *Previously attempted and troubleshooted traditional Port Forwarding + Dynamic DNS (ddclient/No-IP), which proved complex due to router/ISP limitations. Tailscale provided a seamless and more secure solution.*

---

## 📦 Kubernetes Cluster (K3s)

I'm running a lightweight Kubernetes distribution for container orchestration.

*   **Distribution:** [K3s](https://k3s.io/) (v1.33.3+k3s1) - Chosen for its minimal resource footprint and ease of management on bare-metal.
*   **Nodes:** 2 (initial master/worker node - the Toshiba laptop, and a new worker node - the Acer laptop)
*   **Future Plans:** Add more physical worker nodes (e.g., thin clients like HP T520/T620) to expand the cluster further.
---

## 🛠️ Key Technologies & Tools I'm Using/Learning

*   **Operating System:** Ubuntu Server 24.04 LTS
*   **Containerization:** Docker, containerd
*   **Orchestration:** Kubernetes (K3s)
*   **Networking:** `netplan`, `nmcli`, `ip`, `ufw`, `Tailscale`
*   **Monitoring:** `htop`, `sensors`, `landscape-sysinfo`, `Prometheus`, `Grafana`
*   **Configuration Management:** (Future: Ansible)
*   **Version Control:** Git, GitHub
*   **YAML:** For Kubernetes manifests
*   **Shell Scripting:** Bash

---

## 📂 Repository Contents

*   [`docs/`](./docs): Detailed guides and documentation for setup, configurations, and troubleshooting.
*   [`kubernetes/`](./kubernetes): All Kubernetes YAML manifests for deployments, services, ingress, and more.
*   [`scripts/`](./scripts): Useful shell scripts for server maintenance and automation.

---

## 🤝 Contributing & Support

This is a personal learning project, but feel free to open an issue if you have questions, suggestions, or spot any errors.

---

## 📝 License

This project is open-source under the [MIT License](LICENSE).
