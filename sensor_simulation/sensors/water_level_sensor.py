import random
import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class WaterLevelSensor(BaseSensor):
    """
    Water level sensor class.
    Min and max water level values are in cm.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: float = 300.0,
                 min_water_level: int = 30,
                 max_water_level: int = 100,
                 water_level_change: int = -0.01,
                 current_water_level: int = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_water_level = min_water_level
        self.max_water_level = max_water_level
        self.water_level_change = water_level_change

        if current_water_level is None:
            current_water_level = (max_water_level + min_water_level) / 2
        self.current_water_level = current_water_level

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        self.current_water_level += self.water_level_change

        if self.current_water_level <= self.min_water_level:
            self.current_water_level = self.max_water_level

        return self.current_water_level
