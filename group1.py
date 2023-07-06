import os
import time

import requests

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000"
os.environ["FILESYSTEM_BASE_PATH"] = ""

# Methods: =============================================================================================================


def hello_world():
    return requests.get(os.environ["SERVICE_URL"] + '/hello_world').content


def get_file_names_in_directory():
    # TODO: Implement a method to read all file names in a directory
    return []


def detect_new_files():
    # TODO: Implement an identification of new files in the given list
    return []


def read_from_file():
    # TODO: Implement a method to read the content of a file
    return None


def generate_json():
    # TODO: Implement a method to package information to be send to the API
    return None


def send_to_group2():
    # TODO: Implement the REST call to group 2
    return None


# Main Program: ========================================================================================================


while True:
    print(hello_world())
    time.sleep(2)
