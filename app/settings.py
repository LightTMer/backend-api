from pydantic_settings import BaseSettings, SettingsConfigDict
from neomodel import config


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    ACCESS_TOKEN: str
    NEO4J_URI: str


app_settings = ApplicationSettings()
config.DATABASE_URL = app_settings.NEO4J_URI
