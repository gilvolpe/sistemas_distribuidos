import socket
import threading
import time
import json
import sys


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
    args = sys.argv[1:]
    server_ip = args[0]
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((server_ip,PORT))
    server.listen()
    print('[*] Servidor inicializado, ponto de entrada')

    try:
        while True:
            conn, addr = server.accept()
            with clients_list_lock:
                clients_list.append(conn)

            with clients_addr_lock:
                clients_addr.append(addr[0])
                print(addr[0])

            t = threading.Thread(target=f_client,args=(conn,addr,),daemon=1)
            t.start()
    except KeyboardInterrupt:
        print('[-] Terminal finalizado')
    finally:
        server.close()

    

