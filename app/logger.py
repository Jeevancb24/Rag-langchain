from loguru import logger

logger.add("debug.log", rotation="10MB", level="DEBUG", format="{time} {level} {message}")
