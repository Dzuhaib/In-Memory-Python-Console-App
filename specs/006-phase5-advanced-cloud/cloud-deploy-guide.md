# Cloud Deployment Guide: Todo App with Dapr and Redpanda Cloud

**Version**: 1.0.0
**Last Updated**: 2026-02-12
**Prerequisites**: kubectl, Helm 3.x, Dapr CLI, Docker, cloud provider CLI (az/gcloud/oci)

---

## Overview

This guide walks through deploying the Todo App stack to a production cloud Kubernetes cluster with:
- **Cloud Kubernetes**: OKE (Oracle), AKS (Azure), or GKE (Google Cloud)
- **Dapr Runtime**: Distributed application runtime for microservices
- **Redpanda Cloud**: Managed Kafka (free serverless tier available)
- **TLS/HTTPS**: Automated certificate management with cert-manager and Let's Encrypt
- **Container Registry**: GitHub Container Registry (GHCR)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Provision Cloud Kubernetes Cluster](#step-1-provision-cloud-kubernetes-cluster)
3. [Step 2: Configure kubectl Context](#step-2-configure-kubectl-context)
4. [Step 3: Install Dapr on Cloud Cluster](#step-3-install-dapr-on-cloud-cluster)
5. [Step 4: Set Up Redpanda Cloud Kafka](#step-4-set-up-redpanda-cloud-kafka)
6. [Step 5: Update Dapr Kafka Component](#step-5-update-dapr-kafka-component)
7. [Step 6: Install cert-manager](#step-6-install-cert-manager)
8. [Step 7: Install nginx-ingress Controller](#step-7-install-nginx-ingress-controller)
9. [Step 8: Build and Push Docker Images](#step-8-build-and-push-docker-images)
10. [Step 9: Create Kubernetes Secrets](#step-9-create-kubernetes-secrets)
11. [Step 10: Deploy with Helm](#step-10-deploy-with-helm)
12. [Step 11: Verify Deployment](#step-11-verify-deployment)
13. [Step 12: Verify HTTPS Access](#step-12-verify-https-access)
14. [Troubleshooting](#troubleshooting)
15. [Cleanup](#cleanup)

---

## Prerequisites

### Required Tools

```bash
# Verify tool installations
kubectl version --client
helm version
dapr version
docker --version

# Cloud provider CLI (choose one):
az --version        # Azure
gcloud --version    # GCP
oci --version       # Oracle Cloud
```

### Required Accounts

- Cloud provider account (OKE/AKS/GKE)
- GitHub account (for GHCR container registry)
- Redpanda Cloud account (free tier: https://redpanda.com/try-redpanda)
- Domain name or subdomain for TLS (optional: use nip.io for testing)

### Environment Variables

```bash
export GITHUB_USERNAME="dzuhaib"  # Your GitHub username
export REGISTRY="ghcr.io/${GITHUB_USERNAME}"
export DOMAIN="todo.example.com"  # Replace with your domain
export EMAIL="admin@example.com"  # For Let's Encrypt notifications
```

---

## Step 1: Provision Cloud Kubernetes Cluster

Choose your cloud provider and provision a Kubernetes cluster.

### Option A: Oracle Cloud (OKE)

```bash
# Authenticate
oci session authenticate

# Set variables
export COMPARTMENT_ID="ocid1.compartment.oc1..xxxxxx"
export CLUSTER_NAME="todo-app-cluster"
export REGION="us-phoenix-1"

# Create VCN and subnets (simplified - use OCI Console for production)
# Note: Full networking setup requires multiple steps; consider using OCI Console

# Create OKE cluster (requires pre-configured VCN)
oci ce cluster create \
  --compartment-id $COMPARTMENT_ID \
  --name $CLUSTER_NAME \
  --vcn-id $VCN_ID \
  --kubernetes-version v1.28.2 \
  --service-lb-subnet-ids "[\"$SUBNET_ID\"]" \
  --wait-for-state ACTIVE

# Create node pool
oci ce node-pool create \
  --cluster-id $CLUSTER_ID \
  --name default-pool \
  --compartment-id $COMPARTMENT_ID \
  --node-shape VM.Standard.E4.Flex \
  --node-shape-config '{"ocpus":2,"memoryInGBs":16}' \
  --size 2 \
  --wait-for-state ACTIVE

# Get cluster ID
export CLUSTER_ID=$(oci ce cluster list \
  --compartment-id $COMPARTMENT_ID \
  --name $CLUSTER_NAME \
  --query 'data[0].id' --raw-output)
```

### Option B: Azure (AKS)

```bash
# Authenticate
az login

# Set variables
export RESOURCE_GROUP="todo-app-rg"
export CLUSTER_NAME="todo-app-cluster"
export LOCATION="eastus"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create AKS cluster (2 nodes, Standard_DS2_v2)
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count 2 \
  --node-vm-size Standard_DS2_v2 \
  --generate-ssh-keys \
  --enable-managed-identity \
  --network-plugin azure \
  --network-policy azure

# Wait for cluster to be running
az aks wait \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --created
```

### Option C: Google Cloud (GKE)

```bash
# Authenticate
gcloud auth login

# Set variables
export PROJECT_ID="your-gcp-project-id"
export CLUSTER_NAME="todo-app-cluster"
export ZONE="us-central1-a"

# Set default project
gcloud config set project $PROJECT_ID

# Create GKE cluster (2 nodes, e2-standard-2)
gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --num-nodes 2 \
  --machine-type e2-standard-2 \
  --disk-size 50 \
  --enable-autorepair \
  --enable-autoupgrade \
  --enable-ip-alias

# Wait for cluster to be running (automatic)
```

**Success Criteria**: Cluster reports as `Running`/`READY` with at least 2 nodes.

---

## Step 2: Configure kubectl Context

Retrieve cluster credentials and configure kubectl to connect to the cloud cluster.

### Oracle Cloud (OKE)

```bash
# Generate kubeconfig
oci ce cluster create-kubeconfig \
  --cluster-id $CLUSTER_ID \
  --file ~/.kube/oke-config \
  --region $REGION \
  --token-version 2.0.0

# Merge with existing kubeconfig
export KUBECONFIG=~/.kube/config:~/.kube/oke-config
kubectl config view --merge --flatten > ~/.kube/merged-config
mv ~/.kube/merged-config ~/.kube/config

# Set context
kubectl config use-context context-<cluster-ocid>
```

### Azure (AKS)

```bash
# Get credentials
az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --overwrite-existing

# Verify context
kubectl config current-context
```

### Google Cloud (GKE)

```bash
# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME \
  --zone $ZONE

# Verify context
kubectl config current-context
```

### Verify Cluster Access

```bash
# Verify connection
kubectl get nodes

# Expected output: 2 nodes in Ready state
# NAME                            STATUS   ROLES    AGE   VERSION
# node-1                          Ready    <none>   5m    v1.28.x
# node-2                          Ready    <none>   5m    v1.28.x

# Verify cluster info
kubectl cluster-info
```

**Success Criteria**: `kubectl get nodes` returns cloud cluster nodes (not Minikube), all nodes are `Ready`.

---

## Step 3: Install Dapr on Cloud Cluster

Initialize Dapr control plane on the Kubernetes cluster.

```bash
# Install Dapr runtime (control plane components)
dapr init --kubernetes --wait

# Verify Dapr installation
dapr status -k

# Expected output:
#   NAME                   NAMESPACE    HEALTHY  STATUS   REPLICAS  VERSION  AGE  CREATED
#   dapr-sentry            dapr-system  True     Running  1         1.13.0   30s  2026-02-12 10:00.00
#   dapr-operator          dapr-system  True     Running  1         1.13.0   30s  2026-02-12 10:00.00
#   dapr-sidecar-injector  dapr-system  True     Running  1         1.13.0   30s  2026-02-12 10:00.00
#   dapr-placement-server  dapr-system  True     Running  1         1.13.0   30s  2026-02-12 10:00.00

# Verify Dapr pods are running
kubectl get pods -n dapr-system

# All pods should be Running with 1/1 READY
```

**Success Criteria**: `dapr status -k` shows all control plane services (operator, sentry, sidecar-injector, placement) as Running and healthy.

---

## Step 4: Set Up Redpanda Cloud Kafka

Redpanda Cloud provides a managed Kafka service with a free serverless tier.

### Create Redpanda Cloud Account

1. Visit https://redpanda.com/try-redpanda
2. Sign up for a free account
3. Create a new Serverless cluster (free tier: 10 GB storage, 10 MB/s throughput)

### Create Cluster and Topics

```bash
# Via Redpanda Cloud Console:
# 1. Create a new Serverless cluster (select region closest to your K8s cluster)
# 2. Note the bootstrap server address (e.g., seed-abc123.cloud.redpanda.com:9092)
# 3. Create SASL/SCRAM user:
#    - Username: todo-app-user
#    - Password: (auto-generated, save securely)
# 4. Create topics:
#    - task-events (partitions: 3, retention: 7 days)
#    - reminders (partitions: 1, retention: 1 day)
#    - task-updates (partitions: 3, retention: 7 days)

# Save configuration
export KAFKA_BOOTSTRAP_SERVERS="seed-abc123.cloud.redpanda.com:9092"
export KAFKA_SASL_USERNAME="todo-app-user"
export KAFKA_SASL_PASSWORD="your-generated-password"
```

### Test Connectivity (Optional)

```bash
# Use kcat (formerly kafkacat) to test connectivity
docker run --rm -it edenhill/kcat:1.7.1 \
  -b $KAFKA_BOOTSTRAP_SERVERS \
  -X security.protocol=SASL_SSL \
  -X sasl.mechanisms=SCRAM-SHA-256 \
  -X sasl.username=$KAFKA_SASL_USERNAME \
  -X sasl.password=$KAFKA_SASL_PASSWORD \
  -L

# Expected output: broker and topic metadata
```

**Success Criteria**: Bootstrap server is reachable, topics are created, SASL credentials are valid.

---

## Step 5: Update Dapr Kafka Component

Update the Dapr Kafka Pub/Sub component YAML with cloud broker credentials.

```bash
# Create Kubernetes Secret for Kafka credentials
kubectl create namespace todo-app

kubectl create secret generic redpanda-kafka-credentials \
  --from-literal=sasl-username=$KAFKA_SASL_USERNAME \
  --from-literal=sasl-password=$KAFKA_SASL_PASSWORD \
  --namespace todo-app

# Verify secret
kubectl get secret redpanda-kafka-credentials -n todo-app
```

### Update `dapr-components/kafka-pubsub.yaml`

Edit the Dapr component YAML to use cloud Kafka:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    # Cloud Kafka bootstrap servers
    - name: brokers
      value: "seed-abc123.cloud.redpanda.com:9092"  # Replace with your bootstrap servers
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: redpanda-kafka-credentials
        key: sasl-username
    - name: saslPassword
      secretKeyRef:
        name: redpanda-kafka-credentials
        key: sasl-password
    - name: saslMechanism
      value: "SCRAM-SHA-256"  # Or SCRAM-SHA-512
    - name: maxMessageBytes
      value: "1024000"
    - name: consumerGroup
      value: "todo-app-consumers"
    # TLS configuration (required for cloud)
    - name: skipVerify
      value: "false"  # Set to false for production
    - name: caCert
      value: ""  # Optional: provide CA cert if needed
```

**Success Criteria**: Component YAML is valid, Secret exists in the target namespace, bootstrap server is reachable.

---

## Step 6: Install cert-manager

Install cert-manager for automated TLS certificate provisioning from Let's Encrypt.

```bash
# Add Jetstack Helm repo
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager with CRDs
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true \
  --version v1.14.2 \
  --wait

# Verify cert-manager pods
kubectl wait --for=condition=Ready pod \
  -l app.kubernetes.io/instance=cert-manager \
  -n cert-manager \
  --timeout=120s

# Expected output: 3 pods (cert-manager, webhook, cainjector) all Running
kubectl get pods -n cert-manager
```

### Create Let's Encrypt ClusterIssuer

```bash
# Create ClusterIssuer for Let's Encrypt Production
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: $EMAIL  # Replace with your email
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
      - http01:
          ingress:
            class: nginx
EOF

# Verify ClusterIssuer is Ready
kubectl get clusterissuer letsencrypt-prod

# Expected output: READY=True
# NAME               READY   AGE
# letsencrypt-prod   True    10s
```

**Optional: Create Staging Issuer for Testing**

```bash
# Use staging for testing to avoid rate limits
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: $EMAIL
    privateKeySecretRef:
      name: letsencrypt-staging-account-key
    solvers:
      - http01:
          ingress:
            class: nginx
EOF
```

**Success Criteria**: `kubectl get clusterissuer` shows the issuer in Ready state, cert-manager webhook is responding.

---

## Step 7: Install nginx-ingress Controller

Install nginx-ingress to expose services via HTTP/HTTPS with TLS termination.

```bash
# Add ingress-nginx Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install nginx-ingress controller
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --wait

# Wait for LoadBalancer external IP to be assigned (may take 2-5 minutes)
kubectl get svc -n ingress-nginx ingress-nginx-controller -w

# Expected output: EXTERNAL-IP changes from <pending> to an actual IP
# NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)
# ingress-nginx-controller   LoadBalancer   10.96.123.45    203.0.113.10     80:30080/TCP,443:30443/TCP
```

### Configure DNS

Point your domain to the LoadBalancer external IP:

```bash
# Get external IP
export EXTERNAL_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "Configure DNS A record:"
echo "$DOMAIN -> $EXTERNAL_IP"

# Example DNS records:
# A    todo.example.com    203.0.113.10
# A    *.todo.example.com  203.0.113.10  (if using subdomains)
```

**Alternative: Use nip.io for Testing (No DNS Required)**

```bash
# nip.io automatically resolves <anything>.<ip>.nip.io to <ip>
export DOMAIN="todo.${EXTERNAL_IP}.nip.io"
echo "Using domain: $DOMAIN"
```

**Success Criteria**: External IP is assigned, DNS A record is configured (or using nip.io), domain resolves to LoadBalancer IP.

---

## Step 8: Build and Push Docker Images

Build all Docker images and push them to GitHub Container Registry (GHCR).

### Authenticate with GHCR

```bash
# Create GitHub Personal Access Token (PAT):
# 1. Go to https://github.com/settings/tokens
# 2. Generate new token (classic) with scopes: write:packages, read:packages, delete:packages
# 3. Copy the token

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Expected output: Login Succeeded
```

### Build and Push Images

```bash
# Navigate to project root
cd "D:\hackathon phase 4 to 5\In-Memory-Python-Console-App"

# Build backend image
docker build -t $REGISTRY/todo-backend:latest ./backend
docker push $REGISTRY/todo-backend:latest

# Build frontend image
docker build -t $REGISTRY/todo-frontend:latest ./frontend
docker push $REGISTRY/todo-frontend:latest

# Build consumer microservices
docker build -t $REGISTRY/notification-service:latest ./services/notification-service
docker push $REGISTRY/notification-service:latest

docker build -t $REGISTRY/recurring-task-service:latest ./services/recurring-task-service
docker push $REGISTRY/recurring-task-service:latest

docker build -t $REGISTRY/audit-service:latest ./services/audit-service
docker push $REGISTRY/audit-service:latest

docker build -t $REGISTRY/websocket-service:latest ./services/websocket-service
docker push $REGISTRY/websocket-service:latest

# Verify images on GHCR
# Visit: https://github.com/<username>?tab=packages
```

**Optional: Tag with Version**

```bash
export VERSION="v1.0.0"
docker tag $REGISTRY/todo-backend:latest $REGISTRY/todo-backend:$VERSION
docker push $REGISTRY/todo-backend:$VERSION
```

**Success Criteria**: All 6 images are built and pushed to GHCR successfully.

---

## Step 9: Create Kubernetes Secrets

Create Kubernetes Secrets for sensitive configuration (database URL, API keys, Kafka credentials).

```bash
# Set secret values
export DATABASE_URL="postgresql://user:password@host:5432/tododb"  # Replace with your DB
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"           # Replace with your key

# Create backend secrets
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL=$DATABASE_URL \
  --from-literal=OPENAI_API_KEY=$OPENAI_API_KEY \
  --namespace todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Kafka credentials (already created in Step 5)
kubectl get secret redpanda-kafka-credentials -n todo-app

# Verify secrets
kubectl get secrets -n todo-app
```

**Optional: Image Pull Secret (if using private GHCR repo)**

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=$GITHUB_USERNAME \
  --docker-password=$GITHUB_TOKEN \
  --namespace todo-app
```

**Success Criteria**: All required secrets exist in the `todo-app` namespace.

---

## Step 10: Deploy with Helm

Deploy the full stack to the cloud cluster using Helm with production values.

### Update Production Values

Edit `k8s/charts/todo-app/values-production.yaml` with your configuration:

```yaml
# Replace placeholders:
# - backend.config.CORS_ORIGINS: "https://$DOMAIN"
# - frontend.config.NEXT_PUBLIC_API_URL: "https://$DOMAIN/api/v1"
# - kafka.cloud.bootstrapServers: "<your-bootstrap-servers>"
# - ingress.hosts[].host: "$DOMAIN"
# - ingress.tls[].hosts[]: "$DOMAIN"
# - certManager.email: "$EMAIL"
```

```bash
# Update values file with environment variables
sed -i "s|todo.example.com|$DOMAIN|g" k8s/charts/todo-app/values-production.yaml
sed -i "s|admin@example.com|$EMAIL|g" k8s/charts/todo-app/values-production.yaml
sed -i "s|seed-<cluster-id>.cloud.redpanda.com:9092|$KAFKA_BOOTSTRAP_SERVERS|g" k8s/charts/todo-app/values-production.yaml
```

### Deploy with Helm

```bash
# Navigate to Helm chart directory
cd k8s/charts/todo-app

# Dry-run to validate
helm upgrade --install todo-app . \
  -f values-production.yaml \
  --namespace todo-app \
  --create-namespace \
  --dry-run --debug

# Deploy (actual)
helm upgrade --install todo-app . \
  -f values-production.yaml \
  --namespace todo-app \
  --create-namespace \
  --wait \
  --timeout 10m

# Expected output: Release "todo-app" has been upgraded. Happy Helming!
```

### Verify Helm Release

```bash
# List Helm releases
helm list -n todo-app

# Expected output:
# NAME       NAMESPACE  REVISION  UPDATED                                STATUS    CHART          APP VERSION
# todo-app   todo-app   1         2026-02-12 10:30:00.000000 -0700 MST   deployed  todo-app-0.1.0 1.0.0
```

**Success Criteria**: Helm release reports `STATUS: deployed`, no errors during deployment.

---

## Step 11: Verify Deployment

Verify all pods are running and Dapr sidecars are injected.

### Check Pods

```bash
# Get all pods in todo-app namespace
kubectl get pods -n todo-app -o wide

# Expected output: All pods in Running state with 2/2 containers (app + daprd sidecar)
# NAME                                    READY   STATUS    RESTARTS   AGE
# todo-backend-xxxxxx-xxxxx               2/2     Running   0          2m
# todo-backend-xxxxxx-xxxxx               2/2     Running   0          2m
# todo-frontend-xxxxxx-xxxxx              1/1     Running   0          2m  (no sidecar if dapr.enabled=false)
# todo-frontend-xxxxxx-xxxxx              1/1     Running   0          2m
# notification-service-xxxxxx-xxxxx       2/2     Running   0          2m
# recurring-task-service-xxxxxx-xxxxx     2/2     Running   0          2m
# audit-service-xxxxxx-xxxxx              2/2     Running   0          2m
# websocket-service-xxxxxx-xxxxx          2/2     Running   0          2m

# Check for CrashLoopBackOff or Error states
kubectl get pods -n todo-app | grep -vE "Running|Completed"
```

### Verify Dapr Sidecars

```bash
# List Dapr-enabled apps
dapr list -k -n todo-app

# Expected output: All backend and consumer services with Dapr sidecars
# APP ID                      APP PORT  AGE  CREATED
# todo-backend                8000      5m   2026-02-12 10:30.00
# notification-service        8001      5m   2026-02-12 10:30.00
# recurring-task-service      8002      5m   2026-02-12 10:30.00
# audit-service               8003      5m   2026-02-12 10:30.00
# websocket-service           8004      5m   2026-02-12 10:30.00
```

### Check Services

```bash
# Get all services
kubectl get svc -n todo-app

# Expected output:
# NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
# backend-service          ClusterIP   10.96.123.45     <none>        8000/TCP
# frontend-service         ClusterIP   10.96.123.46     <none>        3000/TCP
# notification-service     ClusterIP   10.96.123.47     <none>        8001/TCP
# recurring-task-service   ClusterIP   10.96.123.48     <none>        8002/TCP
# audit-service            ClusterIP   10.96.123.49     <none>        8003/TCP
# websocket-service        ClusterIP   10.96.123.50     <none>        8004/TCP
```

### Check Ingress

```bash
# Get ingress resources
kubectl get ingress -n todo-app

# Expected output:
# NAME                  CLASS   HOSTS              ADDRESS         PORTS     AGE
# todo-app-ingress      nginx   todo.example.com   203.0.113.10    80, 443   5m
```

### Check TLS Certificate

```bash
# Get certificate status
kubectl get certificate -n todo-app

# Expected output:
# NAME            READY   SECRET          AGE
# todo-app-tls    True    todo-app-tls    5m

# Describe certificate for details
kubectl describe certificate todo-app-tls -n todo-app

# Check for "Certificate issued successfully" event
```

### Check Logs

```bash
# Check backend logs
kubectl logs -n todo-app deployment/todo-backend -c backend --tail=50

# Check Dapr sidecar logs
kubectl logs -n todo-app deployment/todo-backend -c daprd --tail=50

# Check consumer service logs
kubectl logs -n todo-app deployment/audit-service -c audit-service --tail=50
```

**Success Criteria**:
- Zero pods in CrashLoopBackOff, Error, or Pending state
- All application pods with Dapr enabled have 2/2 containers (app + daprd)
- All replicas are at count 2 for backend/frontend, 1 for consumers
- Ingress has an external IP assigned
- TLS certificate is issued (READY=True)

---

## Step 12: Verify HTTPS Access

Test end-to-end connectivity via the public HTTPS URL.

```bash
# Wait for DNS propagation (if using real domain, may take 5-60 minutes)
nslookup $DOMAIN

# Test HTTP redirect to HTTPS
curl -I http://$DOMAIN

# Expected output: 301 or 308 redirect to https://

# Test HTTPS frontend
curl -I https://$DOMAIN

# Expected output: 200 OK, valid TLS certificate

# Test HTTPS backend API
curl https://$DOMAIN/api/v1/health

# Expected output: {"status":"healthy"}

# Open in browser
echo "Open browser: https://$DOMAIN"
```

### Smoke Test: Create a Task

```bash
# Create a task via API
curl -X POST https://$DOMAIN/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cloud deployment test",
    "priority": "high",
    "due_at": "2026-02-13T12:00:00Z"
  }'

# Expected output: Task created with ID

# Verify in UI
# Open https://$DOMAIN in browser and check task appears
```

### Verify Event Flow

```bash
# Check audit-service logs for event
kubectl logs -n todo-app deployment/audit-service -c audit-service --tail=20 | grep "task.created"

# Expected output: JSON log entry with task.created event
```

**Success Criteria**:
- HTTPS URL is accessible with valid TLS certificate (green padlock in browser)
- Frontend loads without errors
- Backend API responds to health checks
- Tasks can be created via UI and API
- Events appear in audit-service logs

---

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod for events
kubectl describe pod <pod-name> -n todo-app

# Common issues:
# - ImagePullBackOff: Check image name, registry auth (imagePullSecret)
# - CrashLoopBackOff: Check logs, environment variables, secret values
# - Pending: Check node resources, PVC bindings, scheduling constraints
```

### Dapr Sidecar Not Injected

```bash
# Check Dapr annotations on deployment
kubectl get deployment <deployment-name> -n todo-app -o yaml | grep dapr.io

# Verify Dapr system pods are healthy
kubectl get pods -n dapr-system

# Check sidecar injector logs
kubectl logs -n dapr-system deployment/dapr-sidecar-injector
```

### TLS Certificate Not Issuing

```bash
# Check certificate status
kubectl describe certificate todo-app-tls -n todo-app

# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# Check ClusterIssuer status
kubectl describe clusterissuer letsencrypt-prod

# Common issues:
# - DNS not propagated: Wait 5-60 minutes
# - HTTP01 challenge failing: Check ingress is reachable on port 80
# - Rate limit: Use letsencrypt-staging for testing
```

### Kafka Connection Issues

```bash
# Check Dapr component status
kubectl describe component kafka-pubsub -n todo-app

# Test connectivity from pod
kubectl run -it --rm kafka-test \
  --image=edenhill/kcat:1.7.1 \
  --restart=Never \
  -- -b $KAFKA_BOOTSTRAP_SERVERS \
     -X security.protocol=SASL_SSL \
     -X sasl.mechanisms=SCRAM-SHA-256 \
     -X sasl.username=$KAFKA_SASL_USERNAME \
     -X sasl.password=$KAFKA_SASL_PASSWORD \
     -L

# Check Dapr sidecar logs for Pub/Sub errors
kubectl logs -n todo-app deployment/todo-backend -c daprd | grep pubsub
```

### Ingress Not Routing

```bash
# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller

# Test directly to service (port-forward)
kubectl port-forward -n todo-app svc/frontend-service 3000:3000

# Open http://localhost:3000 in browser

# Check ingress rules
kubectl describe ingress todo-app-ingress -n todo-app
```

### Database Connection Issues

```bash
# Check database secret
kubectl get secret todo-backend-secrets -n todo-app -o yaml

# Decode DATABASE_URL
kubectl get secret todo-backend-secrets -n todo-app \
  -o jsonpath='{.data.DATABASE_URL}' | base64 -d

# Test connection from pod
kubectl exec -it -n todo-app deployment/todo-backend -c backend -- \
  python -c "import os; import psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))"
```

---

## Cleanup

### Delete Helm Release

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app
```

### Delete Cloud Resources

```bash
# OKE
oci ce cluster delete --cluster-id $CLUSTER_ID --force

# AKS
az aks delete --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --yes --no-wait
az group delete --name $RESOURCE_GROUP --yes --no-wait

# GKE
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet
```

### Delete Redpanda Cloud Cluster

1. Log in to Redpanda Cloud Console
2. Select your cluster
3. Click "Delete cluster"
4. Confirm deletion

---

## Next Steps

- **Monitoring**: Set up Prometheus/Grafana for observability
- **Logging**: Integrate ELK/EFK stack or cloud logging (CloudWatch/Stackdriver)
- **Alerting**: Configure alerts for pod failures, high resource usage, certificate expiry
- **Scaling**: Tune HPA settings based on load testing
- **Security**: Implement NetworkPolicies, Pod Security Standards, secret rotation
- **CI/CD**: Automate deployments with GitHub Actions (see `.github/workflows/deploy.yml`)
- **Backup**: Set up PostgreSQL backups and disaster recovery

---

## Summary Table

| Step | Component | Status | Verification Command |
|------|-----------|--------|---------------------|
| 1 | Cloud K8s Cluster | ✅ | `kubectl get nodes` |
| 2 | kubectl Context | ✅ | `kubectl config current-context` |
| 3 | Dapr Runtime | ✅ | `dapr status -k` |
| 4 | Redpanda Cloud | ✅ | Test connectivity with kcat |
| 5 | Dapr Kafka Component | ✅ | `kubectl get component -n todo-app` |
| 6 | cert-manager | ✅ | `kubectl get pods -n cert-manager` |
| 7 | nginx-ingress | ✅ | `kubectl get svc -n ingress-nginx` |
| 8 | Docker Images | ✅ | Check GHCR packages |
| 9 | Kubernetes Secrets | ✅ | `kubectl get secrets -n todo-app` |
| 10 | Helm Deployment | ✅ | `helm list -n todo-app` |
| 11 | Pods Running | ✅ | `kubectl get pods -n todo-app` |
| 12 | HTTPS Access | ✅ | `curl https://$DOMAIN` |

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintainer**: Todo App Team
**Support**: https://github.com/Dzuhaib/In-Memory-Python-Console-App/issues
