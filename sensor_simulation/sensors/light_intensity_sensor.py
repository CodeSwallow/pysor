import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class LightIntensitySensor(BaseSensor):
    """
    Light intensity sensor class.
    Min and max light intensity values are in lux.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: int = 120,
                 min_light_intensity: int = 0,
                 max_light_intensity: int = 10000,
                 light_intensity_change: int = 25,
                 current_light_intensity: int = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_light_intensity = min_light_intensity
        self.max_light_intensity = max_light_intensity
        self.light_intensity_change = light_intensity_change

        if current_light_intensity is None:
            current_light_intensity = (max_light_intensity + min_light_intensity) // 2
        self.current_light_intensity = current_light_intensity

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        self.current_light_intensity += self.light_intensity_change

        if self.current_light_intensity >= self.max_light_intensity:
            self.current_light_intensity = self.max_light_intensity
            self.light_intensity_change = -abs(self.light_intensity_change)

        if self.current_light_intensity <= self.min_light_intensity:
            self.current_light_intensity = self.min_light_intensity
            self.light_intensity_change = abs(self.light_intensity_change)

        return self.current_light_intensity
