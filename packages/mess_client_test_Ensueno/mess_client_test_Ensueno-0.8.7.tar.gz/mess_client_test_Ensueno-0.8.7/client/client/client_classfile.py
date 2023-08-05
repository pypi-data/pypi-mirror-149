"""
client_classfile
----------------

Модуль client_classfile содержит основной бекэнд клиентской части мессенджера.
Реализует взаимодействие графических элементов пользовательского интерфейса,
базы данных и функционала обмена данными с сервером.

**Классы**

* ClientDataPreparation
    Вспомогательный класс для подготовки данных для основного класса Client.
    Получает данные о номере порта сервера и его ip-адресе, логине (имени)
    и пароле Клиента из параметров командной строки. При их отсутствии для
    порта и адреса сервера назначаются дефолтные значения, а имя и логин
    Клиента запрашиваются у него посредством стартового окна.
    При работе этого класса выполняется логирование, реализованное посредством
    декоратора Log.
* Client
    Основной класс бэкенда клиентской части мессенджера. Имеет потоковую
    реализацию, используется дескриптор для атрибута server_port. Выполняется
    логирование, реализованное посредством декоратора Log.

The client_class file module contains the main backend of the messenger client
part. Implements the interaction of graphical elements of the user interface,
database and data exchange with the server functionality.

**Classes**

* Client Data Preparation
    Auxiliary class for preparing data for the main Client class.
    Retrieves data about the server port number and its IP address,
    login (name) and password of the Client from the command line parameters.
    In their absence, default values are assigned to the server port and
    address, and the name and login of client is requested through the start
    window. When running instances of this class, logging is performed,
    implemented by Log decorator.
* Client
    The main class of the backend of the client part of the messenger.
    It has a streaming implementation, a handle for the server_port
    attribute is used. Logging is performed, implemented using the Log
    decorator.
"""
import argparse
import binascii
import hashlib
import hmac
import json
import logging
import os
import sys
import threading
import time
import traceback
from Cryptodome.PublicKey import RSA
from PyQt5.QtCore import QObject

from client.db.client_db import ClientStorage
from client.gui.welcome_window import noname_client_welcome, user_warning
from common.decorators import Log
from common.descriptors import Port
from common.errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
from common.parent_classfile import App
from common.vars import DEFAULT_IP_ADDRESS, \
    ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR, \
    DEFAULT_PORT, MESSAGE_TEXT, MESSAGE, SENDER, DESTINATION, \
    EXIT, FAQ, GET_CONTACTS, LIST_INFO, ADD_CONTACT, REMOVE_CONTACT, \
    USERS_REQUEST, PUBLIC_KEY, DATA, RESPONSE_511, PUBLIC_KEY_REQUEST


