import pytest

from sensor_simulation.config.parsers import TomlParser


@pytest.fixture
def toml_parser() -> TomlParser:
    """
    Fixture for the TomlParser instance

    :return: TomlParser instance
    """
    config_file = """
    [General]
    broker_address = "test.mosquitto.org"
    broker_port = 1883
    client_id = "sensor_simulation"
    keep_alive = 60

    [Sensors]

    [Sensors.TemperatureSensor]
    topic = "temperature"
    interval = 1
    min_temperature = 10
    max_temperature = 30
    """
    return TomlParser(config_file)


def test_read_config(toml_parser: TomlParser) -> None:
    """
    Test the read_config method of the TomlParser class

    :param toml_parser: TomlParser instance
    :return: None
    """
    toml_parser.read_config()

    assert toml_parser.config is not None
    assert isinstance(toml_parser.config, dict)


def test_get_general_config(toml_parser: TomlParser) -> None:
    """
    Test the get_general_config method of the TomlParser class

    :param toml_parser: TomlParser instance
    :return: None
    """
    toml_parser.read_config()
    config = toml_parser.get_general_config()

    assert config is not None
    assert isinstance(config, dict)
    assert config['broker_address'] == 'test.mosquitto.org'
    assert config['broker_port'] == 1883
    assert config['client_id'] == 'sensor_simulation'


def test_get_sensors_config(toml_parser: TomlParser) -> None:
    """
    Test the get_sensors_config method of the TomlParser class

    :param toml_parser: TomlParser instance
    :return: None
    """
    toml_parser.read_config()
    config = toml_parser.get_sensor_config("TemperatureSensor")

    assert config is not None
    assert isinstance(config, dict)
    assert config['topic'] == 'temperature'
    assert config['interval'] == 1
    assert config['min_temperature'] == 10
    assert config['max_temperature'] == 30
