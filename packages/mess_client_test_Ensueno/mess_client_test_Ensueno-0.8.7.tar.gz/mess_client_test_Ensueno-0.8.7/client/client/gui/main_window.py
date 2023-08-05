"""
Модуль main_window предназначен для создания и полноценной работы
главного окна мессенджера (клиентская часть).

**Классы**

* ClientMainWindow
    Основным классом является ClientMainWindow, в интерфейсе которого
    реализуется создание окна взаимодействия клиента с его собеседниками
    и контакт-листом.
* TestRequestingObj
    Дополнительный класс создан для тестирования работоспособности
    основного класса.

**Функции**

* start_main_window(obj):
    инициирует создание экземпляра ClientMainWindow, присоединяет слоты к
    сигналам, завершает работу клиентской части мессенджера.

    *Параметры*

    + obj : Client
        экземпляр класса Client, основной элемент бэкенда клиентской
        части мессенджера

The main_window module is designed to create and fully operate
the main window of the messenger (the client part).

**Classes**

* ClientMainWindow
    The main class is ClientMainWindow, in the interface of which is
    implemented the creation of a window of interaction between the
    client and his interlocutors and a contact list.
* TestRequestingObj
    The additional TestRequestingObj class was created to test the main class.

**Functions**

* start_main_window(obj):
    initiates the creation of an instance of ClientMainWindow, attaches slots
    to signals, shuts down the client part of the messenger.

    *Parameters*

    + obj : Client
        an instance of the Client class, the main element of the client's backend
        messenger parts
"""
import base64
import json
import sys
import time

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication

from client.gui.add_contact import AddContactDialog
from client.gui.del_contact import DelContactDialog
from client.gui.main_window_ui import Ui_MainClientWindow
from common.vars import MESSAGE_TEXT, SENDER
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


