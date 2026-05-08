import threading
import socket

server_port = 12345
server_host = 'localhost'

lista_clients = []
client_lock = threading.Lock()

def f_sendall(msg, remetente):
    with client_lock:
        for cli in lista_clients:
            if cli is not remetente:
                try:
                    cli.send(msg)
                except:
                    pass

def f_client(conn, addr):
    print(f'A conexao {addr} chegou')
    conn.send('Ola seja bem vindo conexao!'.encode('utf-8'))
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = f'{addr[0]}:{addr[1]} => '.encode('utf-8') + data
            f_sendall(msg, conn)
    finally:
        with client_lock:
            if conn in lista_clients:
                lista_clients.remove(conn)
        conn.close()

'''
int main(){

}
'''
if __name__ == '__main__':
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((server_host,server_port))
    server.listen()

    try:
        while True:
            conn, addr = server.accept()
            with client_lock:
                lista_clients.append(conn)

            t = threading.Thread(target=f_client,args=(conn,addr,),daemon=1)
            t.start()
    except KeyboardInterrupt:
        print('Terminando o servidor')
    finally:
        server.close()



