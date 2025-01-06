import logging

def setup_logger(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")  # Default to INFO if not set
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    app.logger = logging.getLogger()
