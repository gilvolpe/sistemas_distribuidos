import threading
import socket
import sys
import random


SERVER_PORT = 9000
P2P_PORT = 6000
list_of_addres_lock = threading.Lock()


class P2PNode:
    def __init__(self, host, port, server_host, server_port):
        self.host = host
        self.port = port
        self.server_host = server_host
        self.server_port = server_port

        self.peers = set()

    def start_node(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_host, self.server_port))
        print('[*] Conectando ao servidor bootstrap')

        data = client.recv(4096).decode('utf-8')
        if data:
            address_list = data.split(';')
            address_list = [ _ for _ in address_list if _ != self.host]
            with list_of_addres_lock:
                self.peers.update(address_list)
            print(f'[*] Recebeu a lista de nós conhecidos {self.peers}')
        
        client.close()
        print('[*] Fechando conexão com o servidor bootstrap')

    def connection_p2p(self, conn, addr):
        try:
            data = conn.recv(4096).decode('utf-8')
            if data:
                print(f'[*] Redebendo a mensagem {data} de {addr[0]}')
            with list_of_addres_lock:
                list_of_peers = list(self.peers)
                if not addr[0] in list_of_peers:
                    self.peers.add(addr[0])
        except:
            pass
        finally:
            conn.close()

    def server_node_p2p(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((self.host,self.port))
        server.listen()

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.connection_p2p,args=(conn,addr,),daemon=1)
            t.start()
    
    def send_msg(self):
    
        MSG = ['éeeeguuuua','mas quando','pai dégua',\
                'papa xibe','carimbó']
        
        while True:

            seconds_to_sleep = [1,2,3,4,5,6,7,8,9,10]
            with list_of_addres_lock:
                list_peers = list(self.peers)
                print(f'List of peers to conect {list_peers}')

            if len(list_peers) > 0:
                ip  = random.choice(list_peers)
                msg = random.choice(MSG)

                client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client.connect((ip,self.port))
                client.send(msg.encode('utf-8'))
                client.close()

                time.sleep(random.choice(seconds_to_sleep))
        
    def run(self):
        self.start_node()
        t_sn = threading.Thread(target=self.server_node_p2p,daemon=1)
        t_sm = threading.Thread(target=self.send_msg,daemon=1)
        t_sn.start()
        t_sm.start()

        while True:
            i = 1



if __name__ == '__main__':
    args = sys.argv[1:]
    server_ip = args[0]

    my_ip = socket.gethostbyname(socket.gethostname())

    node = P2PNode(my_ip, P2P_PORT, server_ip, SERVER_PORT)
    node.run()
