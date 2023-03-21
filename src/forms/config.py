from decouple import config

ZK_IP = config('ZK_IP', default='192.168.5.198')
ZK_PORT = config('ZK_PORT', default=4370)
ZK_COMM_PASSWORD = config('ZK_COMM_PASSWORD')
USER_PASSWORD = config('USER_PASSWORD')
#DEBUG = config('DEBUG', default=False, cast=bool)
