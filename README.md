🚀 Plamen's K3s Home Lab Journey 🚀

Welcome!

This repository documents my ongoing journey in building, optimizing, and experimenting with a home lab server. As an aspiring DevOps professional, this lab serves as my personal playground for learning Kubernetes (K3s), Docker, Linux server administration, networking, automation, and various cloud-native technologies in a hands-on environment.

🎯 My Goals

- Learn Kubernetes: Gain deep practical experience with container orchestration.

- Build Automation Skills: Practice Infrastructure as Code (IaC) and scripting.

- Master Linux Server Administration: Enhance my command-line proficiency and system management.

- Explore Cloud-Native Tools: Experiment with monitoring, logging, CI/CD, and more.

- Document Everything: Create a valuable resource for myself and others who might embark on a similar journey.


---

💻 The Hardware


My home lab is built on repurposed old laptops, optimized for 24/7 operation.

Master/Worker Node 1

- Model: Toshiba Satellite P50-A-11L

- CPU: Intel Core i7-4700MQ (4 cores, 8 threads)

- RAM: 16GB DDR3L-1600MHz SO-DIMM

- Storage: 500GB Samsung 870 EVO SATA SSD

- Network: Wired Gigabit Ethernet (static IP)

Worker Node 2

- Model: Acer Aspire 5738Z

- CPU: Intel Pentium T4300 (2 cores, 2 threads)

- RAM: 4GB DDR2-800MHz SO-DIMM / Plan for Upgrade [Depending on cost]

- Storage: 1TB HDD / Plan for Upgrade to SSD

- Network: Wired Gigabit Ethernet (static IP)


---

🌐 Networking & Access


Ensuring reliable and secure access to my server is crucial.


- OS: Ubuntu Server 24.04.3 LTS

- Local IP: Static Wired Ethernet

- External Access: Tailscale (Zero-Config VPN)

- Public Services: Cloudflare Tunnels for external web access
	- Previously attempted and troubleshooted traditional Port Forwarding + Dynamic DNS (ddclient/No-IP), which proved complex due to router/ISP limitations. Tailscale provided a seamless and more secure solution.



---

📦 Kubernetes Cluster (K3s)


I'm running a lightweight Kubernetes distribution for container orchestration.


- Distribution: K3s (v1.33.3+k3s1) - Chosen for its minimal resource footprint and ease of management on bare-metal.

- Nodes: 2 (initial master/worker node - the Toshiba laptop, and a new worker node - the Acer laptop)

- GitOps: FluxCD for automated application deployment and cluster state management

- Future Plans: Add more physical worker nodes (e.g., thin clients like HP T520/T620) to expand the cluster further.


---

🔒 Security & Infrastructure

- TLS Management: cert-manager with Let's Encrypt for automated SSL certificates

- Secrets Management: Sealed Secrets for encrypting sensitive data in Git repositories

- Ingress: Traefik (built-in with K3s) with automatic HTTPS

- Firewall: UFW configured on all nodes

- Network Security: Tailscale mesh VPN for secure cluster access


---

🛠️ Key Technologies & Tools I'm Using/Learning

- Operating System: Ubuntu Server 24.04 LTS

- Containerization: Docker, containerd

- Orchestration: Kubernetes (K3s)

- GitOps: FluxCD for continuous deployment

- Security: cert-manager, Sealed Secrets

- Networking: netplan, nmcli, ip, ufw, Tailscale, Cloudflare Tunnels

- Monitoring: htop, sensors, landscape-sysinfo, Prometheus, Grafana

- Configuration Management: (Future: Ansible)

- Version Control: Git, GitHub

- YAML: For Kubernetes manifests

- Shell Scripting: Bash, Python


---

🚀 Current Applications & Services

- Personal Blog: Hugo static site with full CI/CD pipeline (GitHub Actions → GHCR → FluxCD → K3s)

- Monitoring Stack: Prometheus(self-hosted) + Grafana(self-hosted) for cluster and application metrics

- Dashboard: Glance for quick service overview and status monitoring

- Future Deployments: Planning database workloads, log aggregation, and additional web services


---

📂 Repository Contents

- clusters/homelab/: FluxCD cluster configuration and application definitions

- docs/: Detailed guides and documentation for setup, configurations, and troubleshooting.

- scripts/: Useful shell scripts for server maintenance and automation.


---

🎯 What's Working

- ✅ K3s Cluster: Two-node cluster running stable workloads

- ✅ GitOps Pipeline: Automated deployments with FluxCD

- ✅ TLS Automation: cert-manager handling SSL certificates

- ✅ Secure Secrets: Sealed Secrets encrypting sensitive data

- ✅ Blog CI/CD: Full pipeline from git push to live deployment

- ✅ Monitoring: Comprehensive metrics collection and visualization

- ✅ External Access: Secure remote connectivity via Tailscale

🔄 Currently Working On

- Infrastructure as Code: Ansible playbooks for cluster automation

- Log Aggregation: Implementing Loki + Promtail for centralized logging

- Persistent Storage: Setting up Longhorn for distributed storage

- Multi-Environment: Staging and production namespace separation

📋 Future Plans

- Service Mesh: Exploring Istio or Linkerd for advanced traffic management

- Backup Strategy: Implementing automated cluster and data backups

- Additional Nodes: Expanding cluster with dedicated thin client hardware

- Advanced Monitoring: Adding distributed tracing and alerting rules


---

🤝 Contributing & Support


This is a personal learning project, but feel free to open an issue if you have questions, suggestions, or spot any errors.


---

📝 License


This project is open-source under the MIT License.

---
