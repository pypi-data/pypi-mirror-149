import logging


def info(msg: str):
    logging.log(logging.INFO, msg)


def warn(msg: str):
    logging.log(logging.WARNING, msg)


def exception(e):
    logging.exception(e)
