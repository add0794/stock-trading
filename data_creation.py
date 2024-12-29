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
        print(f"Attempting to write to {file_path}")
        try:
            with open(file_path, "r") as data_file:
                data = json.load(data_file)
                print("Existing file found and loaded")
        except FileNotFoundError:
            print("File not found, creating new file")
            data = default_data
            with open(file_path, "w") as data_file:
                json.dump(default_data, data_file, indent=formatting, ensure_ascii=False)
                print("New file written")
        else:
            print("Updating existing file")
            data.update(default_data)
            with open(file_path, "w") as data_file:
                json.dump(data, data_file, indent=formatting, ensure_ascii=False)
                print("File updated")
        return data