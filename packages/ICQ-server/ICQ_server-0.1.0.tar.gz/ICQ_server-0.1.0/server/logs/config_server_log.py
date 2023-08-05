import logging
import sys
import os
import logging.handlers
from time import strftime

sys.path.append(os.path.join(os.getcwd(), '../../../messenger'))

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, f'serverlog_{strftime("%Y-%m-%d")}.log')

log = logging.getLogger('serverlog')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(message)s')
file_hand = logging.handlers.TimedRotatingFileHandler(path, encoding='utf-8', when='D')
file_hand.setFormatter(formatter)

log.addHandler(file_hand)
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    log.debug('Отладочная информация')
    log.info('Информационное сообщение')
    log.warning('Предупреждение')
    log.error('Ошибка')
    log.critical('Критическая ошибка')
