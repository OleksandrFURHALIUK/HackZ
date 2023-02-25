import random

from datetime import datetime
import pprint
from typing import List

from pyzkaccess import ZKAccess, ZK200
from pyzkaccess.exceptions import ZKSDKError

from pyzkaccess.tables import Transaction, User
from pyzkaccess.common import ZKDatetimeUtils
from pyzkaccess import VerifyMode, PassageDirection
from pyzkaccess.enums import VerifyMode, PassageDirection


def get_transactions_from_device():
    pass


class HackZ:
    def __init__(self):
        self.connstr = 'protocol=TCP,ipaddress=192.168.5.198,port=4370,timeout=4000,passwd=ad256580'
        self.device: ZKAccess = None

    def connect(self):
        self.device = ZKAccess(connstr=self.connstr,
                               dllpath='pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll',
                               device_model=ZK200)
        # self.device.connect()

    def get_transaction_from_device(self, **kwargs) -> []:
        """
        Reading transaction from device
        :keyword card:number of user id card
        :keyword pin: user id
        :keyword door: door id
        :keyword verify_mode: enum VerifyMode not_available = 0,  only_finger = 1, only_password = 3, only_card = 4, card_or_finger = 6, card_and_finger = 10, card_and_password = 11, others = 200,
        :keyword event_type: enum EventType, 0: 'Normal Punch Open'
        :keyword entry_exit: PassageDirection
        :keyword time: datetime python format
        :return: List of transactions
        """
        raw_data = self.device.table('Transaction').where(**kwargs)
        transactions = []
        for record in raw_data:
            transactions.append(record)
        return transactions

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.disconnect()


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


def main():
    with HackZ() as zk:
        # new_transaction = Transaction(card=str(2819090),
        #                               pin=str(142),
        #                               verify_mode=VerifyMode(4),
        #                               door=2,
        #                               event_type=0,
        #                               entry_exit=PassageDirection(1),
        #                               time=ZKDatetimeUtils.zkctime_to_datetime(743555390)).with_zk(zk.device)
        transactions = zk.get_transaction_from_device(card='1498402')
        print(transactions)
        save_transactions_to_file(transactions)
        zk.get_transaction_from_device()

    transactions = load_transactions_from_file('transactions')
    print(transactions)


if __name__ == '__main__':
    main()
