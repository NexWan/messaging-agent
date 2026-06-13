import logging


def setup_logging(log_file: str = "telegram.log", level: int = logging.INFO) -> None:
    """Configure root logging for the bot.

    Writes to ``log_file`` with timestamps, and quiets the noisy long-polling /
    HTTP loggers so the file stays readable (this also keeps the bot token out
    of the log, since it would otherwise appear in every getUpdates request).
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
