from pydantic_settings import BaseSettings, SettingsConfigDict

# import os

# print("CWD:", os.getcwd())
# print("ENV FILE EXISTS:", os.path.exists(".env"))


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
