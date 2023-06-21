import random
import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class WaterLevelSensor(BaseSensor):
    """
    Water level sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: int, min_water_level: int, max_water_level: int) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_water_level = min_water_level
        self.max_water_level = max_water_level

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        return random.uniform(self.min_water_level, self.max_water_level)
