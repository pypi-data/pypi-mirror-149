import argparse
import logging
import threading
import time
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from configparser import ConfigParser

from server_dist.server.common.log_decor import log
from server_dist.server.server.core import MessageProcessor
from server_dist.server.server.server_database import ServerStorage
from server_dist.server.server.main_window import MainWindow
from server_dist.server.common.variables import *
from server_dist.server.common.errors import *

SERVER_LOGGER = logging.getLogger('serverlog')

new_connection = False
conflag_lock = threading.Lock()


@log
def arg_parser(default_port, default_address):
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_addr = namespace.a
    listen_port = namespace.p
    return listen_addr, listen_port


@log
def config_load():
    """Пармер конфигурации файла инициализации"""
    config = ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/server/{'server.ini'}")
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@log
def main():
    """Основная логика сервера"""
    config = config_load()

    listen_address, listen_port = arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()
    time.sleep(0.5)

    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(database, server, config)

    server_app.exec_()
    server.running = False


if __name__ == '__main__':
    main()
