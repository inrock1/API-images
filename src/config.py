# file src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # AWS S3 configuration
    AWS_BUCKET_NAME: str
    AWS_TEST_BUCKET_NAME: str

    RABBITMQ_URL: str

    MB: int = 1024 * 1024  # KB

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
# end of file src/config.py
