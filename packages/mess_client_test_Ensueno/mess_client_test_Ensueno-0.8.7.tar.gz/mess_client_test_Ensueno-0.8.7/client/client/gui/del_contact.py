"""
Модуль del_contact предназначен для создания и полноценной работы
окна удаления контакта.

Основным классом является DelContactDialog, в интерфейсе которого
реализуется создание окна удаления контакта и инициация списка контактов Клиента.

The del_contact module is designed for creation and full-fledged work
contact deletion windows.

The main class is DelContactDialog, in the interface of which the creation of
a contact deletion window and the initiation of the Client's contact list is implemented.
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication

logger = logging.getLogger('client')


class DelContactDialog(QDialog):
    """
    Класс DelContactDialog используется для создания окна удаления контакта
    и инициации контактов Клиента.
    Дочерний класс класса QDialog.

    **Атрибуты**

    * database : ClientStorage
        экземпляр класса ClientStorage, основной элемент взаимодействия
        с базой данных Клиента.

    The DelContactDialog class is used to create a window for deleting a contact
    and initiating Client contacts.
    A child class of the QDialog class.

    **Attributes**

    * database : ClientStorage
        an instance of the ClientStorage class, the main element of
        interaction with the Client database
    """
    def __init__(self, database):
        """
        Инициация класса DelContactDialog.
        Наследование от родительского класса QDialog. Задание геометрии, поведения и
        определение PyQT-элементов окна удаления контактов. Запрос контактов
        Клиента из его базы данных.

        **Параметры**

        * database : ClientStorage
            экземпляр класса ClientStorage, основной элемент взаимодействия
            с базой данных Клиента.

        Initiation of the DelContactDialog class.
        Inheritance from the parent QDialog class. Setting geometry, behavior, and
        definition of PyQt elements of the contact deletion window. Request Сlient's
        contacts from his database.

        **Parameters**

        * database : ClientStorage
            an instance of the ClientStorage class, the main element of interaction
            with the Client's database.
        """
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для удаления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для удаления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.selector.addItems(sorted(self.database.get_contacts()))


if __name__ == '__main__':
    app = QApplication([])
    window = DelContactDialog(None)
    window.show()
    app.exec_()
