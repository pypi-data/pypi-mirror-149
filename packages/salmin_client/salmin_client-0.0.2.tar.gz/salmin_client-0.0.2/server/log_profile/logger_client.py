import os
from os import path
import logging.handlers


CLIENT = 'client'


def base_format(module):
    return f'%(levelname)s - %(asctime)s - {module} - %(message)s'


def log_dir(value):
    # return f'{path.join(path.dirname(__file__))}/../logs/{value}_log/{value}.log'
    return f'{os.getcwd()}/../logs/{value}_log/{value}.log'

logger = logging.getLogger(CLIENT)

logger_handler = logging.handlers.TimedRotatingFileHandler(
    log_dir(CLIENT), encoding='utf-8', when='midnight', interval=1
)
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(logging.Formatter(base_format(CLIENT)))

logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.critical('Critical_client')
    logger.error('Error_client')
    logger.warning('Warning_client')
    logger.info('Info_client')
    logger.debug('Debug_client')
