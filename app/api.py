from flask import Blueprint, request, jsonify, current_app
from app.utils import fetch_earthquake_data
import json
import os

# Load configuration file
config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path) as config_file:
    CONFIG = json.load(config_file)

API_DEFAULTS = CONFIG["api_defaults"]

api_blueprint = Blueprint("api", __name__)

def validate_params(params, required_fields):
    """Validate required query parameters."""
    missing = [field for field in required_fields if not params.get(field)]
    if missing:
        return f"Missing required parameters: {', '.join(missing)}"
    return None


@api_blueprint.route("/earthquakes/sf", methods=["GET"])
def earthquakes_sf():
    try:
        # Extract query parameters
        min_magnitude = float(request.args.get("min_magnitude", 2.0))
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")

        # Validate required parameters
        error_message = validate_params(request.args, ["start_time", "end_time"])
        if error_message:
            return jsonify({"error": error_message}), 400

        params = {
            "format": API_DEFAULTS["format"],
            "minlatitude": API_DEFAULTS["minlatitude"],
            "maxlatitude": API_DEFAULTS["maxlatitude"],
            "minlongitude": API_DEFAULTS["minlongitude"],
            "maxlongitude": API_DEFAULTS["maxlongitude"],
            "starttime": start_time,
            "endtime": end_time,
            "minmagnitude": min_magnitude,
        }

        current_app.logger.info(f"Fetching SF earthquakes with params: {params}")
        response = fetch_earthquake_data(params)

        # Handle no results
        if not response.get("features", []):
            response["message"] = "No earthquakes found for the given criteria."
        else:
            current_app.logger.info(f"Earthquakes found: {len(response['features'])}")

        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error in earthquakes_sf: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@api_blueprint.route("/earthquakes/sf/felt", methods=["GET"])
def earthquakes_sf_felt():
    try:
        # Extract query parameters
        min_magnitude = float(request.args.get("min_magnitude", 2.0))
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        min_felt = int(request.args.get("min_felt", 10))

        # Validate required parameters
        error_message = validate_params(request.args, ["start_time", "end_time"])
        if error_message:
            return jsonify({"error": error_message}), 400

        params = {
            "format": API_DEFAULTS["format"],
            "minlatitude": API_DEFAULTS["minlatitude"],
            "maxlatitude": API_DEFAULTS["maxlatitude"],
            "minlongitude": API_DEFAULTS["minlongitude"],
            "maxlongitude": API_DEFAULTS["maxlongitude"],
            "starttime": start_time,
            "endtime": end_time,
            "minmagnitude": min_magnitude,
            "minfelt": min_felt,
        }

        current_app.logger.info(f"Fetching SF earthquakes with felt reports using params: {params}")
        response = fetch_earthquake_data(params)

        # Handle no results
        if not response.get("features", []):
            response["message"] = "No earthquakes found with felt reports for the given criteria."
        else:
            current_app.logger.info(f"Earthquakes with felt reports found: {len(response['features'])}")

        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error in earthquakes_sf_felt: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@api_blueprint.route("/earthquakes/tsunami", methods=["GET"])
def earthquakes_tsunami():
    try:
        # Extract query parameters
        state = request.args.get("state")
        min_magnitude = float(request.args.get("min_magnitude", 2.0))

        # Validate required parameters
        error_message = validate_params(request.args, ["state"])
        if error_message:
            return jsonify({"error": error_message}), 400

        params = {
            "format": "geojson",
            "minmagnitude": min_magnitude,
            "alertlevel": "red",
        }

        current_app.logger.info(f"Fetching tsunami earthquakes for state={state} with params: {params}")
        response = fetch_earthquake_data(params)

        # Handle no results
        if not response.get("features", []):
            response["message"] = f"No tsunami-related earthquakes found for {state}."
        else:
            current_app.logger.info(f"Tsunami earthquakes found: {len(response['features'])}")

        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error in earthquakes_tsunami: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
