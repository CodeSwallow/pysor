import asyncio
import logging

from abc import ABC
from abc import abstractmethod
from typing import Any

from sensor_simulation.clients import MqttClient


class ISensor(ABC):
    """
    Interface for sensors
    """

    @abstractmethod
    def generate_data(self) -> Any:
        """
        Generate data to be published to the broker

        :return: Data
        """
        pass

    @abstractmethod
    def publish_data(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        pass


class BaseSensor(ISensor):
    """
    Base sensor class for all sensors
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: float) -> None:
        self.mqtt_client = mqtt_client
        self.topic = topic
        self.interval = interval
        self.running = True
        self.done = asyncio.Future()

    @abstractmethod
    def generate_data(self) -> Any:
        """
        Generate data to be published to the broker

        :return: Data
        """
        pass

    async def publish_data(self) -> None:
        """
        Publish data to the broker with the given interval

        :return: None
        """
        while self.running:
            data = self.generate_data()
            message = str(data)
            logging.info(f"Publishing message: {message} to topic: {self.topic}")
            await self.mqtt_client.publish(self.topic, message)
            await asyncio.sleep(self.interval)
        self.done.set_result(True)

    def stop(self) -> None:
        """
        Stop publishing data to the broker

        :return: None
        """
        self.running = False
