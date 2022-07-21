import socket
import threading

IP = '192.168.0.1'
PORT = 9999

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)

    print(f'[*] Listening on {IP}:{PORT}')

    client, addr = server.accept()
    print(f'[*] Accepted connection from {client}, {addr[0]}:{addr[1]}')
    print(f'{addr}')

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

def handle_client(client):
    with client as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()