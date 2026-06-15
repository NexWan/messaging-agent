import logging
import click

from .telegram import TelegramHandler
from .logging_config import setup_logging

logger = logging.getLogger(__name__)

@click.command()
@click.option("--provider", "-p", default="claude", help="Provider to use, available options: [claude, local]")
def main(provider):
    # Configure logging before anything else
    setup_logging()

    # Init bot
    logger.info("Starting telegram bot polling....")
    TelegramHandler(provider).init_bot()

if __name__ == '__main__':
    main()
