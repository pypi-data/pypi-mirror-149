import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from .register_client import RegisterClient
from .remove_client import RemoveClient
from .server_gui import MainServerWindow, gui_create_model, HistoryServerWindow, create_stat_model, \
    ConfigServerWindow


class ServerWindow:

    def __init__(self, obj):
        self.obj = obj
        self.main_window = None
        self.config_window = None
        self.processes = []

    def server_window(self):
        server_app = QApplication(sys.argv)
        self.main_window = MainServerWindow()
        self.main_window.statusBar().showMessage('Сервер работает')
        self.main_window.table_body.setModel(gui_create_model(self.obj.database))
        self.main_window.btn_config.triggered.connect(self.server_config)
        self.main_window.btn_refresh.triggered.connect(self.list_update)
        self.main_window.btn_history.triggered.connect(self.show_statistics)
        self.main_window.btn_register.triggered.connect(self.register_clients)
        self.main_window.btn_delete.triggered.connect(self.remove_clients)

        try:
            timer = QTimer()
            timer.timeout.connect(self.list_update)
            timer.start(1000)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        server_app.exec_()
        self.obj.thread_run = False

    def list_update(self):
        if self.obj.new_connection:
            self.main_window.table_body.setModel(
                gui_create_model(self.obj.database))

    def show_statistics(self):
        try:
            stat_window = HistoryServerWindow()
            stat_window.table_clients.setModel(create_stat_model(self.obj.database))
            stat_window.exec_()
        except TypeError:
            pass

    def server_config(self):
        self.config_window = ConfigServerWindow()
        self.config_window.db_path.insert(self.obj.config['SETTINGS']['Database_path'])
        self.config_window.db_file.insert(self.obj.config['SETTINGS']['Database_file'])
        self.config_window.port.insert(self.obj.config['SETTINGS']['Default_port'])
        self.config_window.ip.insert(self.obj.config['SETTINGS']['Listen_Address'])
        self.config_window.save_btn.clicked.connect(self.save_server_config)

    def save_server_config(self):
        message = QMessageBox()
        self.obj.config['SETTINGS']['Database_path'] = self.config_window.db_path.text()
        self.obj.config['SETTINGS']['Database_file'] = self.config_window.db_file.text()
        try:
            port = int(self.config_window.port.text())
        except ValueError:
            message.warning(self.config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            self.obj.config['SETTINGS']['Listen_Address'] = self.config_window.ip.text()
            if 1023 < port < 65536:
                self.obj.config['SETTINGS']['Default_port'] = str(port)
                with open('server.ini', 'w') as conf:
                    self.obj.config.write(conf)
                    message.information(
                        self.config_window, 'OK', 'Настройки успешно сохранены!')
            else:
                message.warning(
                    self.config_window,
                    'Ошибка',
                    'Порт должен быть от 1024 до 65536')

    def register_clients(self):
        global reg_win
        reg_win = RegisterClient(self.obj)
        reg_win.show()

    def remove_clients(self):
        global rem_win
        rem_win = RemoveClient(self.obj)
        rem_win.show()
