import paho.mqtt.client as mqtt


class MqttClient:
    """
    A class used to represent a MQTT client
    """

    def __init__(self,
                 broker_address: str,
                 port: int = 1883,
                 keepalive: int = 60,
                 bind_address: str = "",
                 bind_port: int = 0,
                 ) -> None:
        """
        Constructor of the class

        :param broker_address: IP address of the broker
        :param port: Port of the broker
        :param keepalive: Keepalive time
        :param bind_address: Bind address
        :param bind_port: Bind port
        """
        self.client = mqtt.Client()
        self.client.connect(
            broker_address,
            port=port,
            keepalive=keepalive,
            bind_address=bind_address,
            bind_port=bind_port
        )

    async def publish(self, topic: str, message: str) -> None:
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
