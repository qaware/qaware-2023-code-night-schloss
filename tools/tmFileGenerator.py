import datetime
import json
import random
import time


class Sensor:
    def __init__(self, name, type):
        self.name = name
        self.type = type


available_sensors = [
    Sensor("thruster_1.a", "thruster"),
    Sensor("thruster_1.b", "thruster"),
    Sensor("thruster_1.c", "thruster"),
    Sensor("thruster_2.a", "thruster"),
    Sensor("thruster_2.b", "thruster"),
    Sensor("thruster_2.c", "thruster"),
    Sensor("thruster_3.a", "thruster"),
    Sensor("thruster_3.b", "thruster"),
    Sensor("thruster_3.c", "thruster"),
    Sensor("oxygen_tank_1", "gas_valve"),
    Sensor("oxygen_tank_2", "gas_valve"),
    Sensor("hydrogen_tank_1", "gas_valve"),
    Sensor("hydrogen_tank_2", "gas_valve")
]


def generate_json():
    selected_sensor_index = random.randint(0, len(available_sensors) - 1)
    # selected_sensor = random.sample(available_sensors, 1)
    selected_sensor = available_sensors[selected_sensor_index]

    pressure = random.uniform(0.5, 9.0)
    temperature = random.uniform(200.0, 500.0)
    telemetry_content = {
        "type": selected_sensor.type,
        "name": selected_sensor.name,
        "pressure": pressure,
        "temperature": temperature
    }
    return telemetry_content


if __name__ == '__main__':

    while 1 == 1:
        tm_content = generate_json()

        filename = "TM_" + datetime.datetime.now().isoformat() + ".json"
        with open(filename, "w") as file:
            json.dump(tm_content, file)

        print("Wrote " + filename)
        sleep_duration = random.randint(3, 30)
        time.sleep(sleep_duration)
