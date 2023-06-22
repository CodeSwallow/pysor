import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import LightIntensitySensor


@pytest.fixture
def mqtt_client_mock() -> MagicMock:
    """
    Fixture for the MQTT client mock

    :return: MQTT client mock
    """
    return MagicMock()


@pytest.fixture
def light_intensity_sensor(mqtt_client_mock: MagicMock) -> LightIntensitySensor:
    """
    Fixture for the LightIntensitySensor instance

    :param mqtt_client_mock: MQTT client mock
    :return: LightIntensitySensor instance
    """
    return LightIntensitySensor(mqtt_client_mock, "test/light_intensity", 0.5, current_light_intensity=20)


def test_generate_data(light_intensity_sensor: LightIntensitySensor) -> None:
    """
    Test the generate_data method of the LightIntensitySensor class

    :param light_intensity_sensor: LightIntensitySensor instance
    :return: None
    """
    data = light_intensity_sensor.generate_data()

    assert isinstance(data, int)
    assert light_intensity_sensor.min_light_intensity <= data <= light_intensity_sensor.max_light_intensity


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, light_intensity_sensor: LightIntensitySensor) -> None:
    """
    Test the publish_data method of the LightIntensitySensor class

    :param mqtt_client_mock: Mock of the MQTT client
    :param light_intensity_sensor: LightIntensitySensor instance
    :return: None
    """
    initial_light_intensity = light_intensity_sensor.current_light_intensity

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(light_intensity_sensor.publish_data())
    await asyncio.sleep(1)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2
    for publish_call in publish_calls:
        assert float(publish_call[0][1]) > float(initial_light_intensity)
