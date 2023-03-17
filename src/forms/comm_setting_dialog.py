import os

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator


class CommSettingDialogUI(QDialog):
    def __init__(self, parent=None):
        super(CommSettingDialogUI, self).__init__(parent)
        uic.loadUi(os.getcwd()+'/src/forms/comm_setting_dialog.ui', self)

        # define widgets
        self.field_ip_addr: QLineEdit = self. findChild(QLineEdit, 'field_ip_addr')
        self.field_port: QLineEdit = self.findChild(QLineEdit, 'field_port')
        self.field_comm_password: QLineEdit = self.findChild(QLineEdit, 'field_comm_password')

        # allow only integers in port field
        only_int = QIntValidator()
        only_int.setRange(1, 65535)
        self.field_port.setValidator(only_int)

        self.field_comm_password.setEchoMode(QLineEdit.Password)



