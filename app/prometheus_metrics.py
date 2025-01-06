from prometheus_flask_exporter import PrometheusMetrics

def setup_metrics(app):
    # Initialize PrometheusMetrics with the Flask app
    metrics = PrometheusMetrics(app)

    # Add app info as a Prometheus metric
    metrics.info("app_info", "Earthquake service info", version="1.0.0")
