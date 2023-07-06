import os
import time

import requests

# Parameter Definition: ================================================================================================


os.environ["SERVICE_URL"] = "http://127.0.0.1:8000"

# Methods: =============================================================================================================


def hello_world():
    return requests.get(os.environ["SERVICE_URL"] + '/hello_world').content


def ask_from_group_2():
    # TODO: Implement the REST call to group 2
    return None


# Main Program: ========================================================================================================

while True:
    print(hello_world())
    time.sleep(2)
