import ssl

from .mqtt_client import MqttClient
from .azure_token_generator import generate_sas_token


class AzureMqttClient(MqttClient):
    """
    A class used to represent an Azure MQTT client.
    """

    def __init__(self,
                 broker_address: str,
                 device_id: str,
                 shared_access_key: str = None,
                 path_to_root_cert: str = "",
                 cert_path: str = "",
                 key_path: str = "",
                 expiry: int = 3600
                 ) -> None:
        """
        Constructor of the class.

        :param broker_address: IP address of the Azure IoT Hub
        :param device_id: ID of the device in Azure IoT Hub
        :param shared_access_key: Shared access key for the device in Azure IoT Hub
        :param expiry: Token expiry time in seconds. Defaults to 3600 (1 hour)
        """
        super().__init__(broker_address, client_id=device_id, port=8883)
        self.device_id = device_id
        self.shared_access_key = shared_access_key
        self.path_to_root_cert = path_to_root_cert
        self.expiry = expiry
        self.client.username_pw_set(username=self._build_username(), password=self._build_password())
        self.client.tls_set(ca_certs=path_to_root_cert, certfile=cert_path, keyfile=key_path,
                            cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.client.tls_insecure_set(False)

    def _build_username(self) -> str:
        """
        Construct the username required for the Azure MQTT client.

        :return: Username string
        """
        return f"{self.broker_address}/{self.device_id}/api-version=2018-06-30"

    def _build_password(self) -> str:
        """
        Construct the password (SAS token) required for the Azure MQTT client.

        :return: SAS token string
        """
        return generate_sas_token(self.broker_address, self.device_id, self.shared_access_key, self.expiry)

    def username_pw_set(self) -> None:
        """
        Set the username and password for the Azure MQTT client.

        :param username: Username string
        :param password: Password string
        :return: None
        """
        self.client.username_pw_set(
            username=self._build_username(),
            password=self._build_password()
        )

    def connect(self, keepalive: int = 60) -> None:
        """
        Connect to the Azure IoT Hub.

        :param keepalive: Maximum period in seconds allowed between communications with the broker.
        :return: None
        """
        super().connect()
