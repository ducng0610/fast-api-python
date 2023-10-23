"""File contains the app configurations"""
import logging
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    TESTING: bool = False

    # Loads the dotenv file. Including this is necessary to get
    # pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DefaultConfig(BaseConfig):
    DATABASE_URI: Optional[str] = None


class DevConfig(DefaultConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(DefaultConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(DefaultConfig):
    DATABASE_URI: Optional[str] = "sqlite:///test.db"
    TESTING: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str) -> BaseConfig:
    log.info("Loading config for FastAPI app...")
    log.info("ENV: %s" % env_state)
    configs = {
        "dev": DevConfig,
        "prod": ProdConfig,
        "test": TestConfig,
    }
    config_class = configs.get(env_state, DevConfig)
    app_config = config_class()
    app_config.ENV_STATE = env_state
    return app_config


app_config = get_config(BaseConfig().ENV_STATE)
