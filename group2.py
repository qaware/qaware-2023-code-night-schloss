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


@app.get("/address/", response_description="Get Address", response_model=Address)
def get_address():
    address_object = Address(country="Germany", city="Mainz", street="Leo-Trepp-Platz", house_number="1")
    return JSONResponse(status_code=status.HTTP_200_OK, content=address_object.json())


@app.post("/address/", response_description="Create Address", response_model=Address)
def create_address(data: Address):
    print(data.country)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data.json())


def communicate_with_group_1():
    # TODO: Implement a REST end point to communicate with group 1
    return None


def communicate_with_group_3():
    # TODO: Implement a REST end point to communicate with group 3
    return None

