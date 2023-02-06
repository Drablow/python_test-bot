import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("RAPID_API_KEY", None)
    host_api: StrictStr = os.getenv("RAPID_API_HOST", None)


I18N_DOMAIN = 'hotelbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
