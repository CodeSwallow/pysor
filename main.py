from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import TemperatureSensor, HumiditySensor
from sensor_simulation.config.parsers import TomlParser
from sensor_simulation.config.logger import configure_logger


if __name__ == '__main__':
    config_file = 'config.toml'
    parser = TomlParser(config_file)
    parser.read_config()

    general_config = parser.get_general_config()
    temperature_config = parser.get_sensor_config("TemperatureSensor")
    humidity_config = parser.get_sensor_config("HumiditySensor")

    configure_logger(
        general_config["log_level"],
        general_config["log_file"]
    )

    mqtt_client = MqttClient(general_config["broker_address"])

    temperature_sensor = TemperatureSensor(
        mqtt_client,
        temperature_config["topic"],
        temperature_config["interval"],
        temperature_config["min_temperature"],
        temperature_config["max_temperature"]
    )

    humidity_sensor = HumiditySensor(
        mqtt_client,
        humidity_config["topic"],
        humidity_config["interval"],
        humidity_config["min_humidity"],
        humidity_config["max_humidity"]
    )

    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)
    sensor_manager.add_sensor(humidity_sensor)
    sensor_manager.run()

