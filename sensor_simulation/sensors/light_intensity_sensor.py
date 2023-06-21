import random
import asyncio


from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class LightIntensitySensor(BaseSensor):
    """
    Light intensity sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: int, min_light_intensity: int, max_light_intensity: int) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_light_intensity = min_light_intensity
        self.max_light_intensity = max_light_intensity

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        return random.uniform(self.min_light_intensity, self.max_light_intensity)
