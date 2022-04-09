import logging
import os
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = os.getenv('APP_NAME', 'my-app')
    app_version: str = os.getenv('APP_VERSION', '0.0.1')
    
    app_description: str

    redis_host: str = os.getenv('REDIS_HOST', '')
    redis_queue: str = os.getenv('REDIS_QUEUE', '')

    client_max_tries: int = int(os.getenv('CLIENT_MAX_TRIES', '100'))
    client_sleep: float = float(os.getenv('CLIENT_SLEEP', '0.25'))

    image_width: int = int(os.getenv('IMAGE_WIDTH', '224'))
    image_height: int = int(os.getenv('IMAGE_HEIGHT', '224'))

settings = Settings(
    app_description = (Path(__file__).parent.parent / 'static/documentation.md').read_text(encoding='utf-8')
)

# configure project-specific logger
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt='%(levelname)-8s [%(module)s:%(funcName)s] %(message)s'
    )
)
logger = logging.getLogger(settings.app_name)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
