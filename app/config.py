from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_KEY: str
    API_KEY_NAME: str = 'access_token'
    COOKIE_DOMAIN: str = 'localtest.me'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
