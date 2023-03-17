import typing
from time import sleep
from typing import List
import os
from PyQt5.QtCore import Qt, pyqtSlot, QObject, pyqtSignal, QThread, QTimer, pyqtProperty, QPropertyAnimation, \
    QThreadPool
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QMainWindow, QComboBox, QLabel, QPushButton, QTableWidget, QMenu, QAction, QDateTimeEdit, \
    QSpinBox, QLineEdit, QHeaderView, QTableView, QItemDelegate, QTableWidgetItem, QMessageBox, QStyledItemDelegate, \
    QStyleOptionViewItem, QWidget
from PyQt5 import uic, QtCore
from datetime import datetime, timedelta, time

from pyqtspinner import WaitingSpinner

from forms.comm_setting_dialog import CommSettingDialogUI
from forms.wait_popup import WaitPopUpWindow
from utils import load_transactions_from_file, save_transactions_to_file, load_transactions_to_table, \
    get_transactions_from_table

from pyzkaccess import ZKAccess, ZK200


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.abspath('src/forms/main_window.ui'), self)
        # setup user interface
        self.setup_ui()

        # define widgets
        # transactions table
        self.transactions_table: QTableWidget = self.findChild(QTableWidget, 'transactions_table')
        # buttons
        self.btn_search: QPushButton = self.findChild(QPushButton, 'btn_search')
        self.btn_add_transaction: QPushButton = self.findChild(QPushButton, 'btn_add_transaction')
        self.btn_delete_transaction: QPushButton = self.findChild(QPushButton, 'btn_delete_transaction')
        self.btn_calculate_attendance_time: QPushButton = self.findChild(QPushButton, 'btn_calculate_time')
        self.btn_upload_transactions_from_device: QPushButton = self.findChild(QPushButton,
                                                                               'btn_upload_transactions_from_device')
        self.btn_download_transactions_to_device: QPushButton = self.findChild(QPushButton,
                                                                               'btn_download_transactions_to_device')
        self.btn_clear_transactions_table: QPushButton = self.findChild(QPushButton, 'btn_clear_transactions_table')
        # labels
        self.lbl_transactions_count: QLabel = self.findChild(QLabel, 'lbl_transactions_count')
        self.lbl_attendance_time: QLabel = self.findChild(QLabel, 'lbl_attendance_time')
        # filter fields
        self.field_pin: QSpinBox = self.findChild(QSpinBox, 'field_pin')
        self.field_card: QLineEdit = self.findChild(QLineEdit, 'field_card')
        self.field_door: QComboBox = self.findChild(QComboBox, 'field_door')
        self.field_event_type: QComboBox = self.findChild(QComboBox, 'field_event_type')
        self.field_start_date_time: QDateTimeEdit = self.findChild(QDateTimeEdit, 'field_start_date_time')
        self.field_end_date_time: QDateTimeEdit = self.findChild(QDateTimeEdit, 'field_end_date_time')
        # menu
        self.menu_settings: QMenu = self.findChild(QMenu, 'menu_settings')
        self.action_show_connecting_settings: QAction = self.findChild(QAction, 'show_connection_settings')

        # define events handler
        self.btn_search.clicked.connect(self.btn_search_clicked_handler)
        self.btn_add_transaction.clicked.connect(self.btn_add_transaction_clicked_handler)
        self.btn_delete_transaction.clicked.connect(self.btn_delete_transaction_clicked_handler)
        self.btn_clear_transactions_table.clicked.connect(self.btn_clear_transactions_table_clicked_handler)
        self.btn_calculate_attendance_time.clicked.connect(self.btn_calculate_attendance_time_clicked_handler)
        self.btn_upload_transactions_from_device.clicked.connect(
            self.btn_upload_transactions_from_device_clicked_handler)
        self.btn_download_transactions_to_device.clicked.connect(
            self.btn_download_transactions_to_device_clicked_handler)

        # menu settings
        self.action_show_connecting_settings.triggered.connect(self.show_connecting_settings)

        # define zk
        # configure zk download and upload in another thread
        self.wait_dialog = WaitPopUpWindow(self)
        self.zk_thread_pool = QThreadPool()
        self.zk_thread_pool.setMaxThreadCount(2)
        print("Multithreading with maximum %d threads" % self.zk_thread_pool.maxThreadCount())
        self.zk_loader = ZKLoader()
        # configure signals for closing wait window
        self.zk_loader.finished.connect(self.wait_dialog.allow_close)
        self.zk_loader.finished.connect(self.wait_dialog.close)
        # update transactions table when upload from device
        self.zk_loader.upload_finished.connect(self.update_transactions_table)

    def setup_ui(self):
        # setting first day in current month in start datetime field
        self.field_start_date_time.setCalendarPopup(True)
        self.field_start_date_time.setDate(datetime.now().date().replace(day=1))

        # setting the last day in current month in end datetime field
        self.field_end_date_time.setCalendarPopup(True)
        next_month = datetime.today().replace(day=28) + timedelta(days=4)
        # subtracting the number of the current day brings us back one month
        last_day = next_month - timedelta(days=next_month.day)
        self.field_end_date_time.setDate(last_day.date())
        self.field_end_date_time.setTime(time(hour=23, minute=59, second=59))

        self.field_door.addItems(['Any', '1-entry', '2-exit'])
        self.field_event_type.addItems(['Any', 'entry', 'exit'])

        # change column wide in transactions table
        for i in range(self.transactions_table.columnCount()):
            self.transactions_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        # self.transactions_table.resizeColumnsToContents()
        self.transactions_table.setItemDelegateForColumn(4, ComboEntryExitDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(0, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(1, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(2, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(3, AlignDelegate(self.transactions_table))

        # setting auto calculate rows count
        self.transactions_table.model().rowsRemoved.connect(self.calculate_rows)
        self.transactions_table.model().rowsInserted.connect(self.calculate_rows)

    def show_connecting_settings(self):
        setting_window = CommSettingDialogUI(self)
        setting_window.exec()
        print('show connecting settings')

    def calculate_rows(self):
        self.lbl_transactions_count.setText(f'Кількість записів: {self.transactions_table.rowCount()}')
        print('calculating rows')

    def btn_search_clicked_handler(self):
        print('btn search clicked')
        self.zk_transactions = load_transactions_from_file('transactions')
        load_transactions_to_table(self.zk_transactions, self.transactions_table)

    def btn_add_transaction_clicked_handler(self):
        print('btn add record clicked')
        current_row = self.transactions_table.currentRow()
        self.transactions_table.insertRow(current_row + 1)
        if not self.transactions_table.rowCount() == 0:
            self.transactions_table.setItem(current_row + 1, 0,
                                            QTableWidgetItem(self.transactions_table.item(current_row, 0)))
            self.transactions_table.setItem(current_row + 1, 1,
                                            QTableWidgetItem(self.transactions_table.item(current_row, 1)))

    def btn_delete_transaction_clicked_handler(self):
        if self.transactions_table.currentRow() < 0:
            msg = QMessageBox(self)
            msg.setWindowTitle('Помилка')
            msg.setText('Не вибрано даних для видалення')
            msg.setIcon(QMessageBox.Warning)
            msg.exec()
        else:
            self.transactions_table.removeRow(self.transactions_table.currentRow())
        print('btn delete record clicked')

    def btn_clear_transactions_table_clicked_handler(self):
        print('btn clear transactions table')
        self.transactions_table.setRowCount(0)
        self.zk_transactions.clear()

    def btn_calculate_attendance_time_clicked_handler(self):
        print('btn calculate time clicked')
        self.lbl_attendance_time.setVisible(not self.lbl_attendance_time.isVisible())
        print(self.field_event_type.currentText())

    def btn_upload_transactions_from_device_clicked_handler(self):
        print('upload button pressed')

        self.wait_dialog.setWindowTitle('Uploading from device')
        self.zk_thread_pool.start(self.zk_loader.upload_from_device)
        self.wait_dialog.show()

    def btn_download_transactions_to_device_clicked_handler(self):
        print('download button pressed')
        self.zk_transactions = get_transactions_from_table(self.transactions_table)
        self.wait_dialog.setWindowTitle('Downloading to device')
        self.zk_thread_pool.start(self.zk_loader.download_to_device)
        self.wait_dialog.show()

    def update_transactions_table(self):
        load_transactions_to_table(self.zk_loader.transactions, self.transactions_table)

class ComboEntryExitDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ComboEntryExitDelegate, self).__init__(parent)
        self.items = ['entry', 'exit']
        self.parent: QTableWidget = parent

    def initStyleOption(self, option, index):
        """ initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) """
        super(ComboEntryExitDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

    def createEditor(self, parent, option, index):
        """ createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget """
        combobox = QComboBox(parent)
        combobox.addItems(self.items)

        if index.data() == 'entry':
            combobox.setCurrentIndex(0)
        elif index.data() == 'exit':
            combobox.setCurrentIndex(1)
        else:
            combobox.setCurrentIndex(0)
        combobox.currentIndexChanged.connect(self.currentIndexChanged)

        combobox.currentTextChanged.connect(lambda value: self.currentTextChanged(index, value))
        combobox.destroyed.connect(self.destroyEditor)
        return combobox

    def setEditorData(self, editor, index):
        pass
        # value = index.data()
        # print('set editor data')
        # editor.setCurrentIndex(1)

    def destroyEditor(self, editor, index):
        print('combo destroyed')
        event_type = self.parent.item(self.parent.currentRow(), 4).text()
        if event_type == 'entry':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('1'))
        elif event_type == 'exit':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('2'))

    # @pyqtSlot()
    def currentIndexChanged(self):
        print('index changed', self.sender())
        # self.commitData.emit(self.sender())

    # @pyqtSlot()
    def currentTextChanged(self, index, value):
        print('current text changed')


class ComboEventTypeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ComboEntryExitDelegate, self).__init__(parent)
        self.items = ['0-Normal open', 'exit']
        self.parent: QTableWidget = parent

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        combobox.addItems(self.items)
        # combobox.setStyleSheet('selection-background-color: rgb(143, 240, 164);')
        # combobox.setStyleSheet('selection-color: rgb(143, 140, 164);')

        if index.data() == 'entry':
            combobox.setCurrentIndex(0)
        elif index.data() == 'exit':
            combobox.setCurrentIndex(1)
        else:
            combobox.setCurrentIndex(0)
        combobox.currentIndexChanged.connect(self.currentIndexChanged)

        combobox.currentTextChanged.connect(lambda value: self.currentTextChanged(index, value))
        combobox.destroyed.connect(self.destroyEditor)
        return combobox

    def setEditorData(self, editor, index):
        pass
        # value = index.data()
        # print('set editor data')
        # editor.setCurrentIndex(1)

    def destroyEditor(self, editor, index):
        print('combo destroyed')
        event_type = self.parent.item(self.parent.currentRow(), 4).text()
        if event_type == 'entry':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('1'))
        elif event_type == 'exit':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('2'))

    # @pyqtSlot()
    def currentIndexChanged(self):
        print('index changed', self.sender())
        # self.commitData.emit(self.sender())

    # @pyqtSlot()
    def currentTextChanged(self, index, value):
        print('current text changed')


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class ZKLoader(QObject):
    from pyzkaccess import ZKAccess, ZK200
    upload_started = pyqtSignal()
    upload_finished = pyqtSignal()

    download_started = pyqtSignal()
    download_finished = pyqtSignal()

    started = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, parent=None,
                 ip_addr='192.168.5.198', port=4370, password='ad256580'):
        super().__init__(parent)

        self.connection_string = f'protocol=TCP,ipaddress={ip_addr},port={port},timeout=4000,passwd={password}'
        self.zk_device = ZKAccess(connstr=self.connection_string,
                                  dllpath=os.path.abspath('pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll'),
                                  device_model=ZK200)
        self.transactions = list()

    @pyqtSlot()
    def upload_from_device(self):
        """Long-running task."""
        self.started.emit()
        self.upload_started.emit()
        print(self.zk_device.device.serial_number)

        for t in self.zk_device.table('Transaction').where(pin='504'):
            self.transactions.append(t)
        self.upload_finished.emit()
        self.finished.emit()

    @pyqtSlot()
    def download_to_device(self):
        """Long-running task."""
        self.started.emit()
        self.download_started.emit()

        # with self.zk_device as zk:
        print('download trans', self.transactions)
        if self.transactions:
            # zk.table('Transactions').upsert(self.transactions)
            for tr in self.transactions:
                print(tr)

        for i in range(10):
            sleep(1)
            print('downloading', i)
            self.progress.emit(i + 1)
        self.finished.emit()
        self.download_finished.emit()


class Spinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = QPixmap('load_icon.png')

        self.setFixedSize(30, 30)
        self._angle = 0

        self.animation = QPropertyAnimation(self, b"angle", self)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.setDuration(2000)
        self.animation.start()

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def paintEvent(self, ev=None):
        painter = QPainter(self)
        painter.translate(15, 15)
        painter.rotate(self._angle)
        painter.translate(-15, -15)
        painter.drawPixmap(5, 5, self.pixmap)
