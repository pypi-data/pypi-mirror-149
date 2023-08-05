import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog


def gui_create_model(database):
    try:
        list_users = database.show_active_users()
        list = QStandardItemModel()
        list.setHorizontalHeaderLabels(['Имя клиента', 'IP-Адрес', 'Порт', 'Время подключения'])
        for row in list_users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            list.appendRow([user, ip, port, time])
        return list
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return


def create_stat_model(database):
    hist_list = database.message_history()
    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(
        ['Клиент', 'Последний вход', 'Отправлено', 'Получено'])
    for row in hist_list:
        user, last_seen, sent, recvd = row
        user = QStandardItem(user)
        user.setEditable(False)
        last_seen = QStandardItem(str(last_seen.replace(microsecond=0)))
        last_seen.setEditable(False)
        sent = QStandardItem(str(sent))
        sent.setEditable(False)
        recvd = QStandardItem(str(recvd))
        recvd.setEditable(False)
        list.appendRow([user, last_seen, sent, recvd])
    return list


class MainServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное окно сервера')
        self.setWindowIcon(QIcon('chat-bubble.png'))
        self.setFixedSize(600, 500)
        self.statusBar()

        self.btn_config = QAction('Настройки', self)
        self.btn_history = QAction('История подключений', self)
        self.btn_refresh = QAction('Обновить', self)
        self.btn_register = QAction('Регистрация клиентов', self)
        self.btn_delete = QAction('Удаление клиентов', self)

        self.btn_exit = QAction('Выход', self)
        self.btn_exit.setShortcut('Ctrl+Q')
        self.btn_exit.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Menu')
        self.toolbar.addAction(self.btn_config)
        self.toolbar.addAction(self.btn_history)
        self.toolbar.addAction(self.btn_refresh)
        self.toolbar.addAction(self.btn_exit)
        self.toolbar.addAction(self.btn_register)
        self.toolbar.addAction(self.btn_delete)

        self.table_title = QLabel('Список подключённых клиентов:', self)
        self.table_title.setAlignment(Qt.AlignCenter)
        self.table_title.setFixedSize(600, 15)
        self.table_title.move(10, 25)

        self.table_body = QTableView(self)
        self.table_body.move(10, 45)
        self.table_body.setFixedSize(580, 400)
        self.table_body.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.show()


class HistoryServerWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Последнее посещение и счетчик сообщений клиентов')
        self.setFixedSize(500, 400)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.table_clients = QTableView(self)
        self.table_clients.move(10, 10)
        self.table_clients.setFixedSize(480, 300)
        self.table_clients.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.btn_close = QPushButton('Закрыть', self)
        self.btn_close.setGeometry(200, 330, 100, 40)
        self.btn_close.clicked.connect(self.close)

        self.show()


class ConfigServerWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Настройки сервера')
        self.setFixedSize(365, 260)

        self.db_path_label = QLabel('Путь до файла базы данных: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)

        self.db_path_select = QPushButton('Обзор...', self)
        self.db_path_select.move(275, 28)

        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        self.ip_label_note = QLabel(' оставьте это поле пустым, чтобы\n принимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)

        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(190, 220)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = MainServerWindow()
    test.statusBar().showMessage('Тест главного окна сервера')
    test_list = QStandardItemModel(test)
    test_list.setHorizontalHeaderLabels(['Имя клиента', 'IP-Адрес', 'Порт', 'Время подключения'])
    test_list.appendRow([QStandardItem('Исаак Ньютон'), QStandardItem('23.236.62.147'),
                         QStandardItem('1111'), QStandardItem('20 марта 1727 года')])
    test_list.appendRow([QStandardItem('Иоганн Бернулли'), QStandardItem('109.70.26.37'),
                         QStandardItem('2222'), QStandardItem('20 марта 1727 года')])
    test_list.appendRow([QStandardItem('Нильс Бор'), QStandardItem('216.239.32.21'),
                         QStandardItem('3333'), QStandardItem('20 марта 1727 года')])
    test.table_body.setModel(test_list)
    app.exec_()

    # app = QApplication(sys.argv)
    # test = HistoryServerWindow()
    # test_list = QStandardItemModel(test)
    # test_list.setHorizontalHeaderLabels(['Имя клиента', 'Последний вход', 'Отправил', 'Получил'])
    # test_list.appendRow([QStandardItem('Исаак Ньютон'), QStandardItem('20 марта 1727 года'),
    #                      QStandardItem('298'), QStandardItem('1346')])
    # test_list.appendRow([QStandardItem('Иоганн Бернулли'), QStandardItem('1 января 1748'),
    #                      QStandardItem('416'), QStandardItem('2346')])
    # test_list.appendRow([QStandardItem('Нильс Бор'), QStandardItem('18 ноября 1962'),
    #                      QStandardItem('323'), QStandardItem('1235')])
    # test.table_clients.setModel(test_list)
    # app.exec_()

    # app = QApplication(sys.argv)
    # message = QMessageBox
    # dial = ConfigServerWindow()
    # app.exec_()
