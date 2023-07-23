import json

# TODO: ensure data is not processed twice
def readSensorData():
    print("Started reading sensor data!")
    
    data = open('data/data-1.json')
    data = json.load(data)
    
    print("Successfully read sensor data!")
    
    return data
