import socket
import threading
import sys
import time

PORT = 9000
address_lock = threading.Lock()
address_list = []

def f_send_address(conn, addr):
    try:
        with address_lock:
            payload = ';'.join(address_list)
        print(f'[*] Enviado lista de endereços conhecidos {payload}')
        conn.send(payload.encode('utf-8'))
        time.sleep(3)
    except:
        pass
    finally:
        print(f'[*] finalizando conexão após envio da lista de nós conhecidos')
        conn.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    server_ip = args[0]

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server.bind((server_ip,PORT))
    server.listen()
    
    print('[*] Servidor iniciado')
    while True:
        conn, addr = server.accept()
        with address_lock:
            address_list.append(addr[0])
        
        t = threading.Thread(target=f_send_address,args=(conn,addr,),daemon=True)
        t.start()
