import random
import string
import logging


def generate_id(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choices(chars, k=size))


def get_logger(logger_name):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s'))
    logger.addHandler(console)
    logging.getLogger('ws4py').addHandler(console)

    return logger


LOG = get_logger(__name__)
