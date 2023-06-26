import random
import asyncio


from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class PhSensor(BaseSensor):
    """
    pH sensor class.
    Min and max pH values range from 0 to 14.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: float = 10.0,
                 min_ph: float = 0.0,
                 max_ph: float = 14.0,
                 temperature_change: float = 0.01,
                 current_temperature: float = 7.0
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_ph = min_ph
        self.max_ph = max_ph

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: pH Data
        """
        return random.uniform(self.min_ph, self.max_ph)
