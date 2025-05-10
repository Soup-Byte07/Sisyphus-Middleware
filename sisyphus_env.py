from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class SisyphusSettings(BaseSettings):
    app_name: str = "Sisyphus Middleware"
    version: str = "0.1.0"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
