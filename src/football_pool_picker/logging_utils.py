import logging


def get_logger(name: str = "football_pool_picker") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        h = logging.StreamHandler()
        fmt = logging.Formatter("[%(levelname)s] %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
    return logger


def anonymize_team(name: str) -> str:
    if not name:
        return name
    prefix = name[:1]
    return f"{prefix}*** {name.split(' ', 1)[-1]}" if " " in name else f"{prefix}***"
