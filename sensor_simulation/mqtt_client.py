import asyncio

from ssl import SSLContext

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
        self.broker_address = broker_address
        self.port = port
        self.keepalive = keepalive
        self.bind_address = bind_address
        self.bind_port = bind_port

    async def publish(self, topic: str, message: str) -> None:
        """
        Publish a message to a topic

        :param topic: Name of the topic
        :param message: Message to be published
        :return: None
        """
        # self.client.publish(topic, message)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.publish, topic, message)

    def subscribe(self, topic: str) -> None:
        """
        Subscribe to a topic

        :param topic: Name of the topic
        :return: None
        """
        self.client.subscribe(topic)

    def tls_set_context(self, context: SSLContext) -> None:
        """
        Set the TLS context

        :param context: TLS context
        :return: None
        """
        self.client.tls_set_context(context)

    def connect(self) -> None:
        """
        Connect to the broker

        :return: None
        """
        self.client.connect(self.broker_address, self.port, self.keepalive, self.bind_address, self.bind_port)

    def loop_start(self) -> None:
        """
        Start the loop

        :return: None
        """
        self.client.loop_start()
