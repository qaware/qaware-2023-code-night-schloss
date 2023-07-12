import json
import os
import time

import requests

from models import Address

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000"
os.environ["FILESYSTEM_BASE_PATH"] = ""

# Methods: =============================================================================================================


def hello_world():
    return requests.get(os.environ["SERVICE_URL"] + '/hello_world').content


def create_address(data: Address):
    answer = requests.post(os.environ["SERVICE_URL"] + '/address', data.json())
    address_object = json.loads(json.loads(answer.content), object_hook=lambda d: Address(**d))
    return address_object


def send_to_group2():
    # TODO: Implement the REST call to group 2
    return None


# Main Program: ========================================================================================================


while True:
    print(f"Hello World: {hello_world()}")
    data = Address(country="Germany", city="Mainz", street="Leo-Trepp-Platz", house_number="1")
    print(f"Adresse: {create_address(data).country}")
    time.sleep(2)
