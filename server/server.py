import socket
from threading import Thread

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5002

clients = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f'[*] Listening on {SERVER_HOST}:{SERVER_PORT}')


def listen_clients(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f'[!] Client Desconnected')
            clients.remove(cs)
        for client in clients:
            client.send(msg.encode())


while True:
    client, client_addr = s.accept()
    print([f'[+] {client_addr} connected'])
    clients.add(client)

    t = Thread(target=listen_clients, args=(client,))

    t.daemon = True
    t.start()
