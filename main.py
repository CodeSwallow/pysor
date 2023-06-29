import ssl

from ssl import SSLContext

from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import (
    TemperatureSensor,
    HumiditySensor,
    WaterLevelSensor,
    LightIntensitySensor,
    PhSensor
)
from sensor_simulation.config.parsers import TomlParser
from sensor_simulation.config.logger import configure_logger


def ssl_alpn(alpn_context: str, ca_path: str, cert_path: str, key_path: str) -> SSLContext:
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([alpn_context])
        ssl_context.load_verify_locations(cafile=ca_path)
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

        return ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e


if __name__ == '__main__':
    parser = TomlParser('aws_config.toml')
    parser.read_config()
    general_config = parser.get_general_config()

    mqtt_client = MqttClient(general_config['broker_address'], general_config['broker_port'])
    context = ssl_alpn(
        general_config['alpn_context'],
        general_config['ca_path'],
        general_config['cert_path'],
        general_config['key_path']
    )
    mqtt_client.tls_set_context(context=context)
    mqtt_client.connect()
    mqtt_client.loop_start()

    temperature_sensor = TemperatureSensor(mqtt_client, 'sensor/temperature')
    humidity_sensor = HumiditySensor(mqtt_client, 'sensor/humidity')
    water_level_sensor = WaterLevelSensor(mqtt_client, 'sensor/water_level')
    light_intensity_sensor = LightIntensitySensor(mqtt_client, 'sensor/light_intensity')
    ph_sensor = PhSensor(mqtt_client, 'sensor/ph')

    sensor_manager = SensorManager()

    sensor_manager.add_sensor(temperature_sensor)
    sensor_manager.add_sensor(humidity_sensor)
    sensor_manager.add_sensor(water_level_sensor)
    sensor_manager.add_sensor(light_intensity_sensor)
    sensor_manager.add_sensor(ph_sensor)

    sensor_manager.run()

