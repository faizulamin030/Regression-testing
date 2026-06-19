import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerFactory:
    def __init__(self, logs_dir: Path) -> None:
        self.logs_dir = logs_dir
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self._configured = False

    def configure(self) -> None:
        if self._configured:
            return

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        logger_map = {
            "framework": "framework.log",
            "request": "request.log",
            "response": "response.log",
            "validation": "validation.log",
            "error": "error.log",
        }

        for logger_name, file_name in logger_map.items():
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            logger.propagate = False
            logger.handlers.clear()

            file_handler = RotatingFileHandler(
                self.logs_dir / file_name,
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        self._configured = True

    @staticmethod
    def get(name: str) -> logging.Logger:
        return logging.getLogger(name)
