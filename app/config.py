import os

class Config:
    USGS_API_BASE = os.getenv("USGS_API_BASE", "https://earthquake.usgs.gov/fdsnws/event/1/query")
    PROMETHEUS_SCRAPE_INTERVAL = int(os.getenv("PROMETHEUS_SCRAPE_INTERVAL", 30))
    DEFAULT_REGION = os.getenv("DEFAULT_REGION", "San Francisco Bay Area")
    TSUNAMI_ALERT_PARAM = os.getenv("TSUNAMI_ALERT_PARAM", "alertlevel=red")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default to INFO

