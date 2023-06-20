import tomllib


class TomlParser:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = None

    def read_config(self) -> None:
        with open(self.config_file, "rb") as config_file:
            self.config = tomllib.load(config_file)

    def get_general_config(self) -> dict:
        return self.config["General"]

    def get_sensor_config(self, sensor_name: str) -> dict:
        return self.config["Sensors"][sensor_name]
