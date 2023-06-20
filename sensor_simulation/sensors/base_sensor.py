import time
import asyncio

from abc import ABC
from abc import abstractmethod
from typing import Any

from sensor_simulation.mqtt_client import MqttClient


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
    def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        pass


class BaseSensor(ISensor):
    """
    Base sensor class for all sensors
    """

    def __init__(self, mqtt_client: MqttClient, topic: str, interval: int):
        self.mqtt_client = mqtt_client
        self.topic = topic
        self.interval = interval

    @abstractmethod
    def generate_data(self) -> Any:
        """
        Generate data to be published to the broker

        :return: Data
        """
        pass

    async def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        await self.publish_data()

    async def publish_data(self) -> None:
        """
        Publish data to the broker with the given interval

        :return: None
        """
        while True:
            data = self.generate_data()
            message = str(data)
            print(f"Publishing message: {message}")
            print(f'Client: {self.mqtt_client}')
            print(f'Topic: {self.topic}')
            await self.mqtt_client.publish(self.topic, message)
            await asyncio.sleep(self.interval)
