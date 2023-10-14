import itertools

from pyzkaccess import ZKAccess, ZK200
from pyzkaccess.exceptions import ZKSDKError
from itertools import product
from threading import Thread
import time

password_length = 8
correct_password = False
password_chars = "0123456789abcdefghijklmnopqrstuvwxyz"


# connstr = 'protocol=TCP,ipaddress=192.168.5.198,port=4370,timeout=4000,passwd=' + password


def get_possible_passwords(chars: str, length: int = 6):
    return product(chars, repeat=length)


def find_correct_port(ports):
    print(ports)
    for port in ports:
        connstr = f'protocol=TCP,ipaddress=192.168.5.198,port={port},timeout=4000,passwd='
        # print(connstr)
        try:
            zk = ZKAccess(connstr=connstr, device_model=ZK200, dllpath='pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll')
            print('Correct port is: ', port)
            break
        except ZKSDKError as e:
            print(port, e)


if __name__ == '__main__':
    ports = itertools.count(100)

    threads = []
    for thread_number in range(50):
        thread = Thread(target=find_correct_port, name=str(thread_number), kwargs={'ports': ports})
        threads.append(thread)
    for thread in threads:
        thread.start()


