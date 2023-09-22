import logging


# Configure the logging format
logging.basicConfig(
    level=logging.INFO,  # Desired log level
    format="%(levelname)s | %(asctime)s  - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  # Define the timestamp format
)

# create logger for custom logs
logger = logging.getLogger("__name__")
logging.getLogger("uvicorn").handlers.clear()
