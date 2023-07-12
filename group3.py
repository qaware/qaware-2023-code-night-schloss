import json
import os
import time

import requests

from models import Address

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000"

# Methods: =============================================================================================================


def hello_world():
    return requests.get(os.environ["SERVICE_URL"] + '/hello_world').content


def get_address():
    answer = requests.get(os.environ["SERVICE_URL"] + '/address')
    address_object = json.loads(json.loads(answer.content), object_hook=lambda d: Address(**d))
    return address_object


def ask_from_group_2():
    # TODO: Implement the REST call to group 2
    return None


# Main Program: ========================================================================================================

while True:
    print(f"Hello World: {hello_world()}")
    print(f"Adresse: {get_address().country}")
    time.sleep(2)
