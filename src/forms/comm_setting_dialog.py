import os
import base64

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QDialogButtonBox,QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator


class CommSettingDialogUI(QDialog):
    def __init__(self, parent=None):
        super(CommSettingDialogUI, self).__init__(parent)
        uic.loadUi(os.path.abspath('src/forms/comm_setting_dialog.ui'), self)

        # define widgets
        self.field_ip_addr: QLineEdit = self. findChild(QLineEdit, 'field_ip_addr')
        self.field_port: QLineEdit = self.findChild(QLineEdit, 'field_port')
        self.field_comm_password: QLineEdit = self.findChild(QLineEdit, 'field_comm_password')
        self.dialog_buttons: QDialogButtonBox = self.findChild(QDialogButtonBox, 'buttonBox')

        # allow only integers in port field
        only_int = QIntValidator()
        only_int.setRange(1, 65535)
        self.field_port.setValidator(only_int)

        self.field_comm_password.setEchoMode(QLineEdit.Password)
        self.settings: QSettings = self.parent().settings
        self.reading_settings()
        self.dialog_buttons.accepted.connect(self.update_settings)

    def update_settings(self) -> None:
        self.settings.setValue('ZK_IP', base64.b64encode(self.field_ip_addr.text().encode('ascii')))
        self.settings.setValue('ZK_PORT', base64.b64encode(self.field_port.text().encode('ascii')))
        self.settings.setValue('ZK_COMM_PASSWORD', base64.b64encode(self.field_comm_password.text().encode('ascii')))

    def reading_settings(self):

        self.field_ip_addr.setText(base64.b64decode(self.settings.value('ZK_IP')).decode())
        self.field_port.setText(base64.b64decode(self.settings.value('ZK_PORT')).decode())
        self.field_comm_password.setText(base64.b64decode(self.settings.value('ZK_COMM_PASSWORD')).decode())





