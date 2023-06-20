import logging


def configure_logger(
        log_level: int = logging.INFO,
        log_file: str = "logs/sensor_simulation.log",
        log_format: str = "%(asctime)s - %(levelname)s - %(message)s") -> logging.Logger:
    """
    Configure logger for the application

    :param log_level: Log level
    :param log_file: Log file
    :param log_format: Log format
    :return: Logger object
    """

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger()
