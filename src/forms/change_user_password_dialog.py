import os
import base64

from PyQt5.QtCore import QSettings, QObject, QEvent, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QMessageBox, QPushButton, QGridLayout, QGroupBox, \
    QLabel
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QCloseEvent


class ChangeUserPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super(ChangeUserPasswordDialog, self).__init__(parent)
        uic.loadUi(os.path.abspath('src/forms/change_user_password_dialog.ui'), self)

        self.installEventFilter(self)

        # define widgets
        self.field_old_user_password: QLineEdit = self.findChild(QLineEdit, 'field_old_user_password')
        self.lbl_old_user_password_not_match: QLabel = self.findChild(QLabel,'lbl_old_user_password_not_match')

        self.field_new_user_password: QLineEdit = self.findChild(QLineEdit, 'field_new_user_password')
        self.field_new_user_password_repeat: QLineEdit = self.findChild(QLineEdit, 'field_new_user_password_repeat')
        self.lbl_new_user_password_not_match: QLabel = self.findChild(QLabel, 'lbl_new_user_password_not_match')
        self.button_box: QDialogButtonBox = self.findChild(QDialogButtonBox, 'buttonBox')

        self.field_old_user_password.setEchoMode(QLineEdit.Password)
        self.field_new_user_password.setEchoMode(QLineEdit.Password)
        self.field_new_user_password_repeat.setEchoMode(QLineEdit.Password)

        self.old_password_checked: bool = False
        self.new_password_checked: bool = False

        self.settings: QSettings = self.parent().settings

        self.field_old_user_password.textChanged.connect(self.check_old_password)

        self.field_new_user_password.textChanged.connect(self.check_new_password)
        self.field_new_user_password_repeat.textChanged.connect(self.check_new_password)

        self.button_box.accepted.connect(self.check_old_password)

    def check_old_password(self):
        entered_password = base64.b64encode(self.field_old_user_password.text().encode('ascii')).decode()
        saved_password = self.settings.value('USER_PASSWORD')
        print(entered_password)
        print(saved_password)
        if entered_password == saved_password:
            self.lbl_old_user_password_not_match.setText('Match')
            self.lbl_old_user_password_not_match.setStyleSheet('color: rgb(38, 162, 105);')
            self.old_password_checked = True
            print('Match')
        else:
            self.lbl_old_user_password_not_match.setText('Not match')
            self.lbl_old_user_password_not_match.setStyleSheet('color: rgb(224, 27, 36);')
            self.old_password_checked = False

    def check_new_password(self):
        new_password = base64.b64encode(self.field_new_user_password.text().encode('ascii')).decode()
        new_password_repeat = base64.b64encode(self.field_new_user_password_repeat.text().encode('ascii')).decode()
        if new_password == new_password_repeat and new_password and new_password_repeat:
            self.lbl_new_user_password_not_match.setText('Match')
            self.lbl_new_user_password_not_match.setStyleSheet('color: rgb(38, 162, 105);')
            self.new_password_checked = True
            print('match', new_password, new_password_repeat)
        else:
            self.lbl_new_user_password_not_match.setText('Not match')
            self.lbl_new_user_password_not_match.setStyleSheet('color: rgb(224, 27, 36);')
            self.new_password_checked = False
            print('not match', new_password, new_password_repeat)

    def change_password(self):
        if self.old_password_checked and self.new_password_checked:
            new_password = base64.b64encode(self.field_new_user_password_repeat.text().encode('ascii')).decode()
            print(new_password)
            self.settings.setValue('USER_PASSWORD', new_password)
            msg = QMessageBox(self)
            msg.setWindowTitle('Change password')
            msg.setText(f'Password changed')
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            super().accept()

        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('Change password')
            msg.setText(f'Passwords not match')
            msg.setIcon(QMessageBox.Warning)
            msg.exec()

    def accept(self) -> None:
        print("custom func")
        self.change_password()


    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # skip from keyboard close combination
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Escape, Qt.Key_Enter):
                event.ignore()
                return True
        return super(ChangeUserPasswordDialog, self).eventFilter(obj, event)

    # def closeEvent(self, a0: QCloseEvent) -> None:
    #     print('clossing event')
    #     exit()



