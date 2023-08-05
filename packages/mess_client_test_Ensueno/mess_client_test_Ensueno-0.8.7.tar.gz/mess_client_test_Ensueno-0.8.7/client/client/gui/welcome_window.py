"""
Модуль welcome_window предназначен для создания и полноценной работы
стартового окна мессенджера (клиентская часть). Стартовое окно запрашивает у
пользователя его логин и пароль, выполняет валидацию вводимых данных, при
вводе невалидных значений появляется информационное окно с указанием ошибки в данных.

**Классы**

* ClientWelcomeWindow
    Основным классом является ClientWelcomeWindow, в интерфейсе которого
    реализуется создание стартового окна мессенджера.
* NameMissingWindow
    Вспомогательный класс, который инициирует создание окна с указанием
    ошибки во введенных стартовых данных.
* TestRequestingObj
    Дополнительный класс создан для тестирования работоспособности
    основного класса.

**Функции**

* noname_client_welcome(name, pswd):
    инициирует создание объекта стартового окна ClientWelcomeWindow.

    *Параметры*

    + name (str):
        логин пользователя (допускается отсутствие)
    + pswd (str):
        пароль пользователя (допускается отсутствие)

* user_warning(error, msg)
    инициирует создание объекта окна уведомления об ошибке NameMissingWindow.

    *Параметры*

    * error (str):
        текст ошибки пользователя
    * msg (str):
        информационное сообщение пользователю о том, что требуется исправить

The welcome_window module is designed to create and fully operate the messenger's
start window (client part). The start window asks the user for his login and
password, validates the data entered, and when invalid values are entered,
an information window appears indicating an error in the data.

**Classes**

* ClientWelcomeWindow
    The main class is ClientWelcomeWindow, in the interface of which
    the creation of the messenger's start window is implemented.
* NameMissingWindow
    Auxiliary class that initiates the creation of a window with the
    indication of errors in the entered starting data.
* TestRequestingObj
    An additional class has been created for testing the main class.

**Functions**

* noname_client_welcome(name, pswd):
    initiates the creation of the ClientWelcomeWindow start window object.

    *Parameters*

    + name (str):
        user login (absence is allowed)
    + pswd (str):
        user password (absence is allowed)
* user_warning(error, msg)
    initiates the creation of the NameMissingWindow error notification
    window object.

    *Parameters*

    + error (str): user error text
    + msg (str): informational message to the user about what is required fix
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QLabel, qApp, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication


class ClientWelcomeWindow(QWidget):
    """
    Класс ClientWelcomeWindow используется для создания стартового окна клиентской
    части мессенджера, получения данных для первичной валидации вводимых логина
    и пароля.
    Дочерний класс класса QWidget.

    **Атрибуты**

    * name : str
        вводимый пользователем логин (имя)
    * pswd : str
        вводимый пользователем пароль

    **Методы**

    * initUI():
        метод определения характеристик дизайна и состава элементов окна.
    * onChanged(text):
        метод-слот, меняет текст лейбла client_name в соответствии с текстом,
        который вводит пользователь.
    * next_and_close():
        первичная валидация вводимых пользователем данных

    The Client Welcome Window class is used to create the start window of the
    client part of the messenger, to receive data for the initial validation of
    the login input and password.
    A child class of the QWidget class.

    **Attributes**

    * name : str
        user-entered login (name)
    * pswd : str
        user-entered password

    **Methods**

    * initUI():
        a method for determining the design characteristics and composition
        of window elements.
    * onChanged(text):
        method-slot, changes the text of the client_name label in accordance
        with the text that the user enters.
    * next_and_close():
        primary validation of user input data
    """
    def __init__(self, name, pswd):
        """
        Инициация класса ClientWelcomeWindow.
        Наследование от родительского класса QWidget. Вызов
        метода определения характеристик дизайна и состава элементов окна.

        **Параметры**

        * name : str
            вводимый пользователем логин (имя)
        * pswd : str
            вводимый пользователем пароль

        Initiation of the Client Welcome Window class.
        Inheritance from the parent ClientWelcomeWindow class. Calling a method
        for determining the design characteristics and composition of window
        elements.

        **Parameters**

        * name : str
            user-entered login (name)
        * pswd : str
            user-entered password
        """
        super().__init__()
        self.name = name
        self.pswd = pswd
        self.initUI()

    def initUI(self):
        """
        Метод определения характеристик дизайна и состава элементов окна.
        A method for determining the characteristics of the design and
        composition of window elements.
        """
        self.setWindowTitle('Выберите имя')
        self.setFixedSize(200, 280)

        self.info = QLabel(self)
        self.info.move(12, 17)
        self.info.setText('Для начала работы выберите имя')
        self.name_edit = QLineEdit(self)
        self.name_edit.move(33, 47)

        self.lbl_pswd = QLabel(self)
        self.lbl_pswd.move(12, 92)
        self.lbl_pswd.setText('Выберите пароль')
        self.pswd_edit = QLineEdit(self)
        self.pswd_edit.move(33, 122)
        self.pswd_edit.setEchoMode(QLineEdit.Password)

        self.info_name = QLabel(self)
        self.info_name.move(70, 160)
        self.info_name.setText('Войти как:')

        self.client_name = QLabel(self)
        self.client_name.move(60, 180)

        self.cnsl_btn = QPushButton('Выход', self)
        self.cnsl_btn.move(15, 225)

        self.next_btn = QPushButton('Дальше', self)
        self.next_btn.move(110, 225)

        self.next_btn.clicked.connect(self.next_and_close)
        self.name_edit.textChanged[str].connect(self.onChanged)
        self.cnsl_btn.clicked.connect(qApp.exit)

        self.show()

    def onChanged(self, text):
        """
        Метод-слот, меняет текст лейбла client_name в соответствии с текстом,
        который вводит пользователь.

        **Параметры**

        * text (str): вводимый пользователем логин(имя).

        The slot method changes the text of the client_name label according to
        the text that the user enters.

        **Parameters**

        * text (str): login (name) entered by the user.
        """
        self.client_name.setStyleSheet("QLabel{font-size: 18pt;}")
        self.client_name.setText(text)
        self.client_name.adjustSize()

    def next_and_close(self):
        """
        Первичная валидация вводимых пользователем данных, не допускает запуска
        главного окна клиентской части мессенджера, если пользователь не ввел
        пароль или логин.

        **Возвращаемое значение**

        * self.name(str): введенный пользователем логин(имя).
        * self.pswd(str): введенный пользователем пароль.

        The primary validation of the data entered by the user does not allow
        the launch of the main window of the client part of the messenger, if
        the user has not entered a password or login.

        **Return value**

        * self.name (str): the username (name) entered by the user.
        * self.pswd(str): the password entered by the user.
        """
        msg = 'Сначала нужно ввести имя!'
        if self.client_name.text() and self.client_name.text() != msg:
            if self.pswd_edit.text() and self.pswd_edit.text() != msg:
                self.name = self.client_name.text()
                self.pswd = self.pswd_edit.text()
                self.close()
                return self.name, self.pswd
            msg = 'Сначала нужно ввести пароль!'
            self.client_name.setStyleSheet("QLabel{font-size: 8pt; color: red;}")
            self.client_name.setText(msg)
            self.client_name.adjustSize()
        else:
            self.client_name.setStyleSheet("QLabel{font-size: 8pt; color: red;}")
            self.client_name.move(30, 180)
            self.client_name.setText(msg)
            self.client_name.adjustSize()


class NameMissingWindow(QWidget):
    """
    Вспомогательный класс, который инициирует создание окна с указанием ошибки
    во введенных стартовых данных.
    Дочерний класс класса QWidget.

    **Атрибуты**

    * error : str
        информация об ошибке в данных, допущенной пользователем
    * msg : str
        информация о том, что необходимо исправить

    **Методы**

    * initUI():
        метод определения характеристик дизайна и состава элементов окна.

    An auxiliary class that initiates the creation of a window indicating
    an error in the entered starting data.
    A child class of the QWidget class.

    **Attributes**

    * error : str
        information about a data error made by the user
    * msg : str
        information about what needs to be fixed

    **Methods**

    * initUI():
        a method for determining the design characteristics and composition
        of window elements.
    """
    def __init__(self, error, msg):
        """
        Инициация класса NameMissingWindow.
        Наследование от родительского класса QWidget. Вызов метода определения
        характеристик дизайна и состава элементов окна.

        **Параметры**

        * error : str
            информация об ошибке в данных, допущенной пользователем
        * msg : str
            информация о том, что необходимо исправить

        Initiation of the NameMissingWindow class.
        Inheritance from the parent QWidget class. Calling a method for
        determining the design characteristics and composition of window
        elements.

        **Parameters**

        * error : str
            information about a data error made by the user
        * msg : str
            information about what needs to be fixed
        """
        super().__init__()
        self.error = error
        self.msg = msg
        self.initUI()

    def initUI(self):
        """
        Метод определения характеристик дизайна и состава элементов окна.
        A method for determining the characteristics of the design and
        composition of window elements.
        """
        self.setWindowTitle('Ошибка!')
        self.setFixedSize(300, 130)

        self.err_lbl = QLabel(self)
        self.err_lbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.err_lbl.setStyleSheet("QLabel{font-size: 8pt; color: red;}")
        self.err_lbl.setText(f'Ошибка: {self.error}')

        self.info = QLabel(self)
        self.info.setAlignment(Qt.AlignHCenter)
        self.info.setText(self.msg)

        exit_btn = QPushButton('Ок', self)
        exit_btn.clicked.connect(qApp.exit)

        layout = QVBoxLayout(self)
        layout.addWidget(self.err_lbl)
        layout.addWidget(self.info)
        layout.addWidget(exit_btn)


class TestRequestingObj:
    """
    Класс TestRequestingObj - вспомогательный класс с атрибутами-заглушками для
    проверки работы основного класса ClientWelcomeWindow.

    The TestRequestingObj class is an auxiliary class with stub attributes for
    checking the operation of the main ClientWelcomeWindow class.
    """
    def __init__(self):
        self.client_name = None
        self.pswd = None


def noname_client_welcome(name, pswd):
    """
    Инициирует создание объекта стартового окна ClientWelcomeWindow. Запускает
    стартовое окно, закрывает его при завершении работы.

    **Параметры**

    * name (str):
        логин пользователя (допускается отсутствие)
    * pswd (str):
        пароль пользователя (допускается отсутствие)

    **Возвращаемое значение**

    * self.name(str):
        введенный пользователем логин(имя).
    * self.pswd(str):
        введенный пользователем пароль.

    Initiates the creation of the ClientWelcomeWindow start window object.
    Launches the start window, closes it when the work is completed.

    **Parameters**

    * name (str):
        user login (absence is allowed)
    * pswd (str):
        user password (absence is allowed)

    **Return value**

    * self.name (str):
        the username (name) entered by the user.
    * self.pswd(str):
        the password entered by the user.
    """
    application = QApplication(sys.argv)
    window = ClientWelcomeWindow(name, pswd)
    window.show()
    application.exec()
    return window.name, window.pswd


def user_warning(error, msg):
    """
    Инициирует создание объекта окна уведомления об ошибке NameMissingWindow.
    Запускает окно уведомления, закрывает его при завершении работы.

    **Параметры**

        * error (str):
            текст ошибки пользователя
        * msg (str):
            информационное сообщение пользователю о том, что требуется исправить

    Initiates the creation of the NameMissingWindow error notification window
    object. Launches the notification window, closes it when the work is completed.

    **Parameters**

    * error (str):
        user error text
    * msg (str):
        informational message to the user about what needs to be fixed
    """
    application_warning = QApplication(sys.argv)
    window_warning = NameMissingWindow(error, msg)
    window_warning.show()
    application_warning.exec()


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # test = TestRequestingObj()
    # ex = ClientWelcomeWindow(test.client_name, test.pswd)
    # ex.show()
    # app.exec()
    # print(test.client_name)
    #
    application_test = QApplication(sys.argv)
    window_test = NameMissingWindow('Вы не ввели имя!', 'Приложение завершается')
    window_test.show()
    sys.exit(application_test.exec())
