import sys

if sys.version_info < (3, 11):
    import toml as tomllib
else:
    import tomllib


class TomlParser:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = None

    def read_config(self) -> None:
        """
        Read the config file or string and store the config in a dictionary

        :return: None
        """

        if self.config_file.endswith('.toml'):
            with open(self.config_file, 'rb') as f:
                self.config = tomllib.load(f)
        else:
            self.config = tomllib.loads(self.config_file)

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
