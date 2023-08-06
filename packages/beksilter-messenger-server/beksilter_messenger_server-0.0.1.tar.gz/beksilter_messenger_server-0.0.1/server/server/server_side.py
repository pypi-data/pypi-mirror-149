import os,sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import argparse
import logging
import configparser
from common.utilities import *
from common.decos import log
from common.variables import DEFAULT_PORT, SERVER_SETTINGS_PATH, PLUGINS_PATH
from server.core import MessageProcessor
from server.database import ServerStorage
from server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication

# Инициализация логирования сервера.
logger = logging.getLogger('server_side')


@log
def arg_parser(default_port, default_address):
    """Парсер аргументов коммандной строки."""
    logger.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    logger.debug('Аргументы успешно загружены.')
    return listen_address, listen_port, gui_flag


@log
def config_load():
    """Парсер конфигурационного ini файла."""
    config = configparser.ConfigParser()
    config.read(SERVER_SETTINGS_PATH)
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
    # умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', 'server')
        config.set('SETTINGS', 'Database_file', 'database.db3')
        return config


@log
def main():
    """Основная функция"""
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    # Исправление ошибки, встречается при использовании виртуального окружения:
    # qt.qpa.plugin: Could not find the Qt platform plugin "windows" in ""
    # This application failed to start because no Qt platform plugin
    # could be initialized. Reinstalling the application may fix this problem.
    # Для этого используется и копирование в корень проекта папки:
    # C:\Users\23rad\AppData\Local\Programs\
    # Python\Python39\Lib\site-packages\PyQt5\Qt\plugins\platforms
    # и следующая команда:
    # QCoreApplication.addLibraryPath("./")

    # Более простое решение, просто указать путь до папки в виртуальном
    # окружениее но в папке QT5, а не QT, тогда папку копировать не нужно:
    QCoreApplication.addLibraryPath(PLUGINS_PATH)
    main()