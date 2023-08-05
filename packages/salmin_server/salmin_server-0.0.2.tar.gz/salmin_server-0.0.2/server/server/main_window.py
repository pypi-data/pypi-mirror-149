
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTimer
from .stat_window import StatWindow
from .setting_window import SettingWindow
from .add_user import RegisterUser
from .remove_user import DelUserDialog


class MainWindow(QMainWindow):
    def __init__(self, database, server, config):
        super().__init__()

        self.database = database

        self.server_thread = server
        self.config = config


        self.exit_action = QAction('Выход', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(qApp.quit)

        self.refresh_btn = QAction('Обновить', self)
        self.register_btn = QAction('Регистрация пользователя', self)
        self.remove_btn = QAction('Удаление пользователя', self)
        self.history_btn = QAction('История', self)
        self.setting_btn = QAction('Настройки сервера', self)
        self.help_btn = QAction('Помощь', self)

        self.statusBar()
        menu_bar = self.menuBar()
        file_menu_1 = menu_bar.addMenu('&File')
        file_menu_1.addAction(self.refresh_btn)
        file_menu_1.addAction(self.register_btn)
        file_menu_1.addAction(self.remove_btn)
        file_menu_1.addAction(self.history_btn)
        file_menu_1.addAction(self.exit_action)

        file_menu_2 = menu_bar.addMenu('&Settings')
        file_menu_2.addAction(self.setting_btn)

        file_menu_3 = menu_bar.addMenu('&Help')
        file_menu_3.addAction(self.help_btn)
        self.statusBar().showMessage('Server Working')

        # self.toolbar = self.addToolBar('MainBar')
        # self.toolbar.addAction(self.exit_action)
        # self.toolbar.addAction(self.refresh_btn)
        # self.toolbar.addAction(self.history_btn)
        # self.toolbar.addAction(self.setting_btn)
        # self.toolbar.addAction(self.register_btn)
        # self.toolbar.addAction(self.remove_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging Server alpha release')

        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_users_model)
        self.timer.start(1000)

        self.refresh_btn.triggered.connect(self.create_users_model)
        self.history_btn.triggered.connect(self.show_statistics)
        self.setting_btn.triggered.connect(self.server_config)
        self.register_btn.triggered.connect(self.reg_user)
        self.remove_btn.triggered.connect(self.rem_user)

        self.show()

    def create_users_model(self):
        list_users = self.database.active_users_list()
        list = QStandardItemModel()
        list.setHorizontalHeaderLabels(
            ['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
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
        self.active_clients_table.setModel(list)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()

    def show_statistics(self):
        global stat_window
        stat_window = StatWindow(self.database)
        stat_window.show()

    def server_config(self):
        global config_window
        config_window = SettingWindow(self.config)

    def reg_user(self):
        global reg_window
        reg_window = RegisterUser(self.database, self.server_thread)
        reg_window.show()

    def rem_user(self):
        global rem_window
        rem_window = DelUserDialog(self.database, self.server_thread)
        rem_window.show()
