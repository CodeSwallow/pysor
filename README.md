![pysor logo](artwork%2FPysor.png)

# Pysor

Pysor is a Python library for the simulation of various sensors. It is designed to be used with the broker of your choice.
It uses the Paho MQTT library to communicate with the broker.

## Installation
Not yet available on PyPi. To install, clone the repository and run `pip install -r requirements.txt` in the root directory.

## Quickstart
Import the MqttClient class to create a client object. The client object can be used to publish messages to the broker.

```python
from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import TemperatureSensor


if __name__ == '__main__':
    mqtt_client = MqttClient('test.mosquitto.org')

    temperature_sensor = TemperatureSensor(mqtt_client, 'sensor/temperature')

    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)
    sensor_manager.run()
```

## Sensors
Sensors are classes that inherit from the Sensor class. They can be added to the SensorManager to be run.
### Currently available sensors:
- TemperatureSensor
- HumiditySensor
- LightIntensitySensor
- WaterLevelSensor

All sensors have parameters to set the mqtt client, the topic and the interval at which the sensor should publish messages.

### Example of parameters for HumiditySensor
```python
class HumiditySensor(BaseSensor):
    """
    Humidity sensor class.
    Min and max humidity values are in percentage.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: float = 120.0,
                 min_humidity: int = 30,
                 max_humidity: int = 80,
                 humidity_change: float = 1.0,
                 current_humidity: float = None
                 ) -> None:
        ...
```

## Custom Sensors
Extend the BaseSensor class and implement the 'generate_data' method. This method should return the data to be published.
```python
@abstractmethod
def generate_data(self) -> Any:
    """
    Generate data to be published to the broker

    :return: Data
    """
    pass
```

## SensorManager
The SensorManager class is used to run the sensors. It has a method to add sensors and a method to run the sensors.
```python
sensor_manager = SensorManager()

sensor_manager.add_sensor(temperature_sensor)
sensor_manager.add_sensor(humidity_sensor)
sensor_manager.add_sensor(water_level_sensor)
sensor_manager.add_sensor(light_intensity_sensor)

sensor_manager.run()
```