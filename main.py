from sensor_simulation import MqttClient, SensorManager
from sensor_simulation.sensors import TemperatureSensor, HumiditySensor


if __name__ == '__main__':
    mqtt_client = MqttClient("test.mosquitto.org")
    temperature_sensor = TemperatureSensor(mqtt_client, "temperature", 1, 10, 30)
    humidity_sensor = HumiditySensor(mqtt_client, "humidity", 1, 10, 30)

    sensor_manager = SensorManager()
    sensor_manager.add_sensor(temperature_sensor)
    sensor_manager.add_sensor(humidity_sensor)
    sensor_manager.run()

