
---
## Project Overview

## ✅ DevOps Task Completion Checklist

| Task Item                                                    | Status                       |
| ------------------------------------------------------------ | ---------------------------- |
| 1. **Flask REST API with `/health` and `/data`**             | ✅ Done                       |
| 2. **Connected to MongoDB with env credentials**             | ✅ Done                       |
| 3. **Dockerized app with Dockerfile**                        | ✅ Done                       |
| 4. **Docker Compose with services:**                         |                              |
| ─ `application`                                              | ✅ Done                       |
| ─ `database` (MongoDB)                                       | ✅ Done                       |
| ─ `prometheus`                                               | ✅ Done                       |
| ─ `grafana`                                                  | ✅ Done                       |
| ─ `elasticsearch`, `logstash`, `kibana`                      | ✅ Done                       |
| 5. **CI/CD with GitLab CI**                                  | ✅ Done                       |
| ─ `build` stage                                              | ✅ Done                       |
| ─ `push` stage                                               | ✅ Done                       |
| ─ `deploy` stage                                             | ✅ Done                       |
| ─ `test` stage with curl (manual trigger)                    | ✅ Done                       |
| 6. **Monitoring with Prometheus and Grafana**                | ✅ Done                       |
| ─ Prometheus scrapes app metrics                             | ✅ Done                       |
| ─ Grafana with dashboards via provisioning                   | ✅ Done                       |
| 7. **Logging with ELK**                                      | ✅ Done                       |
| ─ Application logs sent to Logstash via TCP                  | ✅ Done                       |
| ─ Logs searchable in Kibana (via Elasticsearch)              | ✅ Done                       |
| 8. **README documentation**                                  | ✅ Done                       |
| ─ How to run project locally                                 | ✅ Done                       |
| ─ GitLab setup instructions                                  | ✅ Done                       |
| ─ Monitoring & logging walkthrough                           | ✅ Done                       |
| ─ Application test commands                                  | ✅ Done                       |
| 9. **Bonus items**                                           |                              |
| ─ `.env` used for image tag and config                       | ✅ Done                       |
| ─ Docker best practices applied (slim image, no cache, etc.) | ✅ Done                       |
| ─ Clean and modular pipeline design                          | ✅ Done                       |
| 10. *(Optional)* Infrastructure as Code (Ansible/Terraform)  | ❌ Not implemented (optional) |

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/mhesfahani97/my-devops-project.git
cd my-devops-project
```

### 2. Prepare Docker Compose

Temporarily disable the application service:

```bash
vim docker-compose.yml
# Comment out the application service section
```

### 3. Pull and Start Core Services

Start all supporting services (GitLab, monitoring, logging):

```bash
docker compose pull
docker pull docker.arvancloud.ir/curlimages/curl:8.14.1 
docker pull docker.arvancloud.ir/docker:dind
docker compose up -d gitlab runner grafana prometheus mongo-exporter elasticsearch kibana logstash
```

### 4. Enable Application Service

Once the core services are up, re-enable the application:

```bash
vim docker-compose.yml
# Uncomment the application service
```

> ⏱ **Wait \~10 minutes** for GitLab to fully initialize.

---

### 5. GitLab Setup

#### 🔑 Get GitLab Root Password

```bash
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

#### 🌐 Access GitLab in Your Browser

```
http://localhost:80
```

* **Username:** `root`
* **Password:** *from the command above*

#### 📁 Create Project

1. Log in to GitLab.
2. Create a new **project** named `my-devops-project` (leave README unchecked).

#### 🔐 Add Your SSH Key

Navigate to **User Settings > SSH Keys** and add your public key.

---

### 6. Register GitLab Runner

#### 🔍 Get Registration Token

Go to:

```
http://localhost/admin/runners
```

Copy the **registration token**.

#### 🛠 Register the Runner

```bash
docker exec -it runner gitlab-runner register
```

Use the following options:

* **GitLab instance URL:** `http://localhost/`
* **Registration token:** `<paste token>`
* **Runner description:** `app`
* **Tags:** `production-like`
* **optional maintenance note for the runner:** `press enter`
* **Executor:** `docker`
* **Docker image:** `docker.arvancloud.ir/docker:dind`

#### 🧩 Update Runner Config

Edit the runner config file:

```bash
sudo vim ./runner-config/config.toml
```

Make the following changes:

```toml
privileged = true
volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock", "/builds:/builds"]

[runners.docker]
pull_policy = ["if-not-present"]
network_mode = "host"
```

Restart the runner:

```bash
docker restart runner
```

---

### 7. Connect Local Repo to GitLab (pipeline based on merge and push)

```bash
cd my-devops-project
git remote add gitlab git@localhost:root/my-devops-project.git
```

Commit and push the code:

```bash
sudo git add -A
git commit -m "Start deploying"
git push gitlab
```

---

## 8. 📈 Monitoring & 📑 Logging

### 8-1 Prometheus

1. Open **Prometheus Targets** in your browser:  
```
http://localhost:9090/targets
```
> ⏱ **Wait \~5 minutes** for application to fully initialize.
You should see the `application`, `mongo-exporter`.

### 8-2 Grafana

1. Visit Grafana dashboard and datasource:  
```

http://localhost:3000

```
* **Username:** `admin`  
* **Password:** `admin`

### 8-3 ELK (Stack)

1. Open Kibana:  
```

http://localhost:5601

```

2. Navigate to **Stack Management ▸ Index Management**.  
You should see your Elasticsearch indices (e.g., `flask-logs-*`).

3. **View live logs**

* Go to **Discover** in Kibana’s sidebar.
* Pick the index pattern that matches your logs (`flask-logs-*`).
* Set time field to `@timestamp`.
* Now create index pattern.
* Go to discover again and Set the time range (top-right) to **Last 15 minutes**.
* Logs streamed by the application (via Logstash) will appear in real time — search, filter, or add visualizations as needed.

---

## 🧪 Test Application Functionality

After the application is running, you can verify that it's working using the following commands:

### 1. Check Health Endpoint

```bash
curl http://localhost:5000/health
````
---

### 2. Insert Sample Data

```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"user": "esfahani", "score": 20}'
```

---

### 3. Retrieve All Data

```bash
curl http://localhost:5000/data
```

---

### 4. Check Prometheus Metrics

```bash
curl http://localhost:5000/metrics
```
---
