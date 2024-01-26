# Note: This module is not being used, but its template was used to create the data_creation module.

import json
import requests


def get_data(endpoint, api_call, existing_data=None):
    if existing_data is not None:
        return existing_data

    try:
        request = requests.get(endpoint, params=api_call)
        data = request.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def load_or_create_json(file_path, default_data, formatting=None):
    try:
        with open(file_path, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open(file_path, "w") as data_file:
            json.dump(default_data, data_file, indent=4, ensure_ascii=False)