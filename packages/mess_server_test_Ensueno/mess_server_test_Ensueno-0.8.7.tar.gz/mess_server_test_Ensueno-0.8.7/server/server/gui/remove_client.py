from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton


class RemoveClient(QDialog):

    def __init__(self, obj):
        super().__init__()
        self.database = obj.database
        self.server = obj

        self.setFixedSize(350, 120)
        self.setWindowTitle('Удаление пользователя')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel(
            'Выберите пользователя для удаления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_ok.clicked.connect(self.remove_user)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.all_users_fill()

    def all_users_fill(self):
        self.selector.addItems([item[0]
                                for item in self.database.show_users_list()])

    def remove_user(self):
        self.database.remove_user(self.selector.currentText())
        if self.selector.currentText() in self.server.client_names:
            self.server.remove_client(self.selector.currentText())
        self.server.service_update_lists()
        self.close()
