import socket
import sys
import logging

sys.path.append('../../../messenger/')
import server_dist.server.logs.config_server_log

if sys.argv[0].find('client.py') == -1:
    LOGGER = logging.getLogger('serverlog')
else:
    LOGGER = logging.getLogger('clientlog')


def log(func):
    """Декоратор выполняющий логирование функция"""
    def wrap(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'функция {func.__name__} с аргументами {args}, {kwargs} вызвана из функции {func.__module__}')
        return res

    return wrap


def login_required(func):
    """Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        from server_dist.server.server.core import MessageProcessor
        from server_dist.server.common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
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
