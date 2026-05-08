import socket
import threading
import time
import os

SERVER_ADDRESS = '192.168.1.3'
SERVER_PORT    = 6000
PEERS_LOCK = threading.Lock()


class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"[*] Nó rodando em {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        data = conn.recv(1024).decode()
        if data:
            print(f"\n[+] Mensagem recebida de {addr}: {data}")
            # Se for uma nova conexão, adiciona aos peers
            if addr[0] not in self.peers:
                self.peers.add(addr[0])
        conn.close()

    def connect_to_peer(self, peer_host):
        if peer_host == self.host: return
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((peer_host, self.port))
            client.send(f"Olá do nó {self.host}".encode())
            client.close()
            self.peers.add(peer_host)
        except Exception as e:
            print(f"[!] Falha ao conectar em {peer_host}")

    def run(self):

        


        # Inicia o servidor em uma thread separada
        threading.Thread(target=self.start_server, daemon=True).start()
        
        # Aguarda o Docker subir tudo
        time.sleep(5)

        # Tenta conectar ao nó inicial (Bootstrap)
        if self.bootstrap_node:
            print(f"[*] Tentando conexão inicial com: {self.bootstrap_node}")
            self.connect_to_peer(self.bootstrap_node)

        # Loop principal: envia um "ping" para os vizinhos a cada 10s
        while True:
            time.sleep(10)
            for peer in list(self.peers):
                print(f"[*] Enviando batida de coração para {peer}")
                self.connect_to_peer(peer)

if __name__ == "__main__":
    # O Docker nos passará o HOSTNAME e o BOOTSTRAP via variáveis de ambiente
    MY_IP = socket.gethostbyname(socket.gethostname())
    
    node = P2PNode(MY_IP, 5000)
    node.run()
