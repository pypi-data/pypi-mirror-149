"""
*coding: utf-8
Form implementation generated from reading ui file 'client.ui'
Created by: PyQt5 UI code generator 5.11.3*

Модуль main_window_ui предназначен для создания основных элементов главного окна
и определения его характеристик.

**Классы**

* Ui_MainClientWindow
    Основной класс характеристик графической оболочки клиентской части
    мессенджера.

The main_window_ui module is designed to create the main elements of the main window
of the client's part of messenger and determine its characteristics.

**Classes**

* Ui_Main Client Window
    The main class of characteristics of the graphical shell of the client's
    part of messenger.
"""
from PyQt5 import QtCore, QtWidgets


class Ui_MainClientWindow(object):
    """
    Класс Ui_MainClientWindow используется для создания основных элементов
    главного окна и определения его характеристик.

    **Методы**

    * setupUi(MainClientWindow):
        определяет геометрию, состав и характеристики элементов дизайна
        главного окна клиентской части мессенджера
    * retranslateUi(MainClientWindow)):
        определяет заголовки и текстовое обозначение элементов дизайна главного
        окна клиентской части мессенджера.

    The Ui_Main Client Window class is used to create basic elements
    of the main window and the definition of its characteristics.

    **Methods**

    * setupUi(Main Client Window):
        defines the geometry, composition and characteristics of design
        elements of the main window of the client part of the messenger
    * retranslateUi(MainClientWindow)):
        defines the headings and the text designation of the design elements
        of the main window of the client part of the messenger.
    """
    def setupUi(self, MainClientWindow):
        """
        Определяет геометрию, состав и характеристики элементов дизайна
        главного окна клиентской части мессенджера.

        **Параметры**

        * MainClientWindow (MainClientWindow):
            объект класса MainClientWindow

        Defines the geometry, composition and characteristics of the
        design elements of the main window of the client part of the messenger.

        **Parameters**

        * MainClientWindow (MainClientWindow):
            an object of the MainClientWindow class
        """
        MainClientWindow.setObjectName("MainClientWindow")
        MainClientWindow.resize(756, 534)
        MainClientWindow.setMinimumSize(QtCore.QSize(756, 534))
        self.centralwidget = QtWidgets.QWidget(MainClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_contacts = QtWidgets.QLabel(self.centralwidget)
        self.label_contacts.setGeometry(QtCore.QRect(10, 0, 101, 16))
        self.label_contacts.setObjectName("label_contacts")
        self.btn_add_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QtCore.QRect(10, 450, 121, 31))
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_remove_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remove_contact.setGeometry(QtCore.QRect(140, 450, 121, 31))
        self.btn_remove_contact.setObjectName("btn_remove_contact")
        self.label_history = QtWidgets.QLabel(self.centralwidget)
        self.label_history.setGeometry(QtCore.QRect(300, 0, 391, 21))
        self.label_history.setObjectName("label_history")
        self.text_message = QtWidgets.QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QtCore.QRect(300, 360, 441, 71))
        self.text_message.setObjectName("text_message")
        self.label_new_message = QtWidgets.QLabel(self.centralwidget)
        self.label_new_message.setGeometry(QtCore.QRect(300, 330, 450, 16))  # Правка тут
        self.label_new_message.setObjectName("label_new_message")
        self.list_contacts = QtWidgets.QListView(self.centralwidget)
        self.list_contacts.setGeometry(QtCore.QRect(10, 20, 251, 411))
        self.list_contacts.setObjectName("list_contacts")
        self.list_messages = QtWidgets.QListView(self.centralwidget)
        self.list_messages.setGeometry(QtCore.QRect(300, 20, 441, 301))
        self.list_messages.setObjectName("list_messages")
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(610, 450, 131, 31))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(460, 450, 131, 31))
        self.btn_clear.setObjectName("btn_clear")
        MainClientWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainClientWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainClientWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainClientWindow)
        self.statusBar.setObjectName("statusBar")
        MainClientWindow.setStatusBar(self.statusBar)
        self.menu_exit = QtWidgets.QAction(MainClientWindow)
        self.menu_exit.setObjectName("menu_exit")
        self.menu_add_contact = QtWidgets.QAction(MainClientWindow)
        self.menu_add_contact.setObjectName("menu_add_contact")
        self.menu_del_contact = QtWidgets.QAction(MainClientWindow)
        self.menu_del_contact.setObjectName("menu_del_contact")
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.menu_add_contact)
        self.menu_2.addAction(self.menu_del_contact)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainClientWindow)
        self.btn_clear.clicked.connect(self.text_message.clear)
        QtCore.QMetaObject.connectSlotsByName(MainClientWindow)

    def retranslateUi(self, MainClientWindow):
        """
        Определяет заголовки и текстовое обозначение элементов дизайна главного
        окна клиентской части мессенджера.

        **Параметры**

        * MainClientWindow (MainClientWindow):
            объект класса MainClientWindow

        Defines the headers and the text designation of the design elements of
        the main window of the client part of the messenger.

        **Parameters**

        * Main Client Window (MainClientWindow):
            an object of the MainClientWindow class
        """
        _translate = QtCore.QCoreApplication.translate
        MainClientWindow.setWindowTitle(_translate("MainClientWindow", "Чат Программа"
                                                                       "alpha release"))
        self.label_contacts.setText(_translate("MainClientWindow", "Список контактов:"))
        self.btn_add_contact.setText(_translate("MainClientWindow", "Добавить контакт"))
        self.btn_remove_contact.setText(_translate("MainClientWindow", "Удалить контакт"))
        self.label_history.setText(_translate("MainClientWindow", "История сообщений:"))
        self.label_new_message.setText(_translate("MainClientWindow", "Введите новое сообщение:"))
        self.btn_send.setText(_translate("MainClientWindow", "Отправить сообщение"))
        self.btn_clear.setText(_translate("MainClientWindow", "Очистить поле"))
        self.menu.setTitle(_translate("MainClientWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainClientWindow", "Контакты"))
        self.menu_exit.setText(_translate("MainClientWindow", "Выход"))
        self.menu_add_contact.setText(_translate("MainClientWindow", "Добавить контакт"))
        self.menu_del_contact.setText(_translate("MainClientWindow", "Удалить контакт"))
