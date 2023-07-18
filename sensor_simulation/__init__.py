from .config.logger import configure_logger
from .sensor_manager import SensorManager

__all__ = [
    "SensorManager"
]


configure_logger()
