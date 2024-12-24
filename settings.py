from pydantic_settings import BaseSettings
from pydantic.types import SecretStr
import requests

class Settings(BaseSettings):
    token: SecretStr
    zone_id: str
    ruleset: str
    cf_api_url: str