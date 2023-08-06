import sys
import logging
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt


logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    """ Диалог добавления пользователя в список контактов
    Предлагает пользователю список возможных контактов и добавляет выбранный в контакты
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 130)
        self.setWindowTitle('Выберите контакт для добавления: ')
        # нужно удалить диалог, если окно было закрыто преждевременно
        self.setAttribute(Qt.WA_DeleteOnClose)
        # делает окно поверх других окон
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления: ', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 40)
        self.selector.move(10, 0)

        self.btn_refresh = QPushButton('Обновить\nсписок', self)
        self.btn_refresh.setFixedSize(100, 60)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # заполнение списка возможных контактов
        self.possible_contacts_update()

        # назначение действия на кнопку "Обновить"
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        """ Заполнение списка возможных контактов """
        self.selector.clear()
        # множества всех контактов и контактов клиента
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        # удаление из списка контактов самого себя
        users_list.remove(self.transport.username)
        # добавление списка возможных контактов
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        """ Обновление таблицы известных пользователей (с сервера),
        а затем - содержимое предполагаемых контактов
        """
        try:
            self.transport.users_list_update()
        except OSError:
            pass
        else:
            logger.debug('Обновление списка пользователей с сервера выполнено')
            self.possible_contacts_update()
