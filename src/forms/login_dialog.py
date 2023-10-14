import os
import base64

from PyQt5.QtCore import QSettings, QObject, QEvent, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QMessageBox, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QCloseEvent


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        uic.loadUi(os.path.abspath('src/forms/login_dialog.ui'), self)

        self.installEventFilter(self)

        # define widgets
        self.field_user_password: QLineEdit = self.findChild(QLineEdit, 'user_password')
        self.btn_login: QPushButton = self.findChild(QPushButton, 'btn_login')

        self.field_user_password.setEchoMode(QLineEdit.Password)
        self.settings: QSettings = self.parent().settings
        self.btn_login.clicked.connect(self.check_password)

    def check_password(self):
        entered_password = base64.b64encode(self.field_user_password.text().encode('ascii')).decode()
        saved_password = self.settings.value('USER_PASSWORD')
        print(entered_password)
        print(saved_password)
        if entered_password == saved_password:
            self.accept()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('Error')
            msg.setText(f'Wrong password, Try again!')
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
            #self.reject()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # skip from keyboard close combination
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Escape, Qt.Key_Enter):
                event.ignore()
                return True
        return super(LoginDialog, self).eventFilter(obj, event)

    def closeEvent(self, a0: QCloseEvent) -> None:
        print('clossing event')
        exit()



