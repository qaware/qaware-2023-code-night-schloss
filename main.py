import os
from typing import List

import motor
import requests
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

from models import SensorDataModel, SensorUpdateModel, Address

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data


@app.get("/hello_world", response_description="Hello World")
def hello_world():
    response = "Hello World"
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@app.get("/address/", response_description="Address", response_model=Address)
def address():
    address = Address(country="Germany", city="Mainz", street="Leo-Trepp-Platz", house_number="1")
    return JSONResponse(status_code=status.HTTP_200_OK, content=address.json())


@app.post("/address/", response_description="Address", response_model=Address)
def address(data: Address):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data.json())


@app.post("/sensor/", response_description="Create Sensor Data", response_model=SensorDataModel)
async def create_sensor_data(data: SensorDataModel):
    new_data = await db["sensordata"].insert_one(jsonable_encoder(data))
    created_data = await db["sensordata"].find_one({"_id": new_data.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


@app.get("/sensor/", response_description="List All Sensor Data", response_model=List[SensorDataModel])
async def list_sensor_data():
    data = await db["sensordata"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.get("/sensor/{id}", response_description="Read A Single Sensor Data", response_model=SensorDataModel)
async def read_sensor_data(id: str):
    data = await db["sensordata"].find_one({"_id": id})

    if data is None:
        raise HTTPException(status_code=404, detail=f"Sensor Data {id} not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.put("/sensor/{id}", response_description="Update A Single Sensor Data", response_model=SensorDataModel)
async def update_sensor_data(id: str, update: SensorUpdateModel):
    data = await db["sensordata"].find_one({"_id": id})

    if data is None:
        raise HTTPException(status_code=404, detail=f"Sensor Data {id} not found")

    update_result = await db["sensordata"].update_one({"_id": id}, {"$set": jsonable_encoder(update)})
    if update_result.modified_count == 1:
        updated_data = await db["sensordata"].find_one({"_id": id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=updated_data)

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.delete("/sensor/{id}", response_description="Delete A Single Sensor Data")
async def delete_sensor_data(id: str):
    delete_result = await db["sensordata"].delete_one({"_id": id})

    if delete_result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Sensor Data {id} not found")

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

if __name__ == '__main__':
    sensor = SensorDataModel(name="Test")
    address = Address(country="Germany", city="Mainz", street="Leo-Trepp-Platz", house_number="1a")
    answer1 = requests.post("http://127.0.0.1:8000/sensor/", sensor.json())
    answer2 = requests.post("http://127.0.0.1:8000/address/", address.json())
    answer3 = requests.get("http://127.0.0.1:8000/address/")
    print(answer1.status_code)
    print(answer2.status_code)
    print(answer3.status_code)
