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
                 min_ph: float = 5.5,
                 max_ph: float = 6.5,
                 temperature_change: float = 0.01,
                 current_temperature: float = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_ph = min_ph
        self.max_ph = max_ph
        self.temperature_change = temperature_change

        if current_temperature is None:
            current_temperature = (max_ph + min_ph) / 2
        self.current_temperature = current_temperature

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: pH Data
        """
        self.current_temperature += self.temperature_change

        if self.current_temperature >= self.max_ph:
            self.current_temperature = self.max_ph
            self.temperature_change = -abs(self.temperature_change)

        if self.current_temperature <= self.min_ph:
            self.current_temperature = self.min_ph
            self.temperature_change = abs(self.temperature_change)

        return self.current_temperature
