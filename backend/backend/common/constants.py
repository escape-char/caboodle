from typing import Final

ERROR_DATABASE: Final[str] = (
    "An internal server error occured while communicating to our database"
)


ENV_DEVELOPMENT: Final[str] = "development"
ENV_PRODUCTION: Final[str] = "production"


SESSION_KEY: Final[str] = "sesson-%s-%s"  # session-<token>-<ip>
SESSION_EXPIRE: Final[int] = 60*60  # 1 hour
