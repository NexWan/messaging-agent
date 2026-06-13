import logging

from .telegram import TelegramHandler
from .logging_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    # Configure logging before anything else
    setup_logging()

    # Init bot
    logger.info("Starting telegram bot polling....")
    TelegramHandler().init_bot()

if __name__ == '__main__':
    main()
