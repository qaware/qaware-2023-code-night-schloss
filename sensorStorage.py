import os
from typing import List

import motor
import requests
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

from models import SensorDataModel, SensorUpdateModel

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data

async def createSensorData(data: SensorDataModel):
    print("Started persisting sensor data!")
    new_data = await db["sensordata"].insert_one(jsonable_encoder(data))
    created_data = await db["sensordata"].find_one({"_id": new_data.inserted_id})
    print("Successfully persisted sensor data!")
    return created_data


async def listSensorData():
    data = await db["sensordata"].find().to_list(1000)
    return data


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
