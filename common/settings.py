import json
HOST = 'localhost'
PORT = 8000
BASE_URLS= f"http://{HOST}:{PORT}"

def load_config(file_path):
    with open(file_path, "r") as config_file:
        config_data = json.load(config_file)
    return config_data