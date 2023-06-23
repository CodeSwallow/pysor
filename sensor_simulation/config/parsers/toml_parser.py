import tomllib


class TomlParser:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = None

    def read_config(self) -> None:
        """
        Read the config file and store the config in a dictionary

        :return: None
        """
        with open(self.config_file, "rb") as config_file:
            self.config = tomllib.load(config_file)

    def get_general_config(self) -> dict:
        """
        Get the general config. E.g. broker address, port, etc.

        :return: General config dictionary
        """
        return self.config["General"]

    def get_sensor_config(self, sensor_name: str) -> dict:
        """
        Get the config for a specific sensor

        :param sensor_name: Name of the sensor. E.g. "WaterLevelSensor"
        :return: Sensor config dictionary
        """
        return self.config["Sensors"][sensor_name]
