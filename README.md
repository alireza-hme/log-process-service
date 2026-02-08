# Distributed Log Processing System

A distributed, cloud-native log processing application designed with Microservices Architecture and deployed on Kubernetes. This project demonstrates advanced concepts such as Service Discovery, Layer 7 Routing (Ingress), Persistent Storage (PVC), and Orchestration.

## 🎓 Academic Context

This project was developed as part of the Distributed Systems course.

---

## 🏗 Architecture

The application is composed of 3 stateless microservices and 1 stateful database, communicating via REST APIs:

1. **Log Generator Service**:
   - Generates logs and sends them to the Log Processor.
   - Acts as the entry point for log creation.

2. **Log Processor Service**:
   - Processes incoming logs.
   - Interacts with the PostgreSQL database to store log data.

3. **Stats Display Service**:
   - Fetches and displays log statistics.
   - Queries the database for aggregated data.

4. **Database (Persistence)**:
   - PostgreSQL deployed as a pod inside the cluster.
   - Stores logs and related metadata.
   - Uses PersistentVolume (PVC) for data durability.

---

## 🛠 Tech Stack

- **Language**: Python 3.9 (FastAPI)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Vagrant + kubeadm)
- **Networking**: NGINX Ingress Controller, ClusterIP
- **Database**: PostgreSQL
- **Version Control**: Git & GitHub

---

## 📂 Project Structure

```
distributed-log-processing/
├── log_generator/       # Log Generator Microservice
├── log_process/         # Log Processor Microservice
├── stats_display/       # Stats Display Microservice
├── db/                  # Database Configuration
├── k8s/                 # Kubernetes Manifests
│   ├── ingress.yml      # Ingress Rules
│   ├── metallb-config.yml # MetalLB Configuration
│   └── *-deployment.yml # Deployments with Resource Limits
│   └── *-service.yml    # ClusterIP Services
└── README.md
```

---

## 🚀 Deployment Guide

### Prerequisites

- Docker
- Vagrant
- Kubernetes (kubeadm)
- Kubectl

### Step 1: Bootstrap Cluster & Addons

1. Start the Vagrant VMs and initialize the Kubernetes cluster:

```bash
   vagrant up
   kubeadm init
```

2. Install and configure MetalLB for Load Balancing:

```bash
   kubectl apply -f k8s/metallb-config.yml
```

3. Deploy the NGINX Ingress Controller:

```bash
   kubectl apply -f k8s/ingress.yml
```

---

### Step 2: Deploy Database (PostgreSQL)

1. Apply the database manifests:

```bash
   kubectl apply -f db/k8s/
```

2. Verify the database pod and service:

```bash
   kubectl get pods
   kubectl get svc
```

---

### Step 3: Deploy Microservices

1. Apply all Kubernetes manifests for the microservices:

```bash
   kubectl apply -f log_generator/k8s/
   kubectl apply -f log_process/k8s/
   kubectl apply -f stats_display/k8s/
```

2. Verify the pods and services:

```bash
   kubectl get pods
   kubectl get svc
```

---

### Step 4: Configure DNS and Access the Application

1. Get the MetalLB external IP assigned to Ingress:

```bash
   kubectl get svc -n ingress-nginx
```

2. Add the domain to your `/etc/hosts` file (or `C:\Windows\System32\drivers\etc\hosts` on Windows):

```bash
   192.168.56.240 log-process-service.test
```

3. Access the application using the Ingress domain:
   - `http://log-process-service.test/stats-display`

## 📈 Bonus Features Implemented

1. **Database Integration**:
   - PostgreSQL is used to store logs and statistics.
   - Persistent storage is ensured via PVC.

2. **Horizontal Scaling**:
   - Microservices are designed to scale horizontally.
   - Kubernetes handles load balancing across replicas.

3. **Real Multi-Node Cluster**:
   - Provisioned using **Vagrant** (1 control-plane + 2 worker nodes).
   - Cluster initialized with **kubeadm**.
   - CNI plugin: **Calico** for pod networking.

4. **External Access**:
   - **MetalLB** provides LoadBalancer IPs in bare-metal environment.
   - **Nginx Ingress Controller** routes external traffic to services.
   - Domain-based routing: `log-process-service.test/stats-display`.

5. **Production-Ready Setup**:
   - Multi-node cluster demonstrates real-world Kubernetes deployment.
   - Load balancing tested across worker nodes (w1, w2).
   - Connection pooling disabled to ensure traffic distribution.
