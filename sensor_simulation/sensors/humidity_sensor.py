import random

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class HumiditySensor(BaseSensor):
    """
    Humidity sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: float, min_humidity: float, max_humidity: float) -> None:
        """
        Constructor of the class

        :param mqtt_client: MQTT client
        :param topic: Name of the topic
        :param interval: Interval of publishing messages
        """
        super().__init__(mqtt_client, topic, interval)
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity

    def generate_data(self) -> str:
        """
        Generate data to be published to the broker

        :return: Data
        """
        return str(random.uniform(self.min_humidity, self.max_humidity))
