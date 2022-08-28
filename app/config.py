from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = 'localhost'
    database_port: str = 'postgres'
    database_password: str
    database_username: str
    database_name: str
    algorithm: str
    secret_key: str = '1234abcd'
    access_token_expiration_minutes: int

    class Config:
        env_file = "app/env.txt"

settings = Settings()