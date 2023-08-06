import logging

# reduce log level
logging.getLogger("pika").setLevel(logging.WARNING)

# Create a custom logger
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
