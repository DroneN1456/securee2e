from datetime import datetime
from threading import Thread
from termcolor import colored
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


import socket

SERVER_HOST = input('Enter server ip: ')
SERVER_PORT = int(input('Enter server port: '))
print()

s = socket.socket()
print(f'[*] Connecting to {SERVER_HOST}:{SERVER_PORT}')
s.connect((SERVER_HOST, SERVER_PORT))
print('[+] Connected')

name = input('Enter your username: ')
password_provided = input('Please inform your decryption key: ').encode()
salt = b'salt_'
kdf = PBKDF2HMAC(algorithm=hashes.SHA256, salt=salt,
                 iterations=1000, backend=default_backend(), length=32)
key = base64.urlsafe_b64encode(kdf.derive(password_provided))
f = Fernet(key)


def listen_for_messages():
    global f
    while True:
        message = s.recv(1024)
        try:
            message = f.decrypt(message)
            print(message.decode())
        except Exception as e:
            print(colored(f'[!] Error: {e}'))
            exit()


t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    msg = input()
    if (msg == 'q'):
        break
    print("\033[A                             \033[A")
    msg = f'{name}: {msg}'
    msg = f.encrypt(msg.encode())
    s.send(msg)


s.close()
