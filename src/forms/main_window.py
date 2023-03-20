import typing
from time import sleep
from typing import List
import os
from PyQt5.QtCore import Qt, pyqtSlot, QObject, pyqtSignal, QThread, QTimer, pyqtProperty, QPropertyAnimation, \
    QThreadPool, QModelIndex, QMargins
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QPainter, QPixmap, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QComboBox, QLabel, QPushButton, QTableWidget, QMenu, QAction, QDateTimeEdit, \
    QSpinBox, QLineEdit, QHeaderView, QTableView, QItemDelegate, QTableWidgetItem, QMessageBox, QStyledItemDelegate, \
    QStyleOptionViewItem, QWidget, QFileDialog
from PyQt5 import uic, QtCore
from datetime import datetime, timedelta, time
from pyzkaccess.enums import PassageDirection, EVENT_TYPES, VerifyMode

from pyqtspinner import WaitingSpinner

from forms.comm_setting_dialog import CommSettingDialogUI
from forms.wait_popup import WaitPopUpWindow
from utils import load_transactions_from_file, save_transactions_to_file, load_transactions_to_table, \
    get_transactions_from_table

from pyzkaccess import ZKAccess, ZK200, DocValue


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.abspath('src/forms/main_window.ui'), self)

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
        self.filter_field_pin: QSpinBox = self.findChild(QSpinBox, 'filter_field_pin')
        self.filter_field_card: QLineEdit = self.findChild(QLineEdit, 'filter_field_card')
        self.filter_field_door: QComboBox = self.findChild(QComboBox, 'filter_field_door')
        self.filter_field_event_type: QComboBox = self.findChild(QComboBox, 'filter_field_event_type')
        self.filter_field_entry_exit: QComboBox = self.findChild(QComboBox, 'filter_field_entry_exit')
        self.filter_field_verify_mode: QComboBox = self.findChild(QComboBox, 'filter_field_verify_mode')
        self.filter_field_start_date_time: QDateTimeEdit = self.findChild(QDateTimeEdit, 'filter_field_start_date_time')
        self.filter_field_end_date_time: QDateTimeEdit = self.findChild(QDateTimeEdit, 'filter_field_end_date_time')
        # menu
        self.menu_settings: QMenu = self.findChild(QMenu, 'menu_settings')
        self.action_show_connecting_settings: QAction = self.findChild(QAction, 'show_connection_settings')
        self.action_open_file: QAction = self.findChild(QAction, 'open_file')
        self.action_save_file: QAction = self.findChild(QAction, 'save_file')

        # define zk
        self.wait_dialog = WaitPopUpWindow(self)
        self.zk_thread_pool = QThreadPool()
        self.zk_thread_pool.setMaxThreadCount(2)
        print("Multithreading with maximum %d threads" % self.zk_thread_pool.maxThreadCount())
        self.zk_loader = ZKLoader(self)

        # setup user interface
        self.setup_ui()

    def setup_ui(self):

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

        # open and save
        self.action_open_file.triggered.connect(self.open_file_handler)
        self.action_save_file.triggered.connect(self.save_file_handler)

        # menu settings
        self.action_show_connecting_settings.triggered.connect(self.show_connecting_settings)

        # setting auto calculate rows count
        self.transactions_table.model().rowsRemoved.connect(self.calculate_rows)
        self.transactions_table.model().rowsInserted.connect(self.calculate_rows)

        # configure signals for closing wait window
        self.zk_loader.finished.connect(self.wait_dialog.allow_close)
        self.zk_loader.finished.connect(self.wait_dialog.close)

        # update transactions table when finished upload from device
        self.zk_loader.upload_finished.connect(self.update_transactions_table)

        # setting first day in current month in start datetime field
        self.filter_field_start_date_time.setCalendarPopup(True)
        self.filter_field_start_date_time.setDate(datetime.now().date().replace(day=1))

        # setting the last day in current month in end datetime field
        self.filter_field_end_date_time.setCalendarPopup(True)
        next_month = datetime.today().replace(day=28) + timedelta(days=4)
        # subtracting the number of the current day brings us back one month
        last_day = next_month - timedelta(days=next_month.day)
        self.filter_field_end_date_time.setDate(last_day.date())
        self.filter_field_end_date_time.setTime(time(hour=23, minute=59, second=59))

        # configure card filter field
        self.filter_field_card.setValidator(QIntValidator())
        self.filter_field_card.setMaxLength(32)
        # configure door field
        self.filter_field_door.addItems(['Any', '1', '2'])

        # configure entry exit field
        self.filter_field_entry_exit.addItem('Any', None)
        for item in PassageDirection:
            self.filter_field_entry_exit.addItem(item.name, item)

        # configure event type filter
        self.filter_field_event_type.addItem('Any', None)
        for key, value in EVENT_TYPES.items():
            value: DocValue
            self.filter_field_event_type.addItem(f'{key} {value.doc}', key)

        # configure verify mode
        self.filter_field_verify_mode.addItem('Any', None)
        for item in VerifyMode:
            self.filter_field_verify_mode.addItem(item.name, item)

        # change column wide in transactions table
        for i in range(self.transactions_table.columnCount()):
            self.transactions_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            if i == 5 :
                self.transactions_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
                self.transactions_table.setColumnWidth(5, 200)

        # self.transactions_table.resizeColumnsToContents()
        self.transactions_table.setItemDelegateForColumn(4, ComboEntryExitDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(0, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(1, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(2, AlignDelegate(self.transactions_table))
        # self.transactions_table.setItemDelegateForColumn(3, AlignDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(3, ComboEventTypeDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(5, DateTimeDelegate(self.transactions_table))
        self.transactions_table.setItemDelegateForColumn(6, ComboVerifyModeDelegate(self.transactions_table))

    def show_connecting_settings(self):
        setting_window = CommSettingDialogUI(self)
        setting_window.exec()
        print('show connecting settings')

    def calculate_rows(self):
        self.lbl_transactions_count.setText(f'Кількість записів: {self.transactions_table.rowCount()}')
        print('calculating rows')

    def btn_search_clicked_handler(self):
        print('btn search clicked')
        # self.zk_transactions = load_transactions_from_file('transactions')
        self.transactions_table.setColumnWidth(5, self.transactions_table.columnWidth(5) + 15)
        #load_transactions_to_table(self.zk_loader.transactions, self.transactions_table)

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
        self.zk_loader.transactions.clear()
        print(self.zk_loader.transactions)

    def btn_calculate_attendance_time_clicked_handler(self):
        print('btn calculate time clicked')
        # self.lbl_attendance_time.setVisible(not self.lbl_attendance_time.isVisible())
        print(self.filter_field_event_type.currentText())

    def btn_upload_transactions_from_device_clicked_handler(self):
        print('upload button pressed')
        self.transactions_table.setRowCount(0)
        self.wait_dialog.setWindowTitle('Uploading from device')
        self.zk_thread_pool.start(self.zk_loader.upload_from_device)
        self.wait_dialog.show()

    def btn_download_transactions_to_device_clicked_handler(self):
        print('download button pressed')
        self.zk_loader.transactions = get_transactions_from_table(self.transactions_table)
        self.wait_dialog.setWindowTitle('Downloading to device')
        self.zk_thread_pool.start(self.zk_loader.download_to_device)
        self.wait_dialog.show()

    def update_transactions_table(self):
        load_transactions_to_table(self.zk_loader.transactions, self.transactions_table)

    def open_file_handler(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open trnsactions file", "",
                                                  "Transaction Files (*.tr);;Text Files (*.txt);;All Files (*)",
                                                  options=options)
        if fileName:
            print('Opening', fileName)
            try:
                load_transactions_to_table(transactions=load_transactions_from_file(fileName),
                                           table=self.transactions_table)
            except Exception as error:
                msg = QMessageBox(self)
                msg.setWindowTitle('Error')
                msg.setText(f'Error during opening file\n{str(error)}')
                msg.setIcon(QMessageBox.Warning)
                msg.exec()

    def save_file_handler(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # self.options |= QFileDialog.DontConfirmOverwrite
        fileName, t = QFileDialog.getSaveFileName(self, "Save transactions as", "",
                                                  "Transactions files (*.tr)",
                                                  options=options)
        if fileName:
            transactions = get_transactions_from_table(self.transactions_table)
            if '.tr' in fileName:
                save_transactions_to_file(transactions, fileName)
            else:
                save_transactions_to_file(transactions, fileName + '.tr')
            print(fileName)


class ComboEntryExitDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ComboEntryExitDelegate, self).__init__(parent)
        self.parent: QTableWidget = parent

    def initStyleOption(self, option, index):
        """ initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) """
        super(ComboEntryExitDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

    def createEditor(self, parent, option, index):
        """ createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget """
        combobox = QComboBox(parent)
        for item in PassageDirection:
            combobox.addItem(item.name, item.name)

        combobox.currentIndexChanged.connect(self.currentIndexChanged)
        combobox.currentTextChanged.connect(lambda value: self.currentTextChanged(index, value))
        combobox.destroyed.connect(self.destroyEditor)
        return combobox

    def setEditorData(self, editor, index):
        editor.setCurrentText(index.data())
        # value = index.data()
        # print('set editor data')
        # editor.setCurrentIndex(1)

    def destroyEditor(self, editor, index):
        print('combo destroyed')
        event_type = self.parent.item(self.parent.currentRow(), 4).text()
        if event_type == 'entry':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('1'))
            if not self.parent.item(self.parent.currentRow(), 3):
                self.parent.setItem(self.parent.currentRow(), 3, QTableWidgetItem('0'))
            if not self.parent.item(self.parent.currentRow(), 6):
                self.parent.setItem(self.parent.currentRow(), 6, QTableWidgetItem('only_card'))
        elif event_type == 'exit':
            self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('2'))
            if not self.parent.item(self.parent.currentRow(), 3):
                self.parent.setItem(self.parent.currentRow(), 3, QTableWidgetItem('0'))
            if not self.parent.item(self.parent.currentRow(), 6):
                self.parent.setItem(self.parent.currentRow(), 6, QTableWidgetItem('only_card'))

    @pyqtSlot()
    def currentIndexChanged(self):
        print('index changed', self.sender())
        # self.commitData.emit(self.sender())

    # @pyqtSlot()
    def currentTextChanged(self, index, value):
        print('current text changed')


class ComboEventTypeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ComboEventTypeDelegate, self).__init__(parent)
        self.parent: QTableWidget = parent

    def initStyleOption(self, option, index):
        """ initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) """
        super(ComboEventTypeDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        for key, value in EVENT_TYPES.items():
            value: DocValue
            combobox.addItem(f'{key} {value.doc}', key)

        combobox.currentIndexChanged.connect(self.currentIndexChanged)
        combobox.currentTextChanged.connect(lambda val: self.currentTextChanged(index, val))
        combobox.destroyed.connect(self.destroyEditor)
        return combobox

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        print('editor ', editor.setCurrentText(index.data()))

    def destroyEditor(self, editor, index):
        print('combo destroyed', editor.currentData())
        self.parent.setItem(self.parent.currentRow(), 3, QTableWidgetItem(str(editor.currentData())))

    # @pyqtSlot()
    def currentIndexChanged(self):
        print('index changed', self.sender())
        # self.commitData.emit(self.sender())

    # @pyqtSlot()
    def currentTextChanged(self, index, value):
        print('current text changed')


class ComboVerifyModeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ComboVerifyModeDelegate, self).__init__(parent)
        self.parent: QTableWidget = parent

    def initStyleOption(self, option, index):
        """ initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) """
        super(ComboVerifyModeDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignVCenter | Qt.AlignLeft

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        for item in VerifyMode:
            combobox.addItem(item.name, item.name)

        combobox.currentIndexChanged.connect(self.currentIndexChanged)
        combobox.currentTextChanged.connect(lambda value: self.currentTextChanged(index, value))
        combobox.destroyed.connect(self.destroyEditor)
        return combobox

    def setEditorData(self, editor, index):
        editor.setCurrentText(index.data())
        print('set editor data')
        # value = index.data()
        # print('set editor data')
        # editor.setCurrentIndex(1)

    def destroyEditor(self, editor, index):
        print('combo destroyed')
        # self.parent.setItem(self.parent.currentRow(), 6, QTableWidgetItem(str(editor.currentData())))
        # elif event_type == 'exit':
        # self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('2'))

    # @pyqtSlot()
    def currentIndexChanged(self):
        print('index changed', self.sender())
        # self.commitData.emit(self.sender())

    # @pyqtSlot()
    def currentTextChanged(self, index, value):
        print('current text changed')


class DateTimeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DateTimeDelegate, self).__init__(parent)
        self.parent: QTableWidget = parent

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        """ initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) """
        super(DateTimeDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignVCenter | Qt.AlignCenter

    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setDisplayFormat('yyyy-MM-dd HH:mm:ss')

        editor.setDateTime(datetime.strptime(index.data(), '%Y-%m-%d %H:%M:%S'))

        editor.dateTimeChanged.connect(self.date_time_changed)
        editor.dateTimeChanged.connect(lambda: print(editor.dateTime()))
        editor.destroyed.connect(self.destroyEditor)

        return editor

    def setEditorData(self, editor, index):
        # editor.setCurrentText(index.data())
        print('set editor data')

    def destroyEditor(self, editor, index):
        print('editor destroyed')

        item = QTableWidgetItem(editor.dateTime().toString('yyyy-MM-dd HH:mm:ss'))
        self.parent.setItem(self.parent.currentRow(), 5, item)

        # self.parent.setItem(self.parent.currentRow(), 6, QTableWidgetItem(str(editor.currentData())))
        # elif event_type == 'exit':
        # self.parent.setItem(self.parent.currentRow(), 2, QTableWidgetItem('2'))

        # @pyqtSlot()

    def date_time_changed(self):
        print('date time changed')


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class ZKLoader(QObject):
    upload_started = pyqtSignal()
    upload_finished = pyqtSignal()

    download_started = pyqtSignal()
    download_finished = pyqtSignal()

    started = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, parent=None, ip_addr='192.168.5.198', port=4370, password='ad256580'):
        super().__init__(parent)

        self.connection_string = f'protocol=TCP,ipaddress={ip_addr},port={port},timeout=4000,passwd={password}'
        self.zk_device = ZKAccess(connstr=self.connection_string,
                                  dllpath=os.path.abspath('pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll'),
                                  device_model=ZK200)
        self.transactions = list()
        self.filter_kwargs = dict()

    @pyqtSlot()
    def upload_from_device(self):
        """Long-running task."""
        self.started.emit()
        self.upload_started.emit()

        self.transactions.clear()
        self.get_filter_kwargs()
        # for t in self.zk_device.table('Transaction').where(**self.filter_kwargs):
        # self.transactions.append(t)
        print('filter kwargs:', self.filter_kwargs)
        self.upload_finished.emit()
        self.finished.emit()

    @pyqtSlot()
    def download_to_device(self):
        """Long-running task."""
        self.started.emit()
        self.download_started.emit()

        self.zk_device.table('Transaction').upsert(self.transactions)
        # self.progress.emit(i + 1)
        self.finished.emit()
        self.download_finished.emit()

    def get_filter_kwargs(self):
        if self.parent().filter_field_pin.text():
            self.filter_kwargs['pin'] = self.parent().filter_field_pin.text()
        else:
            self.filter_kwargs.pop('pin', None)

        if self.parent().filter_field_card.text():
            self.filter_kwargs['card'] = self.parent().filter_field_card.text()
        else:
            self.filter_kwargs.pop('card', None)

        if self.parent().filter_field_door.currentText() == 'Any':
            self.filter_kwargs.pop('door', None)
        else:
            self.filter_kwargs['door'] = int(self.parent().filter_field_door.currentText())

        if self.parent().filter_field_event_type.currentText() == 'Any':
            self.filter_kwargs.pop('event_type', None)
        else:
            self.filter_kwargs['event_type'] = self.parent().filter_field_event_type.currentData()

        # entry exit filter
        if self.parent().filter_field_entry_exit.currentText() == 'Any':
            self.filter_kwargs.pop('entry_exit', None)
        else:
            self.filter_kwargs['entry_exit'] = self.parent().filter_field_entry_exit.currentData()

        # verify mode filter
        if self.parent().filter_field_verify_mode.currentText() == 'Any':
            self.filter_kwargs.pop('verify_mode', None)
        else:
            self.filter_kwargs['verify_mode'] = self.parent().filter_field_verify_mode.currentData()


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
