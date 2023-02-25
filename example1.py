from itertools import product
import time
password = input('Введите ваш пароль:')
start_time = time.time()
chars = '0123456789'
test = 'abcdefghijklmnopqrstuvwxyz'

for i in product(chars,repeat=len(password)):
    if ''.join(i) == password:
        print('\nВаш пароль:',''.join(i),'\nПотребовалось времени:',round(float("%s" % (time.time() - start_time)),2),'секунд')
        break