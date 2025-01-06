import requests
import redis
from flask import current_app
import hashlib
import json

# Connect to Redis
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

def fetch_earthquake_data(params):
    # Generate a unique key for caching
    cache_key = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()

    # Check if the response is cached
    cached_response = redis_client.get(cache_key)
    if cached_response:
        current_app.logger.info("Cache hit")
        return json.loads(cached_response)
    
    current_app.logger.info("Cache miss")
    try:
        response = requests.get(current_app.config["USGS_API_BASE"], params=params)
        response.raise_for_status()
        data = response.json()

        # Cache the response for 30 seconds
        redis_client.setex(cache_key, 30, json.dumps(data))
        return data
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching data: {e}")
        return {"error": str(e)}, 500