from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import os


class SettingWindow(QDialog):
    def __init__(self, config):
        super().__init__()

        self.config = config
        self.initUI()

    def initUI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.db_file_label = QLabel('Выберите файл: ', self)
        self.db_file_label.setFixedSize(240, 15)
        self.db_file_label.move(10, 10)

        self.db_file = QLineEdit(self)
        self.db_file.setFixedSize(250, 20)
        self.db_file.move(10, 30)
        self.db_file.setReadOnly(True)

        self.db_file_select = QPushButton('Обзор...', self)
        self.db_file_select.move(275, 28)

        self.ip_label = QLabel('Введите IP: ', self)
        self.ip_label.setFixedSize(180, 15)
        self.ip_label.move(10, 110)

        self.ip = QLineEdit(self)
        self.ip.setFixedSize(150, 20)
        self.ip.move(200, 108)

        self.port_label = QLabel('Введите Port: ', self)
        self.port_label.setFixedSize(180, 15)
        self.port_label.move(10, 150)

        self.port = QLineEdit(self)
        self.port.setFixedSize(150, 20)
        self.port.move(200, 148)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(190, 220)

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.move(275, 220)
        self.close_btn.clicked.connect(self.close)

        self.db_file_select.clicked.connect(self.open_file_dialog)

        self.show()

        self.db_file.insert(self.config['SETTINGS']['Database_file'])
        self.port.insert(self.config['SETTINGS']['Default_port'])
        self.ip.insert(self.config['SETTINGS']['Listen_Address'])
        self.save_btn.clicked.connect(self.save_server_config)

    def open_file_dialog(self):
        global dialog
        dialog = QFileDialog(self)
        path = dialog.getOpenFileName()[0]
        path = path.replace('/', '\\')
        self.db_file.insert(path)
        self.db_file.clear()
        self.db_file.insert(path)

    def save_server_config(self):
        global config_window
        message = QMessageBox()
        self.config['SETTINGS']['Database_file'] = self.db_file.text()
        try:
            port = int(self.port.text())
        except ValueError:
            message.warning(self, 'Ошибка', 'Порт должен быть числом')
        else:
            self.config['SETTINGS']['Listen_Address'] = self.ip.text()
            if 1023 < port < 65536:
                self.config['SETTINGS']['Default_port'] = str(port)
                # dir_path = os.path.dirname(os.path.realpath(__file__))
                dir_path = os.getcwd()
                dir_path = os.path.join(dir_path, '..')
                with open(f"{dir_path}/{'server.ini'}", 'w') as conf:
                    self.config.write(conf)
                    message.information(
                        self, 'OK', 'Настройки сохранены!')
            else:
                message.warning(
                    self, 'Ошибка', 'Порт должен быть от 1024 до 65536')
