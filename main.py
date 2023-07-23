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
from reader import * 
from processor import * 
from fetcher import * 
from sensorStorage import * 

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data


@app.post("/sensor/", response_description="Create Sensor Data", response_model=SensorDataModel)
async def create_sensor_data(data: SensorDataModel):
    created_data = await createSensorData(data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


@app.get("/sensor/", response_description="List All Sensor Data", response_model=List[SensorDataModel])
async def list_sensor_data():
    data = await getAllSensorData()
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

@app.get("/read", response_description="Read and return sensor data")
def readData():
    data = readSensorData()
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

@app.post("/store/", response_description="Stores the sensor data", response_model=SensorDataModel)
async def storeData(data: SensorDataModel):
    stored_data = await processSensorData(data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=stored_data)

@app.get("/all/", response_description="List All Sensor Data", response_model=List[SensorDataModel])
async def list_sensor_data():
    data = await getAllSensorData()
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

if __name__ == '__main__':
    answer1 = requests.get("http://127.0.0.1:8000/read")
    print("Got response with status code " + str(answer1.status_code) + " and content " + answer1.content.decode('utf-8') + " when reading data")
    answer2 = requests.post("http://127.0.0.1:8000/store/", answer1.content)
    print("Got response with status code " + str(answer2.status_code) + " and content " + answer2.content.decode('utf-8') + " when persisting data")
    answer3 = requests.get("http://127.0.0.1:8000/all/")
    print("Got response with status code " + str(answer3.status_code) + " and content " + answer3.content.decode('utf-8') + " when requesting all persisted data")