@Log()
class ClientDataPreparation:
    """
    Вспомогательный класс для подготовки данных для основного класса Client.
    Получает данные о номере порта сервера и его ip-адресе, логине (имени)
    и пароле Клиента из параметров командной строки. При их отсутствии для
    порта и адреса сервера назначаются дефолтные значения, а имя и логин
    Клиента запрашиваются у него посредством стартового окна.
    При работе этого класса выполняется логирование, реализованное посредством
    декоратора Log.

    **Атрибуты**

    * logger
        объект для логирования работы данного класса
    * parser : ArgumentParser
        объект для парсинга данных командной строки

    **Методы**

    * client_parse_args():
        парсит данные ip-адреса и порта сервера, логина и пароля Клиента из
        командной строки, передает их для дальнейшей валидации методу
        validate_name_paswd(), возвращает полученные и обработанные данные.
    * validate_name_paswd(namespace):
        выполняет валидацию логина и пароля Клиента (их отсутствие, имя менее 4
        символов, имя только из цифр, пароль менее 5 символов), возвращает
        валидные значения.

    Auxiliary class for preparing data for the main Client class.
    Retrieves data about the server port number and its IP address,
    login (name) and password of the Client from the command line parameters.
    In their absence, default values are assigned to the server port and
    address, and the name and login of client is requested through the start
    window. When running instances of this class, logging is performed,
    implemented by Log decorator.

    **Attributes**

    * logger
        an object for logging the work of this class
    * parser : ArgumentParser
        an object for parsing command line data

    **Methods**

    * client_parse_args():
        parses the ip address and port data of the server, the login and
        password of the Client from the command line, passes them to the
        validate_name_paswd() method for further validation, returns the
        received and processed data.
    * validate_name_paswd(namespace):
        performs validation of the Client's login and password (their
        absence, the name is less than 4 characters, name only of digits,
        password less than 5 characters), returns valid values.
    """
    def __init__(self):
        """
        Инициация класса ClientDataPreparation.
        Параметры:
        ----------
        * logger
            объект для логирования работы данного класса
        * parser : ArgumentParser
            объект для парсинга данных командной строки

        Initiation of the Client Data Preparation class.
        Parameters:
        ----------
        * logger
            an object for logging the work of this class
        * parser : ArgumentParser
            an object for parsing command line data
        """
        self.logger = logging.getLogger('app.client_script')
        self.parser = argparse.ArgumentParser()

    def client_parse_args(self):
        """
        Получает из командной строки данные ip-адреса и порта сервера, логина(имени)
        и пароля Клиента. Допустимо отсутствие значений, при этом для порта и
        адреса будут назначены дефолтные значения, а логин и пароль будут
        запрошены у пользователя. Вызывает метод validate_name_paswd() для
        валидизации логина и пароля Клиента. Возвращает валидные значения порта,
        адреса, логина и пароля.

        **Возвращаемое значение:**

        * server_address(str): ip-адрес порта сервера
        * server_port(int): номер порта сервера
        * client_name(str): имя Клиента
        * client_passwd(str): пароль Клиента.

        Receives from the command line the data of the server's IP address and
        port, login (name) and password of the Client. The absence of values
        is acceptable, while default values will be assigned for the port and
        address, and the login and password will be requested from the user.
        Calls the validate_name_paswd() method for validating the Client's login
        and password. Returns valid port, address, login, and password values.

        **Return value:**

        * server_address(str): ip address of the server port
        * server_port(int): server port number
        * client_name(str): Client's name
        * client_password(str): Client's password.
        """
        self.parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        self.parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        self.parser.add_argument('-n', '--name', default=None, nargs='?')
        self.parser.add_argument('-p', '--password', default='', nargs='?')

        namespace = self.parser.parse_args(sys.argv[1:])

        try:
            server_address, server_port = namespace.addr, namespace.port
        except AttributeError:
            self.logger.critical(f'Ошибка валидации порта. Парсер аргументов командной'
                                 f'строки не обнаружил атрибутов \'addr\' или \'port\' '
                                 f'Завершение работы клиента.')
            sys.exit(1)
        client_name, client_passwd = self.validate_name_paswd(namespace)
        return server_address, server_port, client_name, client_passwd

    def validate_name_paswd(self, namespace):
        """
        Выполняет валидацию логина(имени) и пароля Клиента. При их отсутствии
        инициирует запуск стартового окна и запрашивает их у пользователя.
        Возвращает валидные значения логина и пароля.

        **Параметры:**

        * namespace: данные, полученные из командной строки.

        **Возвращаемое значение:**

        * client_name(str): имя Клиента
        * client_passwd(str): пароль Клиента

        Performs validation of the login (name) and password of the Client.
        In their absence, initiates the launch of the start window and requests
        them from the user. Returns valid login and password values.

        **Parameters:**

        * namespace: data received from the command line.

        **Return value:**

        * client_name(str): Client's name
        * client_password(str): Client's password
        """
        client_name = namespace.name
        client_passwd = namespace.password
        if not client_name or not client_passwd:
            while True:
                client_name, client_passwd = noname_client_welcome(client_name, client_passwd)
                if not client_name or not client_passwd:
                    user_warning('Вы не ввели входные данные!', 'Приложение завершается')
                    sys.exit(0)
                else:
                    if client_name.isdigit():
                        user_warning('Имя из цифр недопустимо!', 'Попробуйте еще раз')
                    elif len(client_name) <= 3:
                        user_warning('Имя короче 4 символов недопустимо!', 'Попробуйте еще раз')
                    elif len(client_passwd) < 5:
                        user_warning('Пароль короче 5 символов недопустим!', 'Попробуйте еще раз')
                    else:
                        break
                    client_name, client_passwd = None, None
        return client_name, client_passwd


