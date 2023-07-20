import ssl

from .mqtt_client import MqttClient


class AWSMqttClient(MqttClient):
    """
    A class used to represent a MQTT client for use with AWS IoT Core.
    """

    def __init__(self,
                 broker_address: str,
                 port: int = 1883,
                 keepalive: int = 60,
                 bind_address: str = "",
                 bind_port: int = 0,
                 alpn_context: str = "x-amzn-mqtt-ca",
                 ca_path: str = None,
                 cert_path: str = None,
                 key_path: str = None,
                 ) -> None:
        """
        Constructor of the class.
        """
        super().__init__(broker_address, port, keepalive, bind_address, bind_port)
        self.alpn_context = alpn_context
        self.ca_path = ca_path
        self.cert_path = cert_path
        self.key_path = key_path

    def _set_ssl_alpn(self) -> ssl.SSLContext:
        """
        Set the SSL context for the client.

        :return: SSL context
        """
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([self.alpn_context])
        ssl_context.load_verify_locations(cafile=self.ca_path)
        ssl_context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
        return ssl_context

    def connect(self) -> None:
        """
        Connect to the broker.

        :return: None
        """
        self.client.tls_set_context(self._set_ssl_alpn())
        super().connect()
