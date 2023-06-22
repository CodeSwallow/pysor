import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import WaterLevelSensor


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    """
    Fixture for the MQTT client mock

    :return: MQTT client mock
    """
    return MagicMock()


@pytest.fixture
def water_level_sensor(mqtt_client_mock: MagicMock) -> WaterLevelSensor:
    """
    Fixture for the WaterLevelSensor instance

    :param mqtt_client_mock: MQTT client mock
    :return: WaterLevelSensor instance
    """
    return WaterLevelSensor(mqtt_client_mock, "test/water_level", 0.1, current_water_level=50)


def test_generate_data(water_level_sensor: WaterLevelSensor) -> None:
    """
    Test the generate_data method of the WaterLevelSensor class

    :param water_level_sensor: WaterLevelSensor instance
    :return: None
    """
    data = water_level_sensor.generate_data()

    assert isinstance(data, float)
    assert water_level_sensor.min_water_level <= data <= water_level_sensor.max_water_level


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, water_level_sensor: WaterLevelSensor) -> None:
    """
    Test the publish_data method of the WaterLevelSensor class.
    Water level should decrease.

    :param mqtt_client_mock:
    :param water_level_sensor:
    :return:
    """
    initial_water_level = water_level_sensor.current_water_level

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(water_level_sensor.publish_data())
    await asyncio.sleep(0.2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2
    for publish_call in publish_calls:
        assert float(publish_call[0][1]) < float(initial_water_level)
