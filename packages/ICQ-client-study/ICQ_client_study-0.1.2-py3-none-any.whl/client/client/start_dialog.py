from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp
from PyQt5.QtGui import QPixmap


class UserNameDialog(QDialog):
    """Класс стартового диалога с выбором имени пользователя"""

    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('ICQ')
        self.setFixedSize(175, 310)

        self.icon = QLabel(self)
        pixmap = QPixmap('common/icon128.png')
        self.icon.setPixmap(pixmap)
        self.icon.move(20, 10)
        self.icon.setFixedSize(128, 128)

        self.label = QLabel('Добро пожаловать в ICQ\nВведите имя пользователя:', self)
        self.label.move(15, 138)
        self.label.setFixedSize(150, 40)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 180)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 268)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 268)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_passwd = QLabel('Введите пароль:', self)
        self.label_passwd.move(15, 215)
        self.label_passwd.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 230)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """Обработчик кнопки ОК, если поле ввода не пустое,
        ставим флаг и завершаем приложение
        """
        if self.client_name.text() and self.client_passwd.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
