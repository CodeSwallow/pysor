import random
import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class HumiditySensor(BaseSensor):
    """
    Humidity sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: int, min_humidity: int, max_humidity: int) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        print("Humidity sensor")
        return random.uniform(self.min_humidity, self.max_humidity)
