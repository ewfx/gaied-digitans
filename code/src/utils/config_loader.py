import json
import os

# Define the path to the request types JSON configuration file
CONFIG_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, "request_types.json")

def load_request_type_config():
    """Loads request type and expected field configurations from the JSON file."""
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE_PATH}")

    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def get_valid_request_types():
    """Returns a dictionary of valid request types and their sub-request types."""
    config = load_request_type_config()
    return {key: value["sub_types"] for key, value in config.items()}

def get_expected_fields(request_type):
    """
    Returns the expected structured fields for a given request type.

    :param request_type: The request type for which fields are needed.
    :return: A list of expected fields.
    """
    config = load_request_type_config()

    if request_type in config:
        return config[request_type].get("expected_fields", [])

    return []
