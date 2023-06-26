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
                 ph_change: float = 0.01,
                 current_ph: float = None
                 ) -> None:
        super().__init__(mqtt_client, topic, interval)
        self.min_ph = min_ph
        self.max_ph = max_ph
        self.ph_change = ph_change

        if current_ph is None:
            current_ph = (max_ph + min_ph) / 2
        self.current_ph = current_ph

    def generate_data(self) -> float:
        """
        Generate data to be published to the broker

        :return: pH Data
        """
        self.current_ph += self.ph_change

        if self.current_ph >= self.max_ph:
            self.current_ph = self.max_ph
            self.ph_change = -abs(self.ph_change)

        if self.current_ph <= self.min_ph:
            self.current_ph = self.min_ph
            self.ph_change = abs(self.ph_change)

        return self.current_ph
