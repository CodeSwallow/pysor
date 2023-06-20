import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import TemperatureSensor


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    return MagicMock()


@pytest.fixture
def temperature_sensor(mqtt_client_mock: MagicMock) -> TemperatureSensor:
    return TemperatureSensor(mqtt_client_mock, "test/temperature", 1, 100, 100)


def test_generate_data(temperature_sensor: TemperatureSensor) -> None:
    """
    Test the generate_data method of the TemperatureSensor class

    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    data = temperature_sensor.generate_data()

    assert isinstance(data, float)
    assert 0 <= data <= 100


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, temperature_sensor: TemperatureSensor) -> None:
    """
    Test the publish_data method of the TemperatureSensor class

    :param mqtt_client_mock: Mock of the MQTT client
    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(temperature_sensor.publish_data())
    await asyncio.sleep(2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list
    max_temperature = float(temperature_sensor.max_temperature)
    expected_topic_call = call("test/temperature", str(max_temperature))

    assert expected_topic_call in publish_calls
    assert len(publish_calls) == 2
    assert all(call_args == expected_topic_call for call_args in publish_calls)
