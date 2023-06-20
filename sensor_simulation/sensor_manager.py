import asyncio

from sensor_simulation.mqtt_client import MqttClient
from sensor_simulation.sensors.base_sensor import BaseSensor


class SensorManager:
    """
    The SensorManager class is responsible for managing the sensors in the simulation
    environment when there are multiple sensors.
    """

    def __init__(self) -> None:
        """
        Constructor of the class

        :param sensors: List of sensors
        """
        self.sensors = []

    def add_sensor(self, sensor: BaseSensor) -> None:
        """
        Add a sensor to the list of sensors

        :param sensor: Sensor to be added
        :return: None
        """
        self.sensors.append(sensor)

    async def gather_tasks(self) -> None:
        """
        Gather all tasks that will be performed by the sensors

        :return: None
        """
        while True:
            await asyncio.gather(*(sensor.publish_data() for sensor in self.sensors))

    async def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        await self.gather_tasks()

    def run(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_publishing())
