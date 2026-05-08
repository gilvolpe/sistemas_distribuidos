import socket
import threading

server_host = '127.0.0.1'
server_port = 5000

list_clientes = []
client_lock = threading.Lock()

def enviar_mensagem(msg, remetente):
    with client_lock:
        for cliente in list_clientes:
            if cliente is not remetente:
                try:
                    cliente.sendall(msg)
                except:
                    pass

def lidar_conexao(conexao, endereco):
    print(f'Novo cliente {endereco}')
    conexao.sendall('Ola, seja bem vindo! Escreva uma mensagem e aperte Enter'.encode('utf-8'))
    try:
        while True:
            data = conexao.recv(1024)
            if not data:
                break
            msg = f'{endereco[0]}:{endereco[1]}:\t'.encode('utf-8') + data
            enviar_mensagem(msg, remetente=conexao)
    finally:
        with client_lock:
            if conexao in list_clientes:
                list_clientes.remove(conexao)
        conexao.close()

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((server_host, server_port))
    server.listen()

    try:
        while True:
            cliente, addr = server.accept()
            with client_lock:
                list_clientes.append(cliente)

            t = threading.Thread(target=lidar_conexao,args=(cliente,addr,),daemon=1)
            t.start()
    except KeyboardInterrupt:
        print('Terminando o servidor')
    finally:
        server.close()
