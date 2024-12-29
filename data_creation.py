import json
import requests

class DataHandler:
    def __init__(self, endpoint, api_call):
        self.endpoint = endpoint
        self.api_call = api_call


    def get_data(self, existing_data=None):
        if existing_data is not None:
            return existing_data
        try:
            request = requests.get(self.endpoint, params=self.api_call)
            data = request.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def load_or_create_json(self, file_path, default_data, formatting=None):
        try:
            with open(file_path, "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = default_data
            with open(file_path, "w") as data_file:
                json.dump(default_data, data_file, indent=formatting, ensure_ascii=False)
        else:
            # Update existing data with default_data
            data.update(default_data)
            with open(file_path, "w") as data_file:
                json.dump(data, data_file, indent=formatting, ensure_ascii=False)
        return data