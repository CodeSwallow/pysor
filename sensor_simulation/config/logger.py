import logging


def configure_logger(
        log_level: int = logging.INFO,
        log_file: str = "logs/sensor_simulation.log",
        log_format: str = "%(asctime)s - %(levelname)s - %(message)s") -> logging.Logger:
    """
    Configure logger for the application

    :param log_level: Log level (default: INFO)
    :param log_file: Log file (default: logs/sensor_simulation.log)
    :param log_format: Log format (default: %(asctime)s - %(levelname)s - %(message)s)
    :return: Logger object
    """

    handlers = [logging.StreamHandler()]

    # if log_file:
    #     handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )

    return logging.getLogger()
