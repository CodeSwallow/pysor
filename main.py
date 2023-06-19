from sensor_simulation import MqttClient
from sensor_simulation.sensors import TemperatureSensor


if __name__ == '__main__':
    mqtt_client = MqttClient("test.mosquitto.org")
    temperature_sensor = TemperatureSensor(mqtt_client, "temperature", 1, 10, 30)
    temperature_sensor.start_publishing()

