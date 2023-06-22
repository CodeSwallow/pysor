import random
import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    """
    Temperature sensor class.
    Min and max temperature values are in Celsius.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: float = 10.0,
                 min_temperature: int = 15,
                 max_temperature: int = 30,
                 temperature_change: float = 0.1,
                 current_temperature: float = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.temperature_change = temperature_change

        if current_temperature is None:
            current_temperature = (max_temperature + min_temperature) / 2
        self.current_temperature = current_temperature

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        self.current_temperature += self.temperature_change

        if self.current_temperature >= self.max_temperature:
            self.current_temperature = self.max_temperature - random.uniform(0, 1)
            self.temperature_change = -abs(self.temperature_change)

        if self.current_temperature <= self.min_temperature:
            self.current_temperature = self.min_temperature + random.uniform(0, 1)
            self.temperature_change = abs(self.temperature_change)

        return self.current_temperature
