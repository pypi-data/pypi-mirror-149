import os
from os import path
import logging.handlers


SERVER = 'server'


def base_format(module):
    return f'%(levelname)s - %(asctime)s - {module} - %(message)s'


def log_dir(value):
    # return f'{path.join(path.dirname(__file__))}/../logs/{value}_log/{value}.log'
    return f'{os.getcwd()}/../logs/{value}_log/{value}.log'

logger = logging.getLogger(SERVER)

logger_handler = logging.handlers.TimedRotatingFileHandler(
    log_dir(SERVER),
    encoding='utf-8', when='midnight', interval=1
)

logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(logging.Formatter(base_format(SERVER)))

logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    logger.critical('Critical_server')
    logger.error('Error_server')
    logger.warning('Warning_server')
    logger.info('Info_server')
    logger.debug('Debug_server')
