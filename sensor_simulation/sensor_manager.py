import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class SensorManager:
    """
    The SensorManager class is responsible for managing the sensors in the simulation
    environment when there are one or more sensors.
    """

    def __init__(self) -> None:
        """
        Constructor of the class
        Create an empty list of sensors to be added later
        """
        self.sensors = []
        self.loop = asyncio.get_event_loop()

    def add_sensor(self, sensor: BaseSensor) -> None:
        """
        Add a sensor to the list of sensors

        :param sensor: Sensor to be added
        :return: None
        """
        self.sensors.append(sensor)

    async def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        await asyncio.gather(*(sensor.publish_data() for sensor in self.sensors))
        # await asyncio.wait([sensor.publish_data() for sensor in self.sensors])

    def run(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        self.loop.run_until_complete(self.start_publishing())

    def stop_all(self) -> None:
        """
        Stop publishing data to the broker

        :return: None
        """
        for sensor in self.sensors:
            sensor.stop()
        self.loop.run_until_complete(asyncio.gather(*(sensor.done for sensor in self.sensors)))
        self.loop.stop()

