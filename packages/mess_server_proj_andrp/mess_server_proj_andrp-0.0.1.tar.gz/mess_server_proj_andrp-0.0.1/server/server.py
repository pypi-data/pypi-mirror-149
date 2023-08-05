"""Файл сервера"""
import socket
import os
import argparse
import select
import sys
import threading
import configparser
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, Qt

from common.utils import *
from common.decos import log
from common.variables import DESTINATION
from common.descryptors import Port
from common.metaclasses import ServerMaker
from server.core import MessageProcessor
from server.database import ServerStorage
from server.server_gui import gui_create_model, create_stat_model
from server.config_window import ConfigWindow
from server.main_window import MainWindow
from server.history_window import HistoryWindow

# Инициализация логирования сервера.
logger = logging.getLogger('server')

# Флаг что был подключён новый пользователь, нужен чтобы не мучать BD
# постоянными запросами на обновление
new_connection = False
conflag_lock = threading.Lock()



@log
def arg_parser(default_port, default_address):
    """
    Парсер аргументов коммандной строки.
    :param default_port:
    :param default_address:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    return listen_address, listen_port, gui_flag


def config_load():
    """
    Загрузка файла конфигурации
    :return:
    """
    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
    # умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


def main():
    """
    Основная функция main()
    :return:
    """
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(config['SETTINGS']['Default_port'],
                                                       config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerStorage(os.path.join(
        config['SETTINGS']['Database_path'],
        config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Переключатель GUI
    if gui_flag:
        while True:
            command = input('Нажмите 9 для завершения работы сервера')
            if command == '9':
                server.running = False
                server.join()
                break
    else:
        # графическое окружение для сервера
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # запуск GUI
        server_app.exec_()

        # при закрытии окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
