"""
Модуль client_db необходим для работы с базой данных Клиента.

Основным классом является ClientStorage, в интерфейсе которого
реализуется взаимодействие с таблицами базы данных, создание записей,
изменение и удаление.

The module client_db is required to work with the Client database.

The main class is ClientStorage, within the interface of which
interaction with database tables, data acquisition and modification
is implemented.
"""

import datetime
import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientStorage:
    """
    Класс ClientStorage используется для создания и взаимодействия с базой
    данных Клиента. Методы класса предназначены для создания, изменения и
    удаления записей в таблицах.

        **Подклассы**

        * KnownUsers
            класс для создания таблицы зарегистрированных пользователей
        * MessageHistory
            класс для создания таблицы истории сообщений
        * Contacts
            класс для создания таблицы контактов

        **Переменные класса**

        * session : Session
            экземпляр класса Session,
            позволяет работать с сессией базы данных
        * metadata : MetaData
            экземпляр класса MetaData,
            позволяет работать со связанными таблицами

        **Методы**

        * safe_commit():
            безопасный commit сессии
        * add_contact(buddy)
            добавление контакта
        * del_contact(buddy)
            удаление контакта
        * get_contacts()
            запрос контактов Клиента
        * add_users(users_list)
            актуализирует данные о зарегистрированных пользователях
        * get_users()
            возвращает данные об известных зарегистрированных пользователях
        * check_in_known(username)
            проверяет, есть ли пользователь среди известных
            зарегистрированных пользователей
        * check_in_contacts(contact_name)
            проверяет, есть ли пользователь среди контактов
        * save_message(author, to_whom, message)
            сохраняет сообщение в истории сообщений Клиента
        * get_msg_history(self, author=None, to_whom=None, buddy_history=None, limit=None):
            возвращает историю сообщений Клиента с указанными параметрами

    The ClientStorage class is used to create and interact with the
    Client database. The methods of the class are designed to create,
    modify, and delete records in tables.

        **Subclasses**

        * KnownUsers
            a class for creating a table of registered users
        * MessageHistory
            a class for creating a message history table
        * Contacts
            class for creating a contact table

        **Class variables**

        * session : Session
            instance of the Session class,
            allows you to work with a database session
        * metadata : MetaData
            instance of the MetaData class,
            allows you to work with related tables

        **Methods**

        * safe_commit():
            secure commit session
        * add_contact(buddy)
            adding a contact
        * del_contact(buddy)
            deleting a contact
        * get_contacts()
            request for Client contacts
        * add_users(users_list)
            updates data about registered users
        * get_users()
            returns data about known registered users
        * check_in_known(username)
            checks if there is a user among the known registered users
        * check_in_contacts(contact_name)
            checks if the user is among the contacts
        * save_message(author, to_whom, message)
            saves the message in the Client's message history
        * get_msg_history(self, author=None, to_whom=None, buddy_history=Note, limit=None):
            returns the history of Client messages with the specified parameters
        """

    class KnownUsers:
        """
        Класс KnownUsers требуется для создания одноименной таблицы.
        В ней хранятся данные обо всех пользователях, зарегистрированных
        в мессенджере.

            **Параметры**

            * user (str)
                имя пользователя

            **Атрибуты**

            * id : int
                уникальный идентификатор записи
            * username : str
                имя (никнейм) зарегистрированного клиента

        The KnownUsers class is required to create a table of the same name.
        It stores data about all users registered in the messenger.

            **Parameters**

                * user (str):
                    user name

            **Attributes**

            * id : int
                unique record ID
            * username : string
                name (nickname) of the registered client
        """
        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """
        Класс MessageHistory требуется для создания одноименной таблицы.
        В ней хранится история всех сообщений, полученных и отправленных Клиентом.

            **Аргументы**

            * author (str):
                имя отправителя сообщения
            * to_whom (str):
                имя получателя сообщения
            * message (str):
                текст сообщения

            **Переменные класса**

            * id : int
                уникальный идентификатор записи
            * author : str
                имя отправителя сообщения
            * to_whom : str
                имя получателя сообщения
            * message : str
                текст сообщения
            * date : datetime
                время создания записи

        The MessageHistory class is required to create a table of the same name.
        It stores the history of all messages received and sent by the Client.

            **Arguments**

            * author (str):
                name of the message sender
            * to_whom (str):
                name of the message recipient
            * message (str):
                message text

            **Class variables**

            * id : int
                unique record ID
            * author : stratos
                name of the sender of the message
            * to_whom : str
                name of the message recipient
            * message : string
                message text
            * date : datetime
                time of record creation
        """
        def __init__(self, author, to_whom, message):
            self.id = None
            self.author = author
            self.to_whom = to_whom
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """
        Класс Contacts требуется для создания одноименной таблицы.
        В ней хранятся все контакты Клиента.

            **Аргументы**

            * contact_name (str):
                имя собеседника Клиента

            **Переменные класса**

            * id : int
                уникальный идентификатор записи
            * name : str
                имя собеседника Клиента

        The Contacts class is required to create a table of the same name.
        It stores all the Client's contacts.

            **Arguments**

            * contact_name (str):
                name of the Client's interlocutor

            **Class variables**

            * id : int
                unique record ID
            * name : string
                name of the Client's interlocutor
        """
        def __init__(self, contact_name):
            self.id = None
            self.name = contact_name

    def __init__(self, client_name):
        """
        Инициация класса ClientStorage.
        Определяется путь для создаваемого файла базы данных, выполняется
        создание таблиц Contacts, MessageHistory и KnownUsers. Выполняется
        создание объекта сессии. Таблица Contacts очищается для удаления
        старых контактов. Выполняется безопасный commit.

            **Параметры**

            * client_name (str):
                имя Клиента

        Initiation of the ClientStorage class.
        The path for the database file being created is determined, and
        creating Contacts, MessageHistory, and KnownUsers tables. Сreating
        a session object. The Contacts table is being cleared for old contacts
        deletion. A secure commit is being executed.

        **Parameters**

        * client_name (str):
            Client's name
        """

        path = os.getcwd()
        self.database_engine = create_engine(f'sqlite:///{os.path.join(path, client_name)}',
                                             echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        known_users = Table('known_users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('username', String)
                            )

        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('author', String),
                                Column('to_whom', String),
                                Column('message', Text),
                                Column('date', DateTime)
                                )

        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        self.metadata.create_all(self.database_engine)

        mapper(self.KnownUsers, known_users)
        mapper(self.MessageHistory, message_history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.query(self.Contacts).delete()
        self.safe_commit()

    def safe_commit(self):
        '''
        Безопасный commit сессии.
        Пробует выполнить commit сессии, при возникновении ошибки
        выводит текст ошибки и выполняет rollback сессии.

        Secure commit session.
        Tries to execute a commit session, if an error occurs
        outputs the error text and performs a rollback session.
        '''
        if self.session:
            try:
                self.session.commit()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                self.session.rollback()

    def add_contact(self, buddy):
        '''
        Создание нового контакта для Клиента, новой записи в таблице Contacts.
        Проверяет, существует ли контакт в таблице, если нет, создает его
        и выполняет безопасный коммит (метод safe_commit()).

        **Параметры**

        * buddy (str):
            имя собеседника, с которым создается контакт.

        Creating a new contact for the Client, a new entry in the Contacts table.
        Checks if the contact exists in the table, if not, creates it
        and performs a safe commit (safe_commit() method).

        **Parameters**

        * buddy (str):
            the name of the interlocutor to be created with contact.
        '''
        user_contact = self.session.query(self.Contacts).filter_by(name=buddy).scalar()
        if not user_contact:
            new_contact = self.Contacts(buddy)
            self.session.add(new_contact)
            self.safe_commit()

    def del_contact(self, buddy):
        '''
        Удаление контакта Клиента и записи в таблице Contacts.
        Делает запрос к таблице Contacts и удаляет найденную запись.

        **Параметры**

        * buddy (str):
            имя собеседника, с которым удаляется контакт.

        Deleting a Client contact and an entry in the Contacts table.
        Makes a query to the Contacts table and deletes the found record.

        **Parameters**

        * buddy (str):
            the name of the interlocutor to be deleted from contact.
        '''
        self.session.query(self.Contacts).filter_by(name=buddy).delete()

    def get_contacts(self):
        '''
        Запрашивает все контакты Клиента, делая запрос к таблице Contacts.

        **Возвращаемое значение**

        * contacts_names(list):
            список name всех записей в таблице Contacts.

        Requests all Client's contacts by making a request to the Contacts table.

        **Return value**

        * contacts_names(list):
            list of names of all entries in the Contacts table.
        '''
        contacts_all = self.session.query(self.Contacts.name).all()
        contacts_names = list(map(lambda x: x[0], contacts_all))
        return contacts_names

    def add_users(self, users_list):
        '''
        Актуализирует данные Клиента о зарегистрированных пользователях мессенджера.
        Очищает таблицу KnownUsers от старых записей и заполняет ее новыми,
        полученными от сервера.

        **Параметры**

        * users_list (list):
            список зарегистрированных пользователей.

        Updates the Client's data about the registered users of the messenger.
        Clears the KnownUsers table of old records and fills it with new ones,
        received from the server.

        **Parameters**

        * users_list (list):
            list of registered users.
        '''
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            record = self.KnownUsers(user)
            self.session.add(record)
        self.safe_commit()

    def get_users(self):
        '''
        Запрашивает всех зарегистрированных пользователей, известных Клиенту,
        делая запрос к таблице KnownUsers.

        **Возвращаемое значение**

        * users_names(list):
            список name всех записей в таблице KnownUsers.

        Requests all registered users known to the Client,
        by making a query to the KnownUsers table.
        **Return value**

        * users_names(list):
            list of names of all entries in the KnownUsers table.
        '''
        users_all = self.session.query(self.KnownUsers.username).all()
        users_names = list(map(lambda x: x[0], users_all))
        return users_names

    def check_in_known(self, username):
        '''
        Проверяет, есть ли собеседник среди известных Клиенту пользователей.
        Делает запрос, существует ли запись в таблице KnownUsers.

        **Параметры**

        * username (str):
            имя проверяемого собеседника.

        **Возвращаемое значение**

        * True:
            если запись существует.
        * False:
            если запись отсутствует.

        Checks whether the interlocutor is among the users known to the Client.
        Makes a query whether an entry exists in the KnownUsers table.

        **Parameters**

        * username (str):
            the name of the person being checked.

        **Return value**

        * True:
            if the record exists.
        * False:
            if there is no record.
        '''
        user = self.session.query(self.KnownUsers).filter_by(username=username).scalar()
        return bool(user)

    def check_in_contacts(self, contact_name):
        '''
        Проверяет, есть ли собеседник среди контактов Клиента.
        Делает запрос, существует ли запись в таблице Contacts.

        **Параметры**

        * contact_name (str):
            имя проверяемого собеседника.

        **Возвращаемое значение**

        * True:
            если запись существует.
        * False:
            если запись отсутствует.

        Checks if there is an interlocutor among the Client's contacts.
        Requests whether an entry exists in the Contacts table.

        **Parameters**

        * contact_name (str):
            the name of the person being checked.

        **Return value**

        * True:
            if the record exists.
        * False:
            if there is no record.
        '''
        user = self.session.query(self.Contacts).filter_by(name=contact_name).scalar()
        return bool(user)

    def save_message(self, author, to_whom, message):
        '''
        Сохраняет сообщение, полученное или отправленное Клиентом.
        Создает запись в таблице MessageHistory.

        **Параметры**

        * author (str):
            имя отправителя сообщения.
        * to_whom (str):
            имя получателя сообщения.
        * message (str):
            текст сообщения.

        Saves the message received or sent by the Client.
        Creates an entry in the MessageHistory table.

        **Parameters**

        * author (str):
            the name of the sender of the message.
        * to_whom (str):
            the name of the recipient of the message.
        * message (str):
            the text of the message.
        '''
        msg_record = self.MessageHistory(author, to_whom, message)
        self.session.add(msg_record)
        self.safe_commit()

    def get_msg_history(self, author=None, to_whom=None,
                        buddy_history=None, limit=None):
        '''
        Запрашивает историю сообщений Клиента. Изначально запрашивается
        вся история (все полученные и отправленные сообщения для всех
        собеседников).

        При передаче значения author будут отсортированы записи, где автором
        сообщения является указанный собеседник.

        При передаче значения to_whom будут отсортированы записи, где получателем
        сообщения является указанный собеседник.

        При передаче значения buddy_history будут отсортированы записи, где автором
        или получателем сообщения является указанный собеседник.

        При передаче значения limit возвращаемый результат будет ограничен указанным
        количеством строк данных.

        **Параметры**

        * author (str):
            имя отправителя сообщения.
        * to_whom (str):
            имя получателя сообщения.
        * buddy_history (str):
            имя собеседника, для которого запрашивается двусторонняя история сообщений.
        * limit (int):
            ограничение количества возвращаемых сообщений.

        Requests the Client's message history. Initially requested
        the whole history (all received and sent messages for everyone
        interlocutors).

        When passing the author value, the records will be sorted, where the author
        of message is the specified interlocutor.

        When passing the value to_whom, the records will be sorted, where the recipient
        of message is the specified interlocutor.

        When passing the value of buddy_history, the records will be sorted, where the author
        or the recipient of the message is the specified interlocutor.

        When passing the limit value, the returned result will be limited to the specified
        number of rows of data.

        **Parameters**

        * author (str):
            the name of the sender of the message.
        * to_whom (str):
            the name of the recipient of the message.
        * buddy_history (str):
            the name of the interlocutor for whom a two-way message history is requested.
        * limit (int):
            limiting the number of messages returned.
        '''
        query = self.session.query(self.MessageHistory)
        if buddy_history:
            query = query.filter((self.MessageHistory.author == buddy_history)
                                 | (self.MessageHistory.to_whom == buddy_history)).order_by(
                self.MessageHistory.date.desc())
            if limit:
                try:
                    query = query.limit(int(limit))
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
        elif author:
            query = query.filter_by(author=author)
        elif to_whom:
            query = query.filter_by(to_whom=to_whom)
        return [(elem.author, elem.to_whom, elem.message, elem.date)
                for elem in query.all()]


if __name__ == '__main__':
    print('Создаем тестовую базы для client_1')
    test_db = ClientStorage('client_1')
    print('Добавляем список известных пользователей')
    test_db.add_users(['client_1', 'client_2', 'client_3', 'client_4'])
    print(f'Тест запроса известных пользователей: {test_db.get_users()}')

    print(f'Тест проверки нахождения в известных пользователях '
          f'client_3: {test_db.check_in_known("client_3")}')
    print(f'Тест проверки нахождения в известных пользователях '
          f'client_333: {test_db.check_in_known("client_333")}')

    print('Добавляем для client_1 контакты: client_2, client_3')
    test_db.add_contact('client_2')
    test_db.add_contact('client_3')
    print(f'Тест запроса контактов: {test_db.get_contacts()}')

    print('Удаляем для client_1 контакт: client_2')
    test_db.del_contact('client_3')
    print(f'Тест запроса контактов: {test_db.get_contacts()}')

    print('Отправляем сообщение пользователю client_1 от client_2')
    test_db.save_message('client_1', 'client_2',
                         'Как может брошенное яйцо пролететь три метра и не разбиться?')
    print(f'Тест истории сообщений client_1: {test_db.get_msg_history()}')
    print(f'Тест истории сообщений (от кого=client_2): {test_db.get_msg_history("client_2")}')
    print(f'Тест истории сообщений (кому=client_2): {test_db.get_msg_history(to_whom="client_2")}')

    print('Отправляем сообщение пользователю client_2 от client_1')
    test_db.save_message('client_2', 'client_1', 'Нужно бросить яйцо на четыре метра.')
    print(f'Тест истории сообщений client_1: {test_db.get_msg_history()}')
    print(f'Тест истории сообщений (от кого=client_2): {test_db.get_msg_history("client_2")}')
    print(f'Тест истории сообщений (кому=client_2): {test_db.get_msg_history(to_whom="client_2")}')

    print(f'Тест истории сообщений (кому=client_4): {test_db.get_msg_history(to_whom="client_4")}')
    print(f'Тест истории сообщений (кому=client_4): {test_db.get_msg_history(to_whom="client_4")}')
    print(f'Тест истории сообщений (buddy_history=client_2): '
          f'{test_db.get_msg_history(buddy_history="client_2")}')
    print(f'Тест истории сообщений (buddy_history=client_2, лимит: 1): '
          f'{test_db.get_msg_history(buddy_history="client_2", limit=1)}')
