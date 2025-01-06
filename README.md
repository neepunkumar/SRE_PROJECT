# SRE Take-Home Challenge: Scalable and Highly Available Earthquake Data Service

This project is a scalable and highly available service providing real-time earthquake data from the USGS API. The service extends the USGS earthquake API by adding custom endpoints and ensuring fault tolerance, monitoring, and high availability.

## Features

### API Endpoints

1. **Retrieve Earthquakes in San Francisco Bay Area**
   - Endpoint: `/earthquakes/sf`
   - Query Parameters:
     - `start_time`: Start of the time range (YYYY-MM-DD).
     - `end_time`: End of the time range (YYYY-MM-DD).
   - Example:
     ```bash
     curl "http://localhost/earthquakes/sf?start_time=2024-06-01&end_time=2024-06-16"
     ```

2. **Retrieve Earthquakes with Felt Reports**
   - Endpoint: `/earthquakes/sf/felt`
   - Query Parameters:
     - `start_time`: Start of the time range (YYYY-MM-DD).
     - `end_time`: End of the time range (YYYY-MM-DD).
     - `min_felt`: Minimum number of felt reports.
   - Example:
     ```bash
     curl "http://localhost/earthquakes/sf/felt?start_time=2024-06-01&end_time=2024-06-16&min_felt=10"
     ```

3. **Retrieve Tsunami-Related Earthquakes for a State**
   - Endpoint: `/earthquakes/tsunami`
   - Query Parameters:
     - `state`: Name of the US state.
   - Example:
     ```bash
     curl "http://localhost/earthquakes/tsunami?state=California"
     ```

### Output Formats
- JSON
- XML

### Monitoring
- **Prometheus** for metrics collection.
- **Grafana** for dashboard visualization.
- **NGINX** as a reverse proxy and load balancer.

---

## Setup

### Local Testing with Docker Compose

1. **Prerequisites**
   - Install Docker and Docker Compose.
   - Ensure the project files (e.g., `docker-compose.yml`, `nginx.conf`, `prometheus.yaml`) are in the root directory.

2. **Run the Service**
   ```bash
   docker-compose up --build
   ```
   Services:
   - `earthquake-service` on port `5000`
   - `Redis` on port `6379`
   - `Prometheus` on port `9090`
   - `Grafana` on port `3000`
   - `NGINX` on port `80`

3. **Access the Service**
   - API Endpoints are available through `http://localhost/`.
   - Prometheus Dashboard: `http://localhost:9090`
   - Grafana Dashboard: `http://localhost:3000` (Login: `admin` / `admin`).

---

### Highly Available Setup with Kubernetes

1. **Prerequisites**
   - Install `kubectl` and Minikube.
   - Ensure Kubernetes manifests (e.g., `earthquake-service-deployment.yml`, `redis-deployment.yaml`) are in the `k8s` folder.

2. **Deploy the Service**
   ```bash
   kubectl apply -f k8s/
   ```
   Verify:
   - Pods: `kubectl get pods`
   - Services: `kubectl get services`

3. **Expose LoadBalancer Service**
   - Run Minikube tunnel:
     ```bash
     minikube tunnel
     ```
   - Verify NGINX external IP:
     ```bash
     kubectl get service nginx
     ```

4. **Access the Service**
   Replace `<nginx-loadbalancer-ip>` with the external IP:
   - API Endpoints:
     ```bash
     curl "http://<nginx-loadbalancer-ip>/earthquakes/sf?start_time=YYYY-MM-DD&end_time=YYYY-MM-DD"
     ```

5. **Monitoring**
   - **Prometheus**:
     ```bash
     kubectl port-forward service/prometheus 9090:9090
     ```
     Access: `http://127.0.0.1:9090`
   - **Grafana**:
     ```bash
     kubectl port-forward service/grafana 3000:3000
     ```
     Access: `http://127.0.0.1:3000` (Login: `admin` / `admin`).
     Add Prometheus as Data Source: `http://prometheus:9090`.

---

## System Design

### Architecture
- **Stateless API Service**
  - Scalable with multiple replicas.
  - Caching via Redis to reduce API calls to USGS.
- **NGINX Reverse Proxy**
  - Load balances requests across replicas.
- **Prometheus & Grafana**
  - Monitoring and visualization.

### Tech Stack
- **Backend**: Python (Flask).
- **Containerization**: Docker.
- **Orchestration**: Kubernetes (for production setup).
- **Caching**: Redis.
- **Monitoring**: Prometheus and Grafana.

---

## Bonus Implementation
- API response caching with Redis to avoid duplicate USGS API calls within 30 seconds.

---

## File Structure
```
.
├── docker-compose.yml       # Docker Compose configuration.
├── k8s/                     # Kubernetes manifests.
│   ├── earthquake-service-deployment.yml
│   ├── redis-deployment.yaml
│   ├── nginx-deployment.yaml
│   ├── prometheus-deployment.yaml
│   └── grafana-deployment.yaml
├── nginx.conf               # NGINX configuration.
├── prometheus.yaml          # Prometheus configuration.
├── src/                     # Source code.
│   ├── app.py               # Flask application.
│   ├── requirements.txt     # Python dependencies.
│   └── ...
└── README.md                # Project documentation.
```

---

## Metrics and Dashboards

### Prometheus Queries
- **API Request Count**:
  ```promql
  sum(rate(flask_http_request_total[5m])) by (endpoint)
  ```
- **Error Rate**:
  ```promql
  sum(rate(flask_http_request_total{status=~"5.."}[5m])) by (endpoint)
  ```
- **Request Latency (95th Percentile)**:
  ```promql
  histogram_quantile(0.95, sum(rate(flask_http_request_duration_seconds_bucket[5m])) by (le, endpoint))
  ```

---

## Contributing
Feel free to submit issues or pull requests to improve this project.

---

## License
This project is licensed under the MIT License.
