import os
from typing import List

import motor
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from motor import motor_asyncio
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from pydantic.class_validators import Optional
from starlette import status
from starlette.responses import JSONResponse


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SensorDataModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    temperature: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Sensor",
                "temperature": 300
            }
        }


class SensorUpdateModel(BaseModel):
    name: Optional[str]
    temperature: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "New Sensor Name",
                "temperature": 320
            }
        }


app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.sensor_data


@app.get("/", response_description="Hello World")
def hello_world():
    return "Hello World!"


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
