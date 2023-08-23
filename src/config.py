# file src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # AWS S3 configuration
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str
    AWS_TEST_BUCKET_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# end of file src/config.py