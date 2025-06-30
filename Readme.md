
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
docker compose up -d gitlab runner grafana prometheus mongo-exporter elasticsearch kibana logstash
```

### 4. Enable Application Service

Once the core services are up, re-enable the application:

```bash
vim docker-compose.yml
# Uncomment the application service
```

> ⏱ **Wait \~5–10 minutes** for GitLab to fully initialize.

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
* **Executor:** `docker`
* **Docker image:** `docker.arvancloud.ir/docker:latest`

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

### 7. Connect Local Repo to GitLab

```bash
cd my-devops-project
git remote add gitlab git@localhost:root/my-devops-project.git
```

Commit and push the code:

```bash
git add -A
git commit -m "Start deploying"
git push gitlab
```

---

## 8. 📈 Monitoring & 📑 Logging

### 8-1 Prometheus

1. Open **Prometheus Targets** in your browser:  
```

[http://localhost:9090/targets](http://localhost:9090/targets)

```
You should see the `application`, `mongo-exporter`, and any other scrape targets listed as **UP**.

### 8-2 Grafana

1. Visit Grafana:  
```

[http://localhost:3000](http://localhost:3000)

```
* **Username:** `admin`  
* **Password:** `admin` (prompted to change on first login)

2. **Add the Prometheus data-source**

| Field | Value |
|-------|-------|
| **Type** | `Prometheus` |
| **URL** | `http://prometheus:9090` |
| **Skip TLS verification** | ✅ (check it) |
| **HTTP Method** | `GET` |

Click **Save & Test** — you should see “Data source is working”.

3. **Import dashboards**

* Grafana → **Dashboards ▸ Import**
* Upload or paste the JSON files from `./grafana/dashboards/`
* Hit **Import**

Your panels should immediately start displaying app and database metrics.

### 8-3 ELK (Stack)

1. Open Kibana:  
```

[http://localhost:5601](http://localhost:5601)

```

2. Navigate to **Stack Management ▸ Index Management**.  
You should see your Elasticsearch indices (e.g., `app-logs-000001`).

3. **View live logs**

* Go to **Discover** in Kibana’s sidebar.
* Pick the index pattern that matches your logs (e.g., `app-logs-*`).
* Set the time range (top-right) to **Last 15 minutes**.
* Logs streamed by the application (via Logstash) will appear in real time — search, filter, or add visualizations as needed.

> ℹ️ If no logs appear, check the Logstash container logs for connection errors and ensure the application container can reach `logstash:5000`.

---
