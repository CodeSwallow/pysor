import random
import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    """
    Temperature sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: int, min_temperature: int, max_temperature: int) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        return random.uniform(self.min_temperature, self.max_temperature)
