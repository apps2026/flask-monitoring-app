# Flask Monitoring Stack Project

This README.md provides detailed instructions for setting up, running, and verifying a Flask monitoring application with **Prometheus** and **Grafana** using Docker and Docker Compose.

---

## 1️⃣ Project Folder Structure

```
flask-monitoring-app/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       └── metrics.py
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── datasource.yml
├── docker-compose.yml
└── README.md
```

- **backend/**: Flask app with Dockerfile and Python dependencies.
- **prometheus/**: Prometheus configuration file.
- **grafana/**: Grafana provisioning folder to auto-load data sources.
- **docker-compose.yml**: Defines all services (Flask, Prometheus, Grafana).

---

## 2️⃣ Required Software and Environment Setup

**Prerequisites:**

- **Docker** (>= 20.10)
- **Docker Compose** (>= 1.29)
- **curl** (optional, for testing)

**Installation on Ubuntu:**

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker

# Install Docker Compose
sudo apt install -y docker-compose

# Verify installations
docker --version
docker-compose --version
```

**Add your user to docker group (optional for non-root usage):**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3️⃣ Docker & Docker Compose Cheat Sheet

**Build and start all services:**
```bash
docker-compose up --build
```

**Stop all services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Check running containers:**
```bash
docker-compose ps
```

**Rebuild a single service:**
```bash
docker-compose build backend
```

**Run a one-off command inside a container:**
```bash
docker exec -it flask_app bash
```

**Remove all stopped containers and free ports:**
```bash
docker container prune
```

---

## 4️⃣ Verify Flask App, Prometheus, Grafana URLs

**Flask:**
```bash
curl http://localhost:5000/
```
Expected output:
```json
{"message":"Hello, Flask with Prometheus!"}
```

**Prometheus:**
- URL: [http://localhost:9090](http://localhost:9090)
- Check **Status → Targets** → Flask app should be UP
- Query metric: `flask_request_count`

**Grafana:**
- URL: [http://localhost:3001](http://localhost:3001)
- Login: `admin` / `admin`
- Go to **Configuration → Data Sources → Prometheus** to verify connection

---

## 5️⃣ Verify Prometheus Alerts (Optional)

1. Add an alert rule in Prometheus config (prometheus.yml):
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - "alert.rules.yml"
```

2. Example alert rule (`alert.rules.yml`):
```yaml
groups:
- name: flask_alerts
  rules:
  - alert: HighRequestRate
    expr: rate(flask_request_count[1m]) > 5
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: High request rate on Flask app
```

3. Reload Prometheus:
```bash
docker-compose restart prometheus
```

4. Check **Alerts → Active Alerts** in Prometheus UI.

---

## 6️⃣ Setup Grafana Dashboard

**Step-by-Step:**

1. Open Grafana: `http://localhost:3001`
2. Add data source (if not auto-provisioned): **Prometheus → URL: http://prometheus:9090 → Save & Test**
3. Create a new dashboard:
   - Click **+ → Dashboard → Add new panel**
   - Query: `flask_request_count`
   - Visualization: Time series / Graph
   - Apply panel and save dashboard
4. Optional Prometheus queries:
   - Total requests: `sum(flask_request_count)`
   - Requests per second: `rate(flask_request_count[1m])`
5. Add more panels for latency or error metrics if added in Flask app.

---

## 7️⃣ Debugging & Investigation Steps

**Common Issues and Fixes:**

1. **Flask ModuleNotFoundError**
   - Ensure folder structure matches Docker COPY paths
   - Use `python -m app.main` in Docker CMD
   - Make sure `__init__.py` exists in app folder

2. **Port already in use**
   - Check running containers: `docker ps`
   - Stop conflicting container: `docker stop <container>`
   - Remove old container: `docker rm <container>`

3. **Flask not reachable**
   - Ensure `host="0.0.0.0"` in `app.run()`
   - Check Docker port mapping: `5000:5000`

4. **Prometheus target down**
   - Check Flask container logs
   - Ensure Prometheus target URL matches container name: `backend:5000`

5. **Grafana dashboard not showing data**
   - Verify data source connection (Prometheus URL inside Docker: `http://prometheus:9090`)
   - Check Prometheus metrics endpoint `/metrics`
   - Ensure Prometheus is scraping Flask app successfully

6. **Container build errors**
   - Make sure COPY paths in Dockerfile are correct relative to build context
   - Rebuild container: `docker-compose up --build`

---

## ✅ Summary Flow

```
Flask App → /metrics endpoint → Prometheus scrapes → Grafana visualizes
```

- Hit Flask endpoints → metrics increment → Prometheus scrapes → Grafana dashboard updates

---

This cheat sheet ensures that **setup, run, verify, and debug steps** are all included for the **Flask + Prometheus + Grafana monitoring stack**.

