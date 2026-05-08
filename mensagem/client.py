import threading
import socket
import sys

server_host = 'localhost'
server_port = 12345

def f_readmsg(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')
            print(f'\r{msg}')
            print('> ',end='',flush=True)
        except:
            break



if __name__ == '__main__':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((server_host,server_port))

    t = threading.Thread(target=f_readmsg,args=(client,),daemon=1)
    t.start()
    
    try:
        while True:
            msg = input('> ')
            if msg:
                client.send(msg.encode('utf-8'))
    except:
        pass
    finally:
        client.close()




