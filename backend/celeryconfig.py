from decouple import config
from backend.common.utils import get_conn_str

broker_url: str = get_conn_str(
    "amqp",
    config("CABOODLE_RABBITMQ_HOST"),
    config("CABOODLE_RABBITMQ_PORT", cast=int),
    username=config("CABOODLE_RABBITMQ_USER"),
    password=config("CABOODLE_RABBITMQ_PASSWORD")
) 
