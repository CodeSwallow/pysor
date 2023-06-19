import paho.mqtt.client as mqtt


class MqttClient:
    """
    A class used to represent a MQTT client
    """

    def __init__(self, broker_address: str) -> None:
        """
        Constructor of the class

        :param broker_address: IP address of the broker
        """
        self.client = mqtt.Client()
        self.client.connect(broker_address)

    def publish(self, topic: str, message: str) -> None:
        """
        Publish a message to a topic

        :param topic: Name of the topic
        :param message: Message to be published
        :return: None
        """
        self.client.publish(topic, message)

    def subscribe(self, topic: str) -> None:
        """
        Subscribe to a topic

        :param topic: Name of the topic
        :return: None
        """
        self.client.subscribe(topic)
