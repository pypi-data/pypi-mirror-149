import os
from os import path
import sys
import argparse
import configparser
from PyQt5.QtCore import Qt
from server.core import MessageProcessor
from server.database import ServerStorage
from log_profile.logger_server import SERVER
from common.variables import *
from common.decor import log_decorator
from PyQt5.QtWidgets import QApplication
from server.main_window import MainWindow

logger = logging.getLogger(SERVER)


@log_decorator
def arg_parser(default_address, default_port):
    '''Парсер аргументов коммандной строки.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


@log_decorator
def config_load():
    '''Парсер конфигурационного ini файла.'''
    config = configparser.ConfigParser()
    # dir_path = path.dirname(path.realpath(__file__))
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@log_decorator
def main():
    '''Основная функция'''
    config_file = config_load()

    listen_address, listen_port = arg_parser(
        config_file['SETTINGS']['Listen_Address'],
        config_file['SETTINGS']['Default_port']
    )

    database = ServerStorage(
        config_file['SETTINGS']['Database_file'].split('\\')[-1]
    )

    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(database, server, config_file)

    server_app.exec_()

    server.running = False


if __name__ == '__main__':
    main()
