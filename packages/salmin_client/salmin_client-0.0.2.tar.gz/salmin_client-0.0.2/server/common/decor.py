import sys
import logging
import traceback
from socket import socket
sys.path.append('../')
from log_profile.logger_server import SERVER
from log_profile.logger_client import CLIENT


if (sys.argv[0].split('/')[-1]).lower() == f'{SERVER}.py':
    logger = logging.getLogger(SERVER)
if (sys.argv[0].split('/')[-1]).lower() == f'{CLIENT}.py':
    logger = logging.getLogger(f'{CLIENT}')


def log_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.debug(f'Вызвана функция {func.__name__} с параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}. '
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     )
        return res
    return wrapper


def login_required(func):
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
