from datetime import datetime
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDateTimeEdit
from pyzkaccess import Transaction
from pyzkaccess.tables import Transaction, User
from pyzkaccess.common import ZKDatetimeUtils
from pyzkaccess import VerifyMode, PassageDirection
from pyzkaccess.enums import VerifyMode, PassageDirection, EVENT_TYPES

from zkdevice import ZKDevice


def load_transactions_from_file(filename) -> List[Transaction]:
    """
    :param filename: file that contain records
    :return: list of transactions
    """
    with open(filename, 'r') as file:
        transactions = []
        for row in file.readlines():
            kwargs = {}
            for i in row.strip().split(', '):
                k = i.split('=')[0]
                v = i.split('=')[1]
                if k == 'door' or k == 'event_type':
                    kwargs[k] = int(v)
                elif k == 'entry_exit' or k == 'verify_mode':
                    kwargs[k] = eval(v)
                elif k == 'time':  # 2023-02-24 07:41:14
                    kwargs[k] = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
                else:
                    kwargs[k] = v
            transactions.append(Transaction(**kwargs))

        return transactions


def save_transactions_to_file(transactions: List[Transaction], filename: str = 'transactions') -> None:
    """
    :param transactions: list of transactions
    :param filename: name of file
    :return: None
    """
    with open(filename, 'x') as file:
        for t in transactions:
            row = f'card={t.card}, ' \
                  f'door={t.door}, ' \
                  f'entry_exit={t.entry_exit}, ' \
                  f'event_type={t.event_type}, ' \
                  f'pin={t.pin}, ' \
                  f'time={t.time}, ' \
                  f'verify_mode={t.verify_mode}'
            row += '\n'
            file.write(row)


def calculate_attendance_time(transactions: List) -> datetime:
    if transactions:
        for transaction in transactions:
            print(transaction)
    attendance_time = ''
    return attendance_time


def load_transactions_to_table(transactions: List, table: QTableWidget):
    table.setRowCount(len(transactions))
    for row in range(table.rowCount()):
        transaction = transactions[row]

        pin = QTableWidgetItem(transaction.pin)
        pin.setTextAlignment(Qt.AlignCenter)
        pin.setFlags(pin.flags() & ~Qt.ItemFlag.ItemIsEditable)

        card = QTableWidgetItem(transaction.card)
        card.setFlags(card.flags() & ~Qt.ItemFlag.ItemIsEditable)

        door = QTableWidgetItem(str(transaction.door))
        door.setFlags(door.flags() & ~Qt.ItemFlag.ItemIsEditable)

        event_type = QTableWidgetItem(str(transaction.event_type))
        event_type.setFlags(event_type.flags() & ~Qt.ItemFlag.ItemIsEditable)

        table.setItem(row, 0, pin)
        table.setItem(row, 1, card)
        table.setItem(row, 2, door)
        table.setItem(row, 3, event_type)
        table.setItem(row, 4, QTableWidgetItem(str(transaction.entry_exit.name)))
        table.setItem(row, 5, QTableWidgetItem(str(transaction.time)))
        table.setItem(row, 6, QTableWidgetItem(str(transaction.verify_mode.name)))
        # self.transactions_table.setItemDelegateForColumn(3, ComboEventTypeDelegate())


def get_transactions_from_table(table: QTableWidget):
    transactions = []
    for row in range(table.rowCount()):
        pin = table.item(row, 0).text()
        card = table.item(row, 1).text()
        door = table.item(row, 2).text()
        event_type = table.item(row, 3).text()
        entry_exit = PassageDirection[table.item(row, 4).text()]
        time = datetime.strptime(table.item(row, 5).text(), '%Y-%m-%d %H:%M:%S')
        verify_mode = VerifyMode[table.item(row, 6).text()]

        transaction = Transaction(card=card,
                                  pin=pin,
                                  verify_mode=verify_mode,
                                  door=int(door),
                                  event_type=int(event_type),
                                  entry_exit=entry_exit,
                                  time=time)
        transactions.append(transaction)
    return transactions




