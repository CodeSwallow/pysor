import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class HumiditySensor(BaseSensor):
    """
    Humidity sensor class.
    Min and max humidity values are in percentage.
    """

    def __init__(self,
                 mqtt_client: MqttClient,
                 topic: str,
                 interval: int = 120,
                 min_humidity: int = 30,
                 max_humidity: int = 80,
                 humidity_change: float = 1.0,
                 current_humidity: float = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity
        self.humidity_change = humidity_change

        if current_humidity is None:
            current_humidity = (max_humidity + min_humidity) / 2
        self.current_humidity = current_humidity

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: Data
        """
        self.current_humidity += self.humidity_change

        if self.current_humidity >= self.max_humidity:
            self.current_humidity = self.max_humidity
            self.humidity_change = -abs(self.humidity_change)

        if self.current_humidity <= self.min_humidity:
            self.current_humidity = self.min_humidity
            self.humidity_change = abs(self.humidity_change)

        return self.current_humidity
