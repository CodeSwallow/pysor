import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import HumiditySensor


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    """
    Fixture for the MQTT client mock

    :return: MQTT client mock
    """
    return MagicMock()


@pytest.fixture
def humidity_sensor(mqtt_client_mock: MagicMock) -> HumiditySensor:
    """
    Fixture for the HumiditySensor instance

    :param mqtt_client_mock: MQTT client mock
    :return: HumiditySensor instance
    """
    return HumiditySensor(mqtt_client_mock, "test/humidity", 0.1)


def test_generate_data(humidity_sensor: HumiditySensor) -> None:
    """
    Test the generate_data method of the HumiditySensor class

    :param humidity_sensor: HumiditySensor instance
    :return: None
    """
    data = humidity_sensor.generate_data()

    assert isinstance(data, float)
    assert humidity_sensor.min_humidity <= data <= humidity_sensor.max_humidity


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, humidity_sensor: HumiditySensor) -> None:
    """
    Test the publish_data method of the HumiditySensor class

    :param mqtt_client_mock: Mock of the MQTT client
    :param humidity_sensor: HumiditySensor instance
    :return: None
    """
    initial_humidity = humidity_sensor.current_humidity

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(humidity_sensor.publish_data())
    await asyncio.sleep(0.2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2
    for publish_call in publish_calls:
        assert float(publish_call[0][1]) > float(initial_humidity)
