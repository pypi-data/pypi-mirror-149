"""Классы. Окно статистики сообщений"""
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QDialog, QPushButton
from PyQt5.QtCore import Qt


class HistoryWindow(QDialog):
    """
    Класс. Окно с историей пользователей
    """
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.init_ui()

    def init_ui(self):
        """
        Дополнительная инициализация окна со статистикой сообщений
        :return:
        """
        # Настройки окна:
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Кнапка закрытия окна
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        # Лист с собственно историей
        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.create_stat_model()
        # self.show()

    def create_stat_model(self):
        """ Метод - реализует заполнение таблицы историей сообщений """

        # Список записей из БД
        stat_list = self.database.message_history()

        # объект модели данных
        q_ls = QStandardItemModel()
        q_ls.setHorizontalHeaderLabels(
            ["Имя клиента",
             "Последний взод",
             "Сообщений отправлено",
             "Сообщений получено"]
        )

        for row in stat_list:
            user, last_seen, sent, recvd = row
            user = QStandardItem(user)
            user.setEditable(False)
            last_seen = QStandardItem(str(last_seen.replace(microsecond=0)))
            last_seen.setEditable(False)
            sent = QStandardItem(str(sent))
            sent.setEditable(False)
            recvd = QStandardItem(str(recvd))
            recvd.setEditable(False)
            q_ls.appendRow([user, last_seen, sent, recvd])

        self.history_table.setModel(q_ls)
        self.history_table.resizeColumnsToContents()
        self.history_table.resizeRowsToContents()
