import json
import os

import motor
from fastapi import FastAPI
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

from models import Address

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data


@app.get("/hello_world", response_description="Hello World")
def hello_world():
    response = "Hello World"
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@app.get("/address", response_description="Get Address")
def get_address():
    address = Address(country="Germany", city="Mainz", street="Leo-Trepp-Platz", house_number="1")
    json_address = json.dumps(address.__dict__)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json_address)


@app.post("/address", response_description="Create Address")
def create_address(create: str):
    address = json.loads(json.loads(create), object_hook=lambda d: Address(**d))
    print(address.country)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create)


def communicate_with_group_1():
    # TODO: Implement a REST end point to communicate with group 1
    return None


def communicate_with_group_3():
    # TODO: Implement a REST end point to communicate with group 3
    return None

