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

    def start_publishing(self) -> None:
        """
        Start publishing messages to the broker with the given interval

        :return: None
        """
        for sensor in self.sensors:
            sensor.start_publishing()
