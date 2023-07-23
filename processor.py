import json

from models import SensorDataModel
from sensorStorage import *

# TODO: create or update
async def processSensorData(data: SensorDataModel):
    print("Started processing sensor data!")
    
    persisted_data = await createSensorData(data)

    print("Successfully processed sensor data!")

    return persisted_data