class ClientMainWindow(QMainWindow):
    """
    Класс ClientMainWindow используется для создания главного окна клиентской
    части мессенджера и реализации пользовательского функционала во взаимосвязи
    с бекэндом.
    Дочерний класс класса QMainWindow.

    **Атрибуты**

    * obj : Client
        экземпляр класса Client, основной элемент бэкенда клиентской
        части мессенджера
    * descriptor
        объект дешифратора сообщений
    * logger
        объект логирования Клиента
    * contacts_model
        модель контактов
    * history_model
        модель истории сообщений
    * messages
        модульное окно сообщений системы
    * current_chat : str
        имя текущего собеседника
    * current_chat_key
        публичный ключ текущего собеседника
    * encryptor
        объект шифратора сообщений

    **Методы**

    * set_disabled_input():
        дезактивирует область ввода текст сообщений
    * history_list_update():
        обновляет историю сообщений
    * select_active_user():
        определяет текущего собеседника
    * set_active_user():
        запрашивает открытый ключ собеседника и инициирует диалог с ним
    * clients_list_update():
        актуализирует список контактов
    * add_contact_window():
        запускает окно добавления контактов
    * add_contact_action(item):
        инициирует процесс добавления контакта
    * add_contact(new_contact):
        делегирует базе данных добавление контакта и объекту
        Клиента - уведомление сервера об этом
    * delete_contact_window():
        запускает окно удаления контактов
    * delete_contact(item):
        делегирует базе данных удаление контакта и объекту
        Клиента - уведомление сервера об этом
    * send_message():
        инициирует процесс шифрования и отправки сообщения,
        сохранения его в базе данных
    * say_goodbye_and_exit():
        инициирует процесс завершения работы клиентской части мессенджера
    * message(message):
        метод-слот для сигнала объекта Клиента, дешифрует получаемое
        сообщение, сохраняет в базу данных
    * sig_205():
        метод-слот для сигнала объекта Клиента, активирует обновление
        контакт-листа при изменениях на сервере списка
        зарегистрированных пользователей
    * make_connection():
        метод для назначения сигналам слотов

    The ClientMainWindow class is used to create the main window of the client
    part of the messenger and implement user functionality in conjunction
    with the backend.
    A child class of the QMainWindow class.

    **Attributes**

    * obj : Client
        an instance of the Client class, the main element of the
        client's backend messenger parts
    * descriptor
        message decryptor object
    * logger
        Client logging object
    * contacts_model
        contact model
    * history_model
        message history model
    * messages
        modal system message window
    * current_chat : str
        name of the current interlocutor
    * current_chat_key
        the public key of the current interlocutor
    * encryptor
        message encoder object

    **Methods**

    * set_disabled_input():
        deactivates the message text input area
    * history_list_update():
        updates the message history
    * select_active_user():
        defines the current interlocutor
    * set_active_user():
        requests the public key of the interlocutor and initiates
        a dialogue with him
    * clients_list_update():
        updates the contact list
    * add_contact_window():
        starts the window for adding contacts
    * add_contact_action():
        initiates the process of adding a contact
    * add_contact():
        delegates adding a contact to the database and notifying
        the server about it to the Client object
    * delete_contact_window():
        starts the contact deletion window
    * delete_contact():
        delegates the deletion of a contact to the database and
        notifies the server about it to the Client object
    * send_message():
        initiates the process of encrypting and sending a message,
        saving it to the database
    * say_goodbye_and_exit():
        initiates the shutdown process of the messenger client part
    * message():
        the method-slot for the signal of the Client object,
        decrypts the received message, saves it to the database
    * sig_205():
        the method-slot for the Client object signal, activates the
        update of the contact list when the list of registered
        users changes on the server
    * make_connection():
        method for assigning slots to signals
    """
    def __init__(self, obj):
        """
        Инициация класса ClientMainWindow.
        Наследование от родительского класса QMainWindow. Задание геометрии и поведения
        элементов окна. Назначение элементам действий при взаимодействии пользователя с ними.
        Обновление списка контактов Клиента и дезактивация поля ввода текста сообщения.

        **Параметры**

        * obj : Client
            экземпляр класса Client, основной элемент бэкенда клиентской
            части мессенджера

        Initiation of the ClientMainWindow class.
        Inheritance from the parent class QMainWindow. Setting geometry and behavior of
        window elements. Assigning actions to elements when the user interacts with them.
        Updating the Client's contact list and deactivating the message text input window part.

        **Parameters**

        * obj : Client
            an instance of the Client class, the main element of the client's backend
            messenger parts
        """
        super().__init__()
        self.obj = obj
        self.descriptor = PKCS1_OAEP.new(obj.keys)
        self.logger = obj.logger
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        self.ui.menu_exit.triggered.connect(self.say_goodbye_and_exit)
        self.ui.btn_send.clicked.connect(self.send_message)
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)
        self.setWindowTitle(f'Добро пожаловать, {self.obj.client_name}')

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        '''
        Делает область ввода текста сообщения неактивной.
        Makes the text input area of the message inactive.
        '''
        self.ui.label_new_message.setText('Для выбора получателя дважды '
                                          'кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_list_update(self):
        """
        Очищает историю сообщений с текущим собеседником и обновляет ее.
        Clears the message history with the current interlocutor and updates it.
        """
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()

        list_msg = sorted(self.obj.database.get_msg_history
                          (buddy_history=self.current_chat, limit=20),
                      key=lambda item: item[3])

        for i in list_msg:
            if i.index(self.current_chat) == 0:
                mess = QStandardItem(f'Входящее от {i[3].replace(microsecond=0)}:\n {i[2]}')
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
            else:
                mess = QStandardItem(f'Исходящее от {i[3].replace(microsecond=0)}:\n {i[2]}')
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
            mess.setEditable(False)
            self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """
        Определяет текущего собеседника.
        Identifies the current interlocutor.
        """
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """
        Запрашивает открытый ключ для текущего собеседника.
        Активирует поле ввода текста сообщения.
        Загружает историю сообщений между Клиентом и его собеседником.

        Requests a public key for the current interlocutor. Activates the text
        input field of the message. Loads the history of messages between
        the Client and his interlocutor.
        """
        try:
            self.current_chat_key = self.obj.key_request(self.current_chat)
            if self.current_chat_key:
                self.logger.debug(f'Загружен открытый ключ для {self.current_chat}')
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            self.logger.debug(f'Не удалось получить ключ для {self.current_chat}')

        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return

        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)
        self.history_list_update()

    def clients_list_update(self):
        """
        Запрашивает в базе данных клиента актуальный список контактов.
        Формирует модель контактов.

        Requests an up-to-date list of contacts in the client's database.
        Forms a contact model.
        """
        contacts_list = self.obj.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """
        Инициирует создание окна добавления контактов, подключает к его
        элементам функционал и запускает это окно.

        Initiates the creation of a window for adding contacts, connects
        functionality to its elements and launches this window.
        """
        global select_dialog
        try:
            select_dialog = AddContactDialog(self.obj, self.obj.database)
        except Exception as err:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(err).__name__, err.args)
            print(message)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """
        Считывает имя добавляемого контакта, вызывает метод добавления
        контакта и закрывает окно добавления контактов.

        **Параметры**

        * item (AddContactDialog):
            объект класса AddContactDialog

        Reads the name of the added contact, calls the add contact method
        and closes the add contacts window.

        **Parameters**

        * item (AddContactDialog):
            an object of the AddContactDialog class
        """
        new_contact = item.selector.currentText()
        try:
            self.add_contact(new_contact)
        except Exception as error:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(error).__name__, error.args)
            print(message)
        item.close()

    def add_contact(self, new_contact):
        """
        Вызывает метод объекта Клиента add_contact, который выполняет
        обмен данными с сервером для сообщения ему о добавлении контакта.
        Вызывает метод объекта базы данных Клиента add_contact, который добавляет
        запись в таблицу Contacts.
        Обновляет модель контактов. Вызывает окно сообщения в случае успеха.

        **Параметры**

        * new_contact (str):
            имя добавляемого контакта

        Calls the add_contact method of the Client object, which exchanges
        data with the server to inform it about the addition of a contact.
        Calls a method of the Client database object that adds an entry to
        the Contacts table.
        Updates the contact model. Brings up a message box if successful.

        **Parameters**

        * new_contact (str):
            name of the contact to be added
        """
        try:
            self.obj.add_contact(new_contact)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.obj.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            self.obj.logger.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех', 'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """
        Инициирует создание окна удаления контактов, подключает к его
        элементам функционал и запускает это окно.

        Initiates the creation of a contact deletion window, connects it to
        the functional elements and launches this window.
        """
        global remove_dialog
        remove_dialog = DelContactDialog(self.obj.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """
        Вызывает метод объекта Клиента del_contact, который выполняет обмен
        данными с сервером для сообщения ему об удалении контакта.
        Вызывает метод объекта базы данных Клиента del_contact, который удаляет
        запись из таблицы Contacts. Вызывает метод clients_list_update для
        обновления списка контактов. Вызывает окно сообщения в случае успеха.
        Если удаляемый контакт был текущим собеседником, дезактивирует окно
        обмена сообщениями.

        **Параметры**

        * item (DelContactDialog):
            объект класса DelContactDialog

        Calls del_contact, the method of the Client object, which performs data
        exchange with the server to inform it about the removal of the contact.
        Calls del_contact, the method of the Client database object, which
        deletes an entry from the Contacts table. Calls the clients_list_update
        method to update the contact list. Brings up a message box if successful.
        If the contact being deleted was the current interlocutor, deactivates
        the messaging window.

        **Parameters**

        * item (DelContactDialog):
            an object of the DelContactDialog class
        """
        selected = item.selector.currentText()
        try:
            self.obj.del_contact(selected)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.obj.database.del_contact(selected)
            self.clients_list_update()
            self.obj.logger.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Считывает текст из окна ввода сообщения и очищает его. Зашифровывает
        текст, вызывает метод отправки сообщений объекта Клиента и передает в
        него данные текста. В случае удачи вызывает метод сохранения сообщения
        в базе данных Клиента и обновляет историю сообщений для ее отображения.

        Reads the text from the message input window and clears it. Encrypts
        the text, calls the method of sending messages of the Client object and
        transmits text data to it. If successful, calls the method of saving
        the message in the Client database and updates the message history
        to display it.
        """
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return

        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)

        try:
            self.obj.create_message(self.current_chat,
                                    message_text_encrypted_base64.decode('ascii'))
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except Exception as exception:
            template = "Main window, send_message, An exception of type {0} " \
                       "occurred. Arguments:\n{1!r}"
            message = template.format(type(exception).__name__, exception.args)
            print(message)
        else:
            self.obj.database.save_message(self.obj.client_name, self.current_chat, message_text)
            self.logger.debug(
                f'Отправлено сообщение для {self.current_chat}: {message_text}')
            self.history_list_update()

    def say_goodbye_and_exit(self):
        """
        Вызывает метод объекта Клиента для сообщения серверу о завершении работы,
        закрывает окно клиентской части мессенджера.

        Calls the method of the Client object to notify the server about the
        shutdown, closes the window of the client part of the messenger.
        """
        try:
            self.obj.say_goodbye_and_exit()
            time.sleep(2)
            qApp.exit()
        except Exception as exx:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exx).__name__, exx.args)
            print(message)

    @pyqtSlot(dict)
    def message(self, message):
        """
        Метод, обозначенный как слот для сигнала объекта Клиента send_new_message.
        Получает зашифрованный текст сообщения, дешифрует его при помощи объекта
        дешифратора. В случае если текущий собеседник является отправителем
        сообщения, сохраняет сообщение в базе данных Клиента и обновляет историю
        сообщений. Если сообщение отправил другой пользователь, определяет,
        находится ли он в контактах Клиента. Уведомляет пользователя о новом
        сообщении и спрашивает, открыть ли диалог с отправителем. В случае
        положительного ответа сохраняет сообщение в базе данных Клиента и
        открывает диалог с отправителем. В случае отказа просто сохраняет
        сообщение в базе данных. Если пользователь не в контакт-листе,
        пользователю предлагается открыть сообщение, при этом отправитель
        будет добавлен в контакт-лист. При отказе сообщение будет сохранено
        в базе данных, но отправитель в контакт-лист не добавляется.

        **Параметры**

        * message (dict):
            словарь с данными сообщения (текст, отправитель, дата)

        The method designated as a slot for the send_new_message signal of the
        Client object. Receives the encrypted text of the message, decrypts it
        using the descriptor object.
        If the current interlocutor is the sender of the message, saves the
        message in the Client database and updates the message history.
        If the message was sent by another user, it determines whether he is
        in the Client's contacts. Notifies the user of a new message and asks
        whether to open a dialog with the sender. In case of a positive response,
        saves the message in the Client database and opens a dialog with the
        sender. In case of failure, it simply saves the message in the database.
        If the user is not in the contact list, the user is prompted to open
        the message, and the sender will be added to the contact list.
        In case of refusal, the message will be saved in the database, but the
        sender is not added to the contact list.

        **Parameters**

        * message (dict):
            dictionary with message data (text, sender, date)
        """
        encrypted_message = base64.b64decode(message[MESSAGE_TEXT])
        try:
            decrypted_message = self.descriptor.decrypt(encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return

        sender = message[SENDER]
        if sender == self.current_chat:

            self.obj.database.save_message(self.current_chat, self.obj.client_name,
                                           decrypted_message.decode('utf8'))

            self.history_list_update()
        else:
            if self.obj.database.check_in_contacts(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender},'
                                          f'открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
                    self.obj.database.save_message(self.current_chat, self.obj.client_name,
                                                   decrypted_message.decode('utf8'))
                    self.history_list_update()
                else:
                    self.obj.database.save_message(sender, self.obj.client_name,
                                                   decrypted_message.decode('utf8'))
            else:
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n '
                                          f'Данного пользователя нет в вашем '
                                          f'контакт-листе.\n Добавить в контакты'
                                          f'и открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()
                    self.obj.database.save_message(self.current_chat, self.obj.client_name,
                                                   decrypted_message.decode('utf8'))
                    self.history_list_update()
                else:
                    self.obj.database.save_message(sender, self.obj.client_name,
                                                   decrypted_message.decode('utf8'))

    @pyqtSlot()
    def sig_205(self):
        """
        Метод, обозначенный как слот для сигнала объекта Клиента message_205.
        Вызывается при изменениях списка зарегистрированных на сервере
        пользователей. Если текущий собеседник пользователя был удален с
        сервера, об этом сообщается пользователю и поле ввода текста станет
        неактивным. Обновляет список клиентов пользователя.

        The method designated as a slot for the message_205 signal of the Client
        object. Called when the list of users registered on the server changes.
        If the user's current interlocutor has been deleted from the server,
        this is reported to the user and the text input field becomes inactive.
        Updates the user's client list.
        """
        if self.current_chat and not self.obj.database.check_in_known(
                self.current_chat):
            self.messages.warning(self, 'Сочувствую',
                                  'К сожалению собеседник был удалён с сервера.')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_list_update()

    def make_connection(self):
        """
        Метод для назначения сигналам слотов.
        Method for assigning slots to signals
        """
        self.obj.send_new_message.connect(self.message)
        self.obj.message_205.connect(self.sig_205)


class TestRequestingObj:
    """
    Класс TestRequestingObj - вспомогательный класс с атрибутами-заглушками для
    проверки работы основного класса ClientMainWindow.

    The TestRequestingObj class is an auxiliary class with stub attributes for
    checking the operation of the main ClientMainWindow class.
    """
    def __init__(self):
        self.obj = None
        self.obj.database = None


def start_main_window(obj):
    """
    Инициирует создание объекта главного окна ClientMainWindow. Выполняет
    соединение сигналов и слотов. Запускает главное окно, закрывает его
    при завершении работы клиентской части мессенджера.

    **Параметры**

    * obj (Client):
        экземпляр класса Client, основной элемент бэкенда клиентской части
        мессенджера.

    Initiates the creation of the ClientMainWindow main window object.
    Connects signals and slots. Launches the main window, closes it when
    the client part of the messenger is shut down.

    **Parameters**

    * obj (Client):
        an instance of the Client class, the main element of the client's
        backend messenger parts.
    """
    application = QApplication(sys.argv)
    window = ClientMainWindow(obj)
    window.make_connection()
    window.show()
    application.exec_()
    obj.thread_run = False


if __name__ == '__main__':
    test_application = QApplication(sys.argv)
    test_obj = TestRequestingObj()
    test_window = ClientMainWindow(test_obj)
    test_window.show()
    sys.exit(test_application.exec())
