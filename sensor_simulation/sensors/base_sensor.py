import time

from sensor_simulation.mqtt_client import MqttClient


class BaseSensor:
    """
    Base sensor class
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: float) -> None:
        """
        Constructor of the class

        :param mqtt_client: MQTT client
        :param topic: Name of the topic
        :param interval: Interval of publishing messages
        """
        self.mqtt_client = mqtt_client
        self.topic = topic
        self.interval = interval

    def generate_data(self) -> str:
        """
        Generate data to be published to the broker

        :return: Data
        """
        raise NotImplementedError("Subclass must implement generate_data() method")

    def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        while True:
            data = self.generate_data()
            self.mqtt_client.publish(self.topic, data)
            time.sleep(self.interval)
