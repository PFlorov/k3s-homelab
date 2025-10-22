Getting My DevOps Blog Up and Running on K3s

This is how I managed to get my Hugo blog (from my devops-blog repo) hooked into my k3s-homelab cluster with a full CI/CD pipeline.

1. Setting Up Kubernetes for the Blog

First, I needed to get the cluster ready. I carved out a spot for the blog using standard Kubernetes resources. You'll find these YAMLs in clusters/homelab/apps/blog/ in my k3s-homelab repo.

blog-deployment.yaml: This deployment manages the Nginx pod serving my blog's static content. I configured it with proper resource limits since I'm running on old laptop hardware. The deployment pulls the Docker image from GitHub Container Registry (GHCR).

blog-service.yaml: Creates a ClusterIP service called hugo-blog-service. This gives my blog a stable internal IP and DNS name so Traefik can route traffic to it. Everything's linked using the app: blog label selector.

2. Getting It Online: Ingress, TLS & Cloudflare Tunnels

Next, I made the blog accessible from outside using https://blog.k3s-homelab.org. My setup uses Traefik (K3s's default ingress controller), cert-manager for TLS automation, and Cloudflare Tunnels for external access.

blog-ingress.yaml tells Traefik how to route external traffic to my hugo-blog-service. It also configures cert-manager to automatically get a TLS certificate from Let's Encrypt.

The cert-manager Challenge Problem

I hit a major issue here. I kept getting 404s and cert-manager couldn't validate the HTTP-01 challenge. The problem was my Cloudflare Tunnel configuration - the general rule for blog.k3s-homelab.org was intercepting everything, including the special /.well-known/acme-challenge/ path that cert-manager needs.

The Fix: I added a specific rule to my cloudflared ConfigMap, placing it before the general blog rule:


	- hostname: blog.k3s-homelab.org
	  path: /.well-known/acme-challenge/*
	  service: http://traefik.kube-system.svc.cluster.local:80

This directs ACME challenge requests directly to Traefik's HTTP port, bypassing any HTTPS redirects and letting cert-manager validate successfully.

Result: Certificates now get issued automatically, and https://blog.k3s-homelab.org loads with valid TLS.

3. Building the Docker Image Pipeline

I needed to turn my Hugo blog into a deployable Docker image. This involved setting up the devops-blog repository with proper containerization.

Multi-Stage Dockerfile

Builder stage: Uses hugomods/hugo:latest to compile my blog content into static files with hugo --buildDrafts --buildFuture --cleanDestinationDir. All generated files end up in /app/public.

Production stage: Starts fresh with nginx:alpine, copies the static files from the builder stage into Nginx's web directory (/usr/share/nginx/html). This keeps the final image small and secure.

Custom Nginx Configuration

The default Nginx config doesn't handle Hugo's clean URLs properly. I created a custom nginx.conf that:

- Handles clean URLs (like /posts/my-post/ instead of /my-post.html)

- Sets proper caching headers

- Configures security headers

- Handles 404s correctly

4. Full CI/CD Pipeline with GitHub Actions

The complete automation flow works like this:

	GitHub (blog repo) → GitHub Actions → GHCR → FluxCD → K3s → Live Site

GitHub Actions Workflow

When I push to the main branch of my devops-blog repo:

1. Build Phase: GitHub Actions builds the Docker image using my multi-stage Dockerfile

2. Push Phase: Image gets pushed to GitHub Container Registry (GHCR) with both latest and commit SHA tags

3. GitOps Update: The workflow checks out my k3s-homelab repo and uses yq to update the image tag in blog-deployment.yaml

4. Commit Back: Changes get committed and pushed back to k3s-homelab repo

FluxCD Takes Over

FluxCD monitors my k3s-homelab repository and:

- Detects the updated blog-deployment.yaml

- Pulls the new Docker image from GHCR

- Updates the running blog pods

- Ensures the new content goes live

5. Key Challenges Solved

Theme Issues

Initially ran into problems where only one blog post was showing up. The root cause was:

- Git submodules weren't being pulled in CI/CD (empty theme directory)

- Old Hugo version incompatible with modern Ananke theme

- Missing --buildFuture flag for future-dated posts

Solution: Updated GitHub Actions to use submodules: recursive checkout and switched to hugomods/hugo:latest for better theme compatibility.

Current Status

The entire pipeline is now fully operational:


- ✅ Write blog post in Markdown

- ✅ Commit and push to GitHub

- ✅ Automatic Docker image build and push

- ✅ GitOps deployment via FluxCD

- ✅ Live site updated with TLS certificate

From git push to live deployment takes about 3-5 minutes. The blog is accessible at https://blog.k3s-homelab.org with automatic HTTPS and responsive design.
