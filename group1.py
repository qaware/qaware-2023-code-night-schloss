import os
import time

import requests

from main import SensorDataModel, SensorUpdateModel

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000/"
os.environ["FILESYSTEM_BASE_PATH"] = ""

# Methods: =============================================================================================================


def create_data(create: SensorDataModel):
    return requests.post(os.environ["SERVICE_URL"] + 'sensor/', create.json())


def update_data(id: str, update: SensorUpdateModel):
    return requests.put(os.environ["SERVICE_URL"] + 'sensor/' + id, update.json())


def get_file_names_in_directory(directory_path: str):
    # TODO: Implement a method to read all file names in a directory
    return []


def detect_new_files(file_names: list):
    # TODO: Implement an identification of new files in the given list
    return []


def read_from_file(file_path: str):
    # TODO: Implement a method to read the content of a file
    return None


def generate_json(file_content: str):
    # TODO: Implement a method to package information to be send to the API
    return None


# Main Program: ========================================================================================================


while True:
    files = get_file_names_in_directory(os.environ["FILESYSTEM_BASE_PATH"])
    new_files = detect_new_files(files)
    for file in new_files:
        content = read_from_file(os.environ["FILESYSTEM_BASE_PATH"] + file)
        response = create_data(generate_json(content))
        print(response.status_code)
    time.sleep(2)
