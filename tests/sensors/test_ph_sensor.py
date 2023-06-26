import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import PhSensor


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    """
    Fixture for the MQTT client mock

    :return: MQTT client mock
    """
    return MagicMock()


@pytest.fixture
def ph_sensor(mqtt_client_mock: MagicMock) -> PhSensor:
    """
    Fixture for the PhSensor instance

    :param mqtt_client_mock: MQTT client mock
    :return: PhSensor instance
    """
    return PhSensor(mqtt_client_mock, "test/ph", 0.1, current_ph=6.0)


def test_generate_data(ph_sensor: PhSensor) -> None:
    """
    Test the generate_data method of the PhSensor class

    :param ph_sensor: PhSensor instance
    :return: None
    """
    data = ph_sensor.generate_data()

    assert isinstance(data, float)
    assert ph_sensor.min_ph <= data <= ph_sensor.max_ph


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, ph_sensor: PhSensor) -> None:
    """
    Test the publish_data method of the PhSensor class

    :param mqtt_client_mock: Mock of the MQTT client
    :param ph_sensor: PhSensor instance
    :return: None
    """
    initial_ph = ph_sensor.current_ph

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(ph_sensor.publish_data())
    await asyncio.sleep(0.2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2
    for publish_call in publish_calls:
        assert float(publish_call[0][1]) > float(initial_ph)
