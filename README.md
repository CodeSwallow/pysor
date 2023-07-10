<div align="center">
<img src="artwork/Pysor.png" alt="logo"/>
</div>

<div align="center">
<img src="https://github.com/CodeSwallow/pysor/actions/workflows/python-package.yml/badge.svg" alt="workflow status"/>
<img src="artwork/coverage.svg" alt="coverage"/>
</div>

Pysor is a Python library for the simulation of various sensors. It is designed to be used with an MQTT broker of your choice, providing an easy and flexible way to simulate sensor data for IoT applications. 

## Installation
Pysor is available on PyPi. You can install it via pip:

```shell
pip install pysor
```

## Quickstart
Here's a quick example showing how to simulate a temperature sensor using Pysor:

```python
from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import TemperatureSensor


if __name__ == '__main__':
    mqtt_client = MqttClient('your.broker.org')

    temperature_sensor = TemperatureSensor(mqtt_client, 'sensor/temperature')

    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)

    try:
        sensor_manager.run()
    except KeyboardInterrupt:
        sensor_manager.stop_all()

```

## Available Sensors
Pysor comes with a variety of pre-built sensor simulations:

- TemperatureSensor
- HumiditySensor
- LightIntensitySensor
- WaterLevelSensor
- PhSensor

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
class MyCustomSensor(BaseSensor):
    
    def generate_data(self) -> Any:
        # Your custom data generation logic here
        ...
```

## SensorManager
The SensorManager class is used to run the sensors. It has a method to add sensors and a method to run the sensors.
```python
sensor_manager = SensorManager()

sensor_manager.add_sensor(temperature_sensor)
sensor_manager.add_sensor(humidity_sensor)
sensor_manager.add_sensor(water_level_sensor)
sensor_manager.add_sensor(light_intensity_sensor)

try:
    sensor_manager.run()
except KeyboardInterrupt:
    sensor_manager.stop_all()
```

## MqttClient
The MqttClient class is used to publish messages to the broker. It uses the Paho MQTT library to communicate with the broker.
```python
mqtt_client = MqttClient('your.broker.org')
```

### License
Pysor is licensed under the MIT License. See the LICENSE file for more details
