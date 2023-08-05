import dis
import logging

SERVER_LOGGER = logging.getLogger('serverlog')
CLIENT_LOGGER = logging.getLogger('clientlog')


class ClientVerifier(type):
    """Метакласс выпоняющий проверку,
    что в клиентском классе нет неверных вызовов
    """

    def __init__(cls, clsname, bases, clsdict):
        methods = []
        methods_2 = []
        attrs = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                CLIENT_LOGGER.error('В классе обнаружено '
                                    'использование запрещённого метода')
                raise TypeError('В классе обнаружено '
                                'использование запрещённого метода')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            CLIENT_LOGGER.error('Отсутствуют вызовы функций, '
                                'работающих с сокетами.')
            raise TypeError('Отсутствуют вызовы функций, '
                            'работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):
    """Метакласс выпоняющий проверку,
    что в серверном классе нет неверных вызовов
    """

    def __init__(cls, clsname, bases, clsdict):
        methods = []  # 'LOAD_GLOBAL'
        methods_2 = []  # 'LOAD_METHOD',
        attrs = []  # 'LOAD_ATTR'
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in methods:
            SERVER_LOGGER.error('Использование метода connect '
                                'недопустимо в серверном классе')
            raise TypeError('Использование метода connect '
                            'недопустимо в серверном классе')
        if not ('SOCK_STREAM' in methods and 'AF_INET' in methods):
            SERVER_LOGGER.error('Некорректная инициализация сокета.')
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)