@Log()
class Client(App, threading.Thread, QObject):
    # """
    # Основной класс бэкенда клиентской части мессенджера. Имеет потоковую
    # реализацию, используется дескриптор для атрибута server_port, проверяющий
    # валидность его значения. Выполняется логирование, реализованное посредством
    # декоратора Log.
    #
    # **Переменные класса**
    #
    # * self.name : str
    #     вспомогательное наименование
    # * self.logger
    #     объект для логирования работы класса
    # * self.server_address : str
    #     ip-адрес порта сервера
    # * self.server_port : int
    #     номер порта сервера
    # * self.client_name : str
    #      логин пользователя
    # * self.password : str
    #     пароль пользователя
    # * self.database : ClientStorage
    #     объект базы данных конкретного Клиента
    # * self.sock_lock : threading.Lock()
    #     простой объект блокировки потока
    # * self.database_lock : threading.Lock()
    #     простой объект блокировки потока для работы с базой данных
    # * self.thread_run = True
    #     флаг необходимости продолжения работы потока
    # * self.keys
    #     ключи Клиента для аутентификации
    # * self.passwd_hash_string
    #     hash-строка пароля для аутентификации
    # * self.pubkey
    #     публичный ключ Клиента
    # * self.current_chat_key
    #     публичный ключ текущего собеседника
    #
    # **Методы**
    #
    # * key_load():
    # * auth_dialog():
    # * client_connect():
    # * send_a_message(self, pubkey=None, action=PRESENCE)
    # * response_read():
    # * database_load():
    # * user_list_request(self, repeated=False)
    # * contacts_list_request():
    # * send_or_listen():
    # * message_from_server():
    # * key_request(self, user)
    # * create_message(self, to_user, user_message)
    # * add_contact(self, username)
    # * del_contact(self, username)
    # * say_goodbye_and_exit():
    # * run():
    # """
    server_port = Port()

    def __init__(self, addr, port, name, pswd):
        """
        Инициация класса ClientStorage.

        **Параметры:**

        * addr (str):
            ip-адрес сервера
        * port (int):
            порт сервера
        * name (str):
            логин(имя) Клиаента
        * pswd (str):
            пароль Клиента

        Initiation of the ClientStorage class.

        **Parameters:**

        * addr (str):
            server ip address
        * port (int):
            server port
        * name (str):
            the Client's login (name)
        * pswd (str):
            Client password
        """
        App.__init__(self)
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.name = 'Client'
        self.logger = logging.getLogger('app.client_script')
        self.server_address = addr
        self.server_port = port
        self.client_name = name
        self.password = pswd
        self.database = None
        self.sock_lock = threading.Lock()
        self.database_lock = threading.Lock()
        self.thread_run = True
        self.keys = None
        self.passwd_hash_string = None
        self.pubkey = None
        self.current_chat_key = None

    def key_load(self):
        dir_path = os.getcwd()
        key_file = os.path.join(dir_path, f'{self.client_name}.key')
        if not os.path.exists(key_file):
            self.keys = RSA.generate(2048, os.urandom)
            with open(key_file, 'wb') as key:
                key.write(self.keys.export_key())
        else:
            with open(key_file, 'rb') as key:
                self.keys = RSA.import_key(key.read())

        self.logger.debug(f"Ключи клиента {self.client_name} успешно загружены")
        print(f"Ключи клиента {self.client_name} успешно загружены")

    def auth_dialog(self):
        passwd_bytes = self.password.encode('utf-8')
        salt = self.client_name.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        self.passwd_hash_string = binascii.hexlify(passwd_hash)
        self.logger.debug(f'Для {self.client_name} подготовлен хэш пароля: {self.passwd_hash_string}')
        return self.keys.publickey().export_key().decode('ascii')

    def client_connect(self):
        """Establishes a connection to the server"""
        for i in range(5):
            self.logger.info(f'Попытка подключения №{i + 1}')
            print(f'Попытка подключения №{i + 1}')
            try:
                self.socket.connect((self.server_address, self.server_port))
            except (OSError, ConnectionRefusedError):
                print(traceback.format_exc())
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
            else:
                self.connected = True
                break
            time.sleep(1)
        if not self.connected:
            self.logger.critical(f'Клиенту {self.client_name} не удалось установить соединение с сервером')
            raise ServerError(f'Клиенту {self.client_name} не удалось установить соединение с сервером')

        self.logger.debug(f'Успешное подключение к удаленному сокету '
                          f'по адресу {self.server_address}, порт {self.server_port}, '
                          f'имя клиента {self.client_name}')
        self.pubkey = self.auth_dialog()

        try:
            with self.sock_lock:
                self.send_a_message(pubkey=self.pubkey)  #
                time.sleep(0.5)
                response = self.response_read()  #
                self.send_msg(response)
                time.sleep(0.5)
                self.response_read()

        except (OSError, json.JSONDecodeError):
            self.logger.critical(f'{self.client_name} утратил соединение с сервером в процессе авторизации.')
            raise ServerError(f'{self.client_name} утратил соединение с сервером в процессе авторизации.')
        self.logger.info('Соединение с сервером успешно установлено.')

        print(f'Добро пожаловать! Ваш никнейм - {self.client_name}.')

    def send_a_message(self, pubkey=None, action=PRESENCE):
        """Sends a message to the server"""

        msg_to_server = {
            ACTION: action,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_name
            }
        }

        if pubkey:
            msg_to_server[USER][PUBLIC_KEY] = pubkey

        self.send_msg(msg_to_server)
        self.logger.info(f'Отправлено сообщение серверу.')

    def response_read(self):
        """Receiving the server response and its output"""

        msg = self.get_message()
        self.logger.info(f'Получено сообщение от сервера {msg}')
        try:
            if RESPONSE in msg:
                if msg[RESPONSE] == 200:

                    if LIST_INFO in msg:
                        return LIST_INFO

                    msg = 'Соединение с сервером установлено'
                    print(msg)
                    self.logger.info(msg + f' , клиент - {self.client_name}')
                    return

                elif msg[RESPONSE] == 202:
                    return msg

                elif msg[RESPONSE] == 205:
                    self.user_list_request()
                    self.contacts_list_request()
                    self.message_205.emit()
                    return

                elif msg[RESPONSE] == 511:
                    data = msg[DATA]
                    hash = hmac.new(self.passwd_hash_string, data.encode('utf-8'), 'MD5')
                    digest = hash.digest()
                    reply = RESPONSE_511

                    reply[USER] = {'account_name': self.client_name, 'pubkey': self.pubkey}
                    reply[DATA] = binascii.b2a_base64(
                        digest).decode('ascii')
                    return reply

                elif msg[RESPONSE] == 400:
                    raise ServerError(f'400 : {msg[ERROR]}')
            raise ReqFieldMissingError(RESPONSE)
        except ValueError:
            self.logger.critical(f'Ошибка в ответе сервера. Клиент завершил работу')
            sys.exit(1)
        except ReqFieldMissingError as missing_error:
            self.logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            sys.exit(1)
        except ConnectionRefusedError:
            self.logger.critical('Ошибка подключения к серверу: сервер отверг запрос на подключение')
            sys.exit(1)

    def database_load(self):
        self.database = ClientStorage(self.client_name)
        with self.sock_lock:
            users_list = self.user_list_request()
            contacts_list = self.contacts_list_request()
        try:
            if users_list:
                self.database.add_users(users_list)
            if contacts_list:
                for contact in contacts_list:
                    self.database.add_contact(contact)
        except Exception:
            self.logger.error(f'Не удалось обновить список известных пользователей '
                              f'и/или контактов по причине {traceback.format_exc()}.')

    def user_list_request(self, repeated=False):
        self.logger.debug(f'Запрос списка известных пользователей для {self.client_name}')
        msg_to_server = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.client_name
        }
        self.send_msg(msg_to_server)
        if not repeated:
            return self.response_read()[LIST_INFO]

    def contacts_list_request(self):
        self.logger.debug(f'Запрос контакт-листа для {self.client_name}')
        msg_to_server = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.client_name
        }
        self.send_msg(msg_to_server)
        return self.response_read()[LIST_INFO]

    def send_or_listen(self):
        """Determines the client's operating mode and forms its actions"""
        receiver = threading.Thread(target=self.message_from_server)
        receiver.daemon = True
        receiver.start()

        while True:
            time.sleep(1)

            if receiver.is_alive():
                continue
            self.logger.warning(f'Потоковый прием или отправка сообщений клиента {self.client_name} завершены.')
            break

    def message_from_server(self):
        """Processes messages from the server and displays them on the terminal screen"""

        while self.thread_run:
            time.sleep(1)

            with self.sock_lock:
                try:
                    message = self.get_message()
                    if message == 'close':
                        break

                    if RESPONSE in message:
                        if message[RESPONSE] == 200:
                            if LIST_INFO in message:
                                print(message[LIST_INFO])
                            else:
                                return
                        elif message[RESPONSE] == 400:
                            raise ServerError(f'{message[ERROR]}')

                        elif message[RESPONSE] == 205:
                            users_list = self.user_list_request()
                            contacts_list = self.contacts_list_request()
                            try:
                                if users_list:
                                    self.database.add_users(users_list)
                                if contacts_list:
                                    for contact in contacts_list:
                                        self.database.add_contact(contact)
                            except Exception as ex:
                                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                                message = template.format(type(ex).__name__, ex.args)
                                print(message)
                            self.message_205.emit()

                        elif message[RESPONSE] == 511:
                            if RESPONSE in message and message[RESPONSE] == 511:
                                self.current_chat_key = message[DATA]
                            else:
                                print('Не удалось получить ключ собеседника.')
                                self.logger.error('Не удалось получить ключ собеседника.')
                        else:
                            self.logger.error(f'Принят неизвестный код подтверждения {message[RESPONSE]}')

                    elif ACTION in message and message[ACTION] == MESSAGE and \
                            SENDER in message and DESTINATION in message \
                            and MESSAGE_TEXT in message and message[DESTINATION] == self.client_name:
                        msg = f'Пользователь {message[SENDER]} ' \
                              f'отправил вам сообщение: \n{message[MESSAGE_TEXT]}'

                        self.logger.info(msg)
                        self.send_new_message.emit(message)
                    else:
                        self.logger.error(f'Ответ сервера в сообщении {message} содержит ошибку')

                except IncorrectDataRecivedError:
                    self.logger.error(f'Не удалось декодировать полученное сообщение.')
                except (OSError, ConnectionError, ConnectionAbortedError,
                        ConnectionResetError, json.JSONDecodeError):
                    print(traceback.format_exc())
                    self.logger.critical(f'Потеряно соединение с сервером.')
                    break

    def key_request(self, user):
        self.logger.debug(f'Запрос публичного ключа для {user}')
        msg = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        self.send_msg(msg)
        time.sleep(1)
        if self.current_chat_key:
            return self.current_chat_key
        else:
            a = self.get_message()
            self.current_chat_key = a[DATA]
            return self.current_chat_key

    def create_message(self, to_user, user_message):
        """Receives a message from the user and forms it for sending"""

        with self.database_lock:
            if not self.database.check_in_known(to_user):
                self.logger.error(f'Попытка отправить сообщение незарегистрированому получателю: {to_user}')
                print('Такого пользователя не существует, выберите другого получателя.')
                return

        message_to_other_client = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: user_message
        }

        try:
            self.send_msg(message_to_other_client)
            self.logger.info(f'Отправлено сообщение для пользователя {to_user}')
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            self.logger.error(f'Разрыв соединения с {self.server_address}.')
            sys.exit(1)
        except Exception:
            self.logger.error(f'{traceback.format_exc()}')

    def add_contact(self, username):
        self.logger.debug(f'Добавление пользователя {username} в контакты')
        msg_to_server = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.client_name,
            ACCOUNT_NAME: username
        }
        self.send_msg(msg_to_server)
        print(f'Пользователь {username} успешно добавлен в контакты')

    def del_contact(self, username):
        self.logger.debug(f'Удаление пользователя {username} из контактов')
        msg_to_server = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.client_name,
            ACCOUNT_NAME: username
        }
        self.send_msg(msg_to_server)
        print(f'Пользователь {username} успешно удален из контактов')

    def say_goodbye_and_exit(self):
        """Sends a client shutdown command to the server"""

        msg = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.client_name
        }
        try:
            self.send_msg(msg)
        except Exception:
            pass
        print('Завершение работы. До свидания!')
        self.database.session.close()
        self.logger.info(f'Завершение работы {self.client_name} по его запросу.')
        self.thread_run = False
        time.sleep(0.5)

    def run(self):
        self.database_load()
        self.send_or_listen()
