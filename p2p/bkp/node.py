import socket
import threading
import time
import os
import sys
import random

SERVER_ADDRESS = '192.168.1.3'
SERVER_PORT    = 6000
PEER_PORT      = 9000
PEERS_LOCK = threading.Lock()
CONN = []
ADDR = []

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()

    def f_bootstrap(self, client):
        test = True
        while test:
            try:
                print('[*] aguardando mensagem')
                data = client.recv(1024).decode('utf-8')
                with PEERS_LOCK:
                    list_of_ips = data.split(',')
                    list_of_ips = [ _ for _ in list_of_ips if _ != self.host]
                    list_of_ips = [ _  for _ in list_of_ips if len(_.split('.')) == 4 ]
                    self.peers.update(list_of_ips) # 172 . 20 . 10. 40
                    print(f'[*] lista de ips disponiveis {self.peers}')
            except:
                client.close()
                test = False
                break
    
    def connect_boostrap(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS,SERVER_PORT))

        t = threading.Thread(target=self.f_bootstrap,args=(client,),daemon=1)
        t.start()

    def f_peer(self,conn,addr):
        data = conn.recv(1024)
        if data:
            print(f"[+] Mensagem recebida de {addr[0]}:{data.decode('utf-8')}")
            with PEERS_LOCK:
                if addr[0] not in self.peers:
                    self.peers.update(addr[0])
        conn.close()

    def f_connect_to_peer(self):
        while True:
            my_sleep = random.choice([3,4,5,6,7])
            messages = ['Teste', 'Agora vai', 'Que doido', 'ÉEEguuua']

            with PEERS_LOCK:
                lista_peers = list(self.peers)
                lista_palavas = [ _ for _ in range(len(messages))]
                for p in lista_peers:
                    try:
                        idx_msg = random.choice(lista_palavas)
                        print(f'{idx_msg} {messages[idx_msg]}')
                        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        client.connect((p,self.port))
                        client.send(messages[idx_msg].encode('utf-8'))
                    except:
                        print(f'[-] Problema na conexao com {p}:{self.port}')
                    finally:
                        client.close()

            time.sleep(my_sleep)

    def start_server_p2p(self):
        print((self.host,self.port))
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((self.host,self.port))
        server.listen()

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.f_peer,args=(conn,addr,),daemon=1)
            t.start()


    def run(self):
        self.connect_boostrap()
        t1 = threading.Thread(target=self.start_server_p2p,daemon=1)
        t2 = threading.Thread(target=self.f_connect_to_peer,daemon=1)
        
        t1.start()
        t2.start()

        while True:
            print('[*] Nó vivo e recebendo mensagem')
            time.sleep(10)

if __name__ == "__main__":
    args = sys.argv[1:]
    server_bootstrap_ip = args[0]
    # O Docker nos passará o HOSTNAME e o BOOTSTRAP via variáveis de ambiente
    MY_IP = socket.gethostbyname(socket.gethostname())
    SERVER_ADDRESS = server_bootstrap_ip

    node = P2PNode(MY_IP, PEER_PORT)
    node.run()
