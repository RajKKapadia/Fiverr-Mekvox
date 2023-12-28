import logging
import sys

format = "[%(asctime)s]: %(levelname)s: %(module)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=format,
    handlers=[logging.StreamHandler(sys.stdout)]
)

amzn_bot_logger = logging.getLogger("Amazon-Bot")
