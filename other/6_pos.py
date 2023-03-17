from pyzkaccess import ZKAccess, ZK200
from pyzkaccess.exceptions import ZKSDKError
from itertools import product
import time


password_length = 8
correct_password = False
password_chars = "0123456789abcdefghijklmnopqrstuvwxyz"
port = 0
password = ''
connstr = 'protocol=TCP,ipaddress=192.168.5.198,port=4370,timeout=4000,passwd=' + password


def get_possible_passwords(chars: str, length: int = 6):
    return product(chars, repeat=length)


password = ''
passwords = get_possible_passwords(password_chars)
for port in range(65000):
    connstr = f'protocol=TCP,ipaddress=192.168.5.198,port={port},timeout=4000,passwd=' + ''.join(password)
    #print(connstr)
    try:
        zk = ZKAccess(connstr=connstr, device_model=ZK200, dllpath='pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll')
        print('Correct password is: ', ''.join(password))
        break
    except ZKSDKError as e:
       print(port, e)
