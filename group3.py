import os
import time

import requests

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000/"

# Methods: =============================================================================================================


def get_data(id: str):
    return requests.get(os.environ["SERVICE_URL"] + 'sensor/' + id)


def list_data():
    return requests.get(os.environ["SERVICE_URL"] + 'sensor/')


def save_data(data: list):
    # TODO: Implement a method to save data found in a format usable for the interface
    return None


def update_ui():
    # TODO: Implement a method to update the ui according to changes
    return None


def generate_output():
    # TODO: Implement a method, which formats the output
    return None


# Main Program: ========================================================================================================

# TODO: generate a UI here, which then needs to be updated

while True:
    data = list_data()
    save_data(data)
    generate_output()
    update_ui()
    time.sleep(2)
