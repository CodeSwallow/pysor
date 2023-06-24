from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import (
    TemperatureSensor,
    HumiditySensor,
    WaterLevelSensor,
    LightIntensitySensor
)
from sensor_simulation.config.parsers import TomlParser
from sensor_simulation.config.logger import configure_logger


if __name__ == '__main__':
    mqtt_client = MqttClient('test.mosquitto.org')
    parser = TomlParser('config.toml')

    temperature_sensor = TemperatureSensor(mqtt_client, 'sensor/temperature', interval=1)
    humidity_sensor = HumiditySensor(mqtt_client, 'sensor/humidity', interval=1)
    water_level_sensor = WaterLevelSensor(mqtt_client, 'sensor/water_level', interval=1)
    light_intensity_sensor = LightIntensitySensor(mqtt_client, 'sensor/light_intensity', interval=1)

    sensor_manager = SensorManager()

    # sensor_manager.add_sensor(temperature_sensor)
    # sensor_manager.add_sensor(humidity_sensor)
    sensor_manager.add_sensor(water_level_sensor)
    # sensor_manager.add_sensor(light_intensity_sensor)

    sensor_manager.run()

