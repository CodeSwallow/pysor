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
    """
    Function to create a SSL context with the given parameters.

    :param alpn_context: The Application-Layer Protocol Negotiation context
    :param ca_path: The path to the CA certificate
    :param cert_path: The path to your client's certificate
    :param key_path: The path to your client's private key
    :return: The SSL context as a SSLContext object
    """
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
    # This example shows how to use the sensor simulation library.
    # The library can be used with any MQTT broker, but this example uses AWS IoT Core.
    # TomlParser is not necessary, but it is a good way to store your configuration.

    parser = TomlParser('aws_config.toml')  # Parse the config file, or use your data directly instead of the parser
    parser.read_config()
    general_config = parser.get_general_config()

    mqtt_client = MqttClient(general_config['broker_address'], general_config['broker_port'])  # Create a MQTT client
    context = ssl_alpn(
        general_config['alpn_context'],  # Create a SSL context
        general_config['ca_path'],  # The path to the CA certificate
        general_config['cert_path'],  # The path to the certificate
        general_config['key_path']  # The path to the private key
    )
    mqtt_client.tls_set_context(context=context)  # Set the SSL context
    mqtt_client.connect()  # Connect to the broker
    mqtt_client.loop_start()  # Start the MQTT loop

    temperature_sensor = TemperatureSensor(mqtt_client, 'sensor/temperature', 1)
    humidity_sensor = HumiditySensor(mqtt_client, 'sensor/humidity', 2)
    water_level_sensor = WaterLevelSensor(mqtt_client, 'sensor/water_level', 3)
    light_intensity_sensor = LightIntensitySensor(mqtt_client, 'sensor/light_intensity', 4)
    ph_sensor = PhSensor(mqtt_client, 'sensor/ph', 5)

    sensor_manager = SensorManager()

    sensor_manager.add_sensor(temperature_sensor)
    sensor_manager.add_sensor(humidity_sensor)
    sensor_manager.add_sensor(water_level_sensor)
    sensor_manager.add_sensor(light_intensity_sensor)
    sensor_manager.add_sensor(ph_sensor)

    try:
        sensor_manager.run()  # Start the sensor manager
    except KeyboardInterrupt:
        sensor_manager.stop_all()  # Stop all sensors after a keyboard interrupt
