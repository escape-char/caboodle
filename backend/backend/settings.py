from typing import Optional
from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    environment: str = config("CABOODLE_ENVIRONMENT")

    # auth jwt settings
    auth_secret_key: str = config("CABOODLE_AUTH_SECRET_KEY")
    auth_iss: str = "caboodle"
    auth_algorithm: str = "HS256"
    auth_expire: int = 60  # in minutes
    auth_retries: int = 4  # max invalid logins until loged
    auth_lockout_exp: int = 60  # lockout time in minutes

    # postgres settings
    postgres_protocol: str = "postgresql"
    postgres_host: str = config(
        "CABOODLE_POSTGRES_HOST",
        default="localhost"
    )
    postgres_port: int = config(
        "CABOODLE_POSTGRES_PORT",
        default=5432,
        cast=int
    )
    postgres_username: str = config("CABOODLE_POSTGRES_USER")
    postgres_password: str = config("CABOODLE_POSTGRES_PASSWORD")
    postgres_db: str = config(
        "CABOODLE_POSTGRES_DB",
        default="localhost"
    )

    # redis settings
    redis_protocol: str = "redis"
    redis_host: str = config("CABOODLE_REDIS_HOST", default="localhost")
    redis_port: int = config("CABOODLE_REDIS_PORT", default=6379, cast=int)
    redis_db: int = config("CABOODLE_REDIS_DB", default=0, cast=int)
    redis_ssl: bool = config("CABOODLE_REDIS_SSL", default=False, cast=bool)
    redis_password: Optional[str] = config(
        "CABOODLE_REDIS_PASSWORD",
        default=None
    )

    # default admin created for the app
    default_admin_username: str = config('CABOODLE_DEFAULT_ADMIN_USERNAME')
    default_admin_password: str = config('CABOODLE_DEFAULT_ADMIN_PASSWORD')
    default_admin_email: str = config('CABOODLE_DEFAULT_ADMIN_EMAIL')
    default_admin_name: str = config('CABOODLE_DEFAULT_ADMIN_NAME', default="")


settings: Settings = Settings()
