import os
import typing
from time import sleep
from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, QObject, pyqtSignal, QThread, QTimer, QEvent
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QComboBox, QLabel, QPushButton, QTableWidget, QMenu, QAction, QDateTimeEdit, \
    QSpinBox, QLineEdit, QHeaderView, QTableView, QItemDelegate, QTableWidgetItem, QMessageBox, QStyledItemDelegate, \
    QStyleOptionViewItem, QDialog
from PyQt5 import uic, QtCore
from datetime import datetime, timedelta, time

from pyqtspinner import WaitingSpinner

from forms.comm_setting_dialog import CommSettingDialogUI
from utils import load_transactions_from_file, save_transactions_to_file, load_transactions_to_table, \
    get_transactions_from_table


class WaitPopUpWindow(QDialog):
    def __init__(self, parent=None):
        super(WaitPopUpWindow, self).__init__(parent)
        uic.loadUi(os.getcwd()+'/src/forms/wait_popup.ui', self)

        self.wait_indicator = WaitingSpinner(self, roundness=100.0,
                                             fade=50.35,
                                             radius=10,
                                             lines=15,
                                             line_length=30,
                                             line_width=6,
                                             speed=1.1,
                                             color=QColor(38, 162, 105))

        self.wait_timer = QTimer(self)
        self.wait_timer.setInterval(1000)
        self.wait_time: int = 0
        self.wait_timer.timeout.connect(self.update_wait_time)
        self.wait_timer.timeout.connect(lambda: print(self.wait_time))

        self.allow_close_window: bool = False
        #self.setAttribute(Qt.WA_QuitOnClose, True)
        self.installEventFilter(self)

        # disable close button
        # enable custom window hint
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # reuse initial flags
        # disable (but not hide) close button
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

    def update_wait_time(self):
        self.wait_time += 1
        self.lbl_time.setText(f'Please wait! {self.wait_time} sec')

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        # skip from keyboard close combination
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Escape, Qt.Key_Enter):
                event.ignore()
                return True
        return super(WaitPopUpWindow, self).eventFilter(obj, event)

    def show(self) -> None:
        self.wait_time = 0
        self.wait_indicator.start()
        self.wait_timer.start()
        self.exec()

    def closeEvent(self, a0: QCloseEvent) -> None:
        print('clossing event')
        if self.allow_close_window:
            self.wait_indicator.stop()
            self.wait_timer.stop()
            self.allow_close_window = False
            self.wait_time = 0
        else:
            a0.ignore()

    def allow_close(self):
        self.allow_close_window = True
