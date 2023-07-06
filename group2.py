import os

import motor
from fastapi import FastAPI
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data


@app.get("/hello_world", response_description="Hello World")
def hello_world():
    response = "Hello World"
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


def communicate_with_group_1():
    # TODO: Implement a REST end point to communicate with group 1
    return None


def communicate_with_group_3():
    # TODO: Implement a REST end point to communicate with group 3
    return None

