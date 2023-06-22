import asyncio
import pytest

from unittest.mock import MagicMock, call

from sensor_simulation.sensors import TemperatureSensor


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
    return TemperatureSensor(mqtt_client_mock, "test/temperature", 0.1, current_temperature=20)


@pytest.fixture
def temperature_sensor_with_out_of_range_interval(mqtt_client_mock: MagicMock) -> TemperatureSensor:
    """
    Fixture for the TemperatureSensor instance with interval that should fall out of the range

    :param mqtt_client_mock: MQTT client mock
    :return: TemperatureSensor instance
    """
    return TemperatureSensor(mqtt_client_mock, "test/temperature", 0.1, current_temperature=20, temperature_change=20)


def test_generate_data(temperature_sensor: TemperatureSensor) -> None:
    """
    Test the generate_data method of the TemperatureSensor class

    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    data = temperature_sensor.generate_data()

    assert isinstance(data, float)
    assert temperature_sensor.min_temperature <= data <= temperature_sensor.max_temperature


@pytest.mark.asyncio
async def test_publish_data(mqtt_client_mock: MagicMock, temperature_sensor: TemperatureSensor) -> None:
    """
    Test the publish_data method of the TemperatureSensor class

    :param mqtt_client_mock: Mock of the MQTT client
    :param temperature_sensor: TemperatureSensor instance
    :return: None
    """
    initial_temperature = temperature_sensor.current_temperature

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(temperature_sensor.publish_data())
    await asyncio.sleep(0.2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2
    for publish_call in publish_calls:
        assert float(publish_call[0][1]) > float(initial_temperature)


@pytest.mark.asyncio
async def test_publish_data_with_out_of_range_interval(mqtt_client_mock: MagicMock,
                                                       temperature_sensor_with_out_of_range_interval: TemperatureSensor
                                                       ) -> None:
    """
    Test the publish_data method of the TemperatureSensor class with interval that should fall out of the range.
    Initially, the temperature should be higher than initial_temperature but should not exceed max_temperature.
    Then, the temperature should be lower than initial_temperature but should not fall below min_temperature.

    :param mqtt_client_mock: Mock of the MQTT client
    :param temperature_sensor_with_out_of_range_interval: TemperatureSensor instance
    :return: None
    """
    initial_temperature = temperature_sensor_with_out_of_range_interval.current_temperature
    max_temperature = temperature_sensor_with_out_of_range_interval.max_temperature
    min_temperature = temperature_sensor_with_out_of_range_interval.min_temperature

    mqtt_client_mock.publish.return_value = asyncio.Future()
    mqtt_client_mock.publish.return_value.set_result(None)

    task = asyncio.create_task(temperature_sensor_with_out_of_range_interval.publish_data())
    await asyncio.sleep(0.2)
    task.cancel()

    publish_calls = mqtt_client_mock.publish.call_args_list

    assert len(publish_calls) == 2

    assert float(publish_calls[0][0][1]) > float(initial_temperature)
    assert float(publish_calls[0][0][1]) <= float(max_temperature)

    assert float(publish_calls[1][0][1]) < float(initial_temperature)
    assert float(publish_calls[1][0][1]) >= float(min_temperature)
