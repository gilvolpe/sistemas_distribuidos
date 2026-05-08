import socket
import threading
import time
import json

PORT=6000
clients_addr = []
clients_list = []
clients_list_lock = threading.Lock()
clients_addr_lock = threading.Lock()

def f_client(conn, addr):
    try:
        while True:
            with clients_addr_lock:
                payload = ','.join(clients_addr).encode('utf-8')
            
            print(f'[*] enviando mensagem para {addr} conteudo {payload}')        
            conn.send(payload)
            time.sleep(1)
    finally:
        with clients_list_lock:
            if conn in clients_list:
                clients_list.remove(conn)
            conn.close()
        with clients_addr_lock:
            if addr in clients_addr:
                clients_addr.remove(addr)



if __name__ == '__main__':
    MY_IP = socket.gethostbyname(socket.gethostname())
    print(MY_IP)
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((MY_IP,PORT))
    server.listen()
    print('[*] Servidor inicializado, ponto de entrada')

    while True:
        conn, addr = server.accept()
        with clients_list_lock:
            clients_list.append(conn)

        with clients_addr_lock:
            clients_addr.append(addr[0])
            print(addr[0])

        t = threading.Thread(target=f_client,args=(conn,addr,),daemon=1)
        t.start()


