import socket
import os
import platform
import configparser
from termcolor import colored
from threading import Thread

version = '1.0.0'

config = configparser.ConfigParser()
if (not os.path.exists('./config.ini')):
    with open('./config.ini', 'w') as file:
        config['GENERAL'] = {
            "SERVER_HOST": '0.0.0.0',
            "SERVER_PORT": '5002'
        }
        config.write(file)
config.read('config.ini')

SERVER_HOST = str(config['GENERAL']['SERVER_HOST'])
SERVER_PORT = int(config['GENERAL']['SERVER_PORT'])


def clear_console():
    system = platform.system()
    if (not system == 'Windows'):
        os.system('clear')
    else:
        os.system('cls')


def main():
    print(colored(f'Welcome to SecureE2E {version}!'))
    print()
    print(colored('[1] Start Server'))
    response = int(input())
    if response == 1:
        start_server()


def start_server():
    client_sockets = set()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    clear_console()
    print(colored('[*] ', 'yellow') +
          f'Listening to {SERVER_HOST}:{SERVER_PORT}')

    while True:
        client_socket, client_addr = s.accept()
        print(colored('[+] ', 'green') + f'{client_addr} connected')
        client_sockets.add(client_socket)
        t = Thread(target=listen_to_clients, args=(
            client_socket, client_sockets))
        t.daemon = True
        t.start()

    for cs in client_sockets:
        cs.close()
    s.close()


def listen_to_clients(cs, clients):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(colored('[!] ', 'red') + f'{e}')
        for client in clients:
            client.send(msg.encode())


main()
