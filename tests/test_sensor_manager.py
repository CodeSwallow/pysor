import asyncio
import pytest
from unittest.mock import MagicMock, call
from sensor_simulation.sensors import TemperatureSensor
from sensor_simulation.sensor_manager import SensorManager


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    """
    Fixture for the MQTT client mock

    :return: MQTT client mock
    """
    return MagicMock()


@pytest.fixture
def temperature_sensor(mqtt_client_mock: MagicMock) -> TemperatureSensor:
    """
    Fixture for the TemperatureSensor instance

    :param mqtt_client_mock: MQTT client mock
    :return: TemperatureSensor instance
    """
    return TemperatureSensor(mqtt_client_mock, "test/temperature", 1, 100, 100)


def test_add_sensor(temperature_sensor: TemperatureSensor) -> None:
    """
    Test the add_sensor method of the SensorManager class

    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)

    assert len(sensor_manager.sensors) == 1
    assert sensor_manager.sensors[0] == temperature_sensor


@pytest.mark.asyncio
async def test_start_publishing(mqtt_client_mock: MagicMock, temperature_sensor: TemperatureSensor) -> None:
    """
    Test the start_publishing method of the SensorManager class

    :param mqtt_client_mock: Mock of the MQTT client
    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    publish_task = asyncio.create_task(sensor_manager.start_publishing())
    await asyncio.sleep(1)
    publish_task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list
    max_temperature = float(temperature_sensor.max_temperature)
    expected_topic_call = call("test/temperature", str(max_temperature))

    assert expected_topic_call in publish_calls
    assert len(publish_calls) == 1
