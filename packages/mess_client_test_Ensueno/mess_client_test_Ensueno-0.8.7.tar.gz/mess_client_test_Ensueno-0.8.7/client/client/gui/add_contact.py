"""
Модуль add_contact предназначен для создания и полноценной работы
окна добавления контакта.

Основным классом является AddContactDialog, в интерфейсе которого
реализуется создание окна добавления контакта и инициация списка
известных Клиенту зарегистрированных пользователей и его обновление.

The add_contact module is designed for creation and full-fledged work
of window for adding a contact.

The main class is AddContactDialog, the interface of which implements
the creation of a window for adding a contact and initiating a list
of registered users known to the Client and updating it.
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton

logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    """
    Класс AddContactDialog используется для создания окна добавления
    контакта и инициации списка известных Клиенту зарегистрированных
    пользователей и его обновления.
    Дочерний класс класса QDialog.

    **Атрибуты**

    * transport : Client
        экземпляр класса Client, основной элемент бэкенда клиентской
        части мессенджера
    * database : ClientStorage
        экземпляр класса ClientStorage, основной элемент взаимодействия
        с базой данных Клиента

    **Методы**

    * possible_contacts_update():
        формирование списка доступных для добавления пользователей
    * update_possible_contacts():
        обновление списка доступных для добавления пользователей

    The AddContactDialog class is used to create an add contact window and
    initiate the list of registered users known to the Client and update it.
    A child class of the QDialog class.

    **Attributes**

    * transport : Client
        an instance of the Client class, the main element of the client's backend
        messenger parts
    * database : ClientStorage
        an instance of the ClientStorage class, the main element of interaction
        with the Client's database

    **Methods**

    * possible_contacts_update():
        creating a list of users available for adding
    * update_possible_contacts():
        updating the list of available users to add
    """
    def __init__(self, transport, database):
        """
        Инициация класса AddContactDialog.
        Наследование от родительского класса QDialog. Задание геометрии, поведения и
        определение PyQT-элементов окна добавления контактов. Обновление списка
        известных Клиенту зарегистрированных пользователей.

        **Параметры**

        * transport : Client
            экземпляр класса Client, основной элемент бэкенда клиентской
            части мессенджера
        * database : ClientStorage
            экземпляр класса ClientStorage, основной элемент взаимодействия
            с базой данных Клиента

        Initializing the AddContactDialog class.
        Inheritance from the parent QDialog class. Setting geometry, behavior, and
        definition of PyQt elements of the contact adding window. Updating the list
        registered users known to the Client.

        **Parameters**

        * transport : Client
            an instance of the Client class, the main element of the backend of the
            client's messenger parts
        * database : ClientStorage
            an instance of the ClientStorage class, the main element of interaction
            with the Client's database
        """
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.possible_contacts_update()
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        '''
        Запрашивает списка контактов Клиента и списка известных Клиенту на текущий
        момент зарегистрированных пользователей. Удаляет из списка пользователей тех,
        кто уже находится в контактах и самого Клиента. Добавляет результат к элементу
        селектора (выпадающего списка).

        Requests the Client's contact list and the list of of registered users known
        to the Client for the current moment. Removes from the list of users those
        who are already in contacts and the Client himself. Adds the result to the element
        selector (drop-down list).
        '''
        try:
            self.selector.clear()
            contacts_list = set(self.database.get_contacts())
            users_list = set(self.database.get_users())
            users_list.remove(self.transport.client_name)
            self.selector.addItems(users_list - contacts_list)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def update_possible_contacts(self):
        '''
        Запрашивает у экземпляра класса Client обновление списка
        зарегистрированных в мессенджере пользователей. Экземпляр
        класса Client направляет запрос серверу и обновляет этот список.
        Далее происходит вызов метода possible_contacts_update().

        Requests an instance of the Client class to update the
        list of users registered in the messenger. An instance of
        the Client class sends a request to the server and updates this list.
        Next, the possible_contacts_update() method is called.
        '''
        try:
            self.transport.user_list_request(repeated=True)
        except OSError:
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        else:
            logger.debug('Обновление списка пользователей с сервера выполнено')
            self.possible_contacts_update()
