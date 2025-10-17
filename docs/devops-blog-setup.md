Getting My DevOps Blog Up and Running on K3s

This is how I managed to get my Hugo blog (from my devops-blog repo) hooked into my k3s-homelab cluster.

1. Setting Up Kubernetes for the Blog (in k3s-homelab)

First off, I needed to get the cluster ready. I basically carved out a spot for the blog using standard Kubernetes stuff. You'll find these YAMLs in kubernetes/blog/ in my k3s-homelab repo.

- blog-deployment.yaml: This deployment manages a single Nginx pod, which is where my blog's static content will live. Started with nginx:latest as a placeholder, just to make sure things fired up. I also tossed in some CPU/memory limits, which is pretty essential on old laptop hardware.

- blog-service.yaml: This creates a ClusterIP service, hugo-blog-service. It gives my blog a stable internal IP and name so other services like Traefik can find it. It's all linked up using the app: blog label.

2. Getting It Online: Ingress, Cert-Manager, & Cloudflare Tunnels

Next, I managed to get the blog accessible from outside, using https://blog.k3s-homelab.org. My setup relies on Traefik (K3s's default Ingress controller), cert-manager for TLS, and my trusty Cloudflare Tunnels.

My blog-ingress.yaml tells Traefik how to route external traffic to my hugo-blog-service. It also configures cert-manager to snag a TLS cert (blog-tls-secret) from Let's Encrypt.

However, this is where I hit my first 'big oof' moment. I kept getting 404s and cert-manager couldn't validate the HTTP-01 challenge. The issue was my main Cloudflare rule for blog.k3s-homelab.org was intercepting everything, including the special /.well-known/acme-challenge/ path needed by cert-manager. Plus, the HTTP-to-HTTPS redirect logic in Traefik was likely interfering with the plain HTTP challenge.

The Fix: I learned to add a super specific rule to my cloudflared ConfigMap, placing it before the general blog rule. This new rule directs blog.k3s-homelab.org/.well-known/acme-challenge/* traffic directly to Traefik's HTTP (port 80) entrypoint. You can see it like this: http://traefik.kube-system.svc.cluster.local:80. This bypasses any HTTPS redirects and lets cert-manager do its thing.

Result: Now, certificates get issued correctly, and https://blog.k3s-homelab.org loads.

3. Turning My Blog into a Docker Image (in devops-blog)

Once Kubernetes was ready, I focused on making my Hugo blog into something deployable. This meant getting the devops-blog repo sorted with Docker.

I built a multi-stage Dockerfile. The builder stage uses hugomods/hugo:latest to compile my blog content into static HTML, CSS, and JS files, which all end up in /app/public. The final stage starts fresh with nginx:alpine, then just copies those generated static files from the builder stage (/app/public) right into Nginx's web directory (/usr/share/nginx/html). This keeps the final image tiny.

This was important. The default Nginx config isn't great for Hugo's clean URLs or for things like caching. So, I added a custom nginx.conf to handle all that correctly, which the Dockerfile then copied in.

After a bit of tweaking (and some docker build/docker run commands), I got the image working perfectly, serving my actual blog locally on http://localhost:8080.

What's Next: Getting to Full CI/CD

Setting up GitHub Actions. The idea is to automate the whole process which is pushing a new post, GitHub Actions building the image, pushing it to a registry, and then it updates my Kubernetes deployment in the homelab.
