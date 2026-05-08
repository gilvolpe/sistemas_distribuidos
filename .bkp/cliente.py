import socket
import threading
import sys

server_host = '127.0.0.1'
server_port = 5000

def receber_msg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print('\r[servidor caiu]')
                break
            msg = data.decode('utf-8').strip()
            print(f'\r{msg}')
            print("> ", end="", flush=True)
        except:
            break

if __name__ == '__main__':
    cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente.connect((server_host,server_port))

    t = threading.Thread(target=receber_msg,args=(cliente,),daemon=1)
    t.start()

    sys.stdout.write('> ')
    sys.stdout.flush()

    try:
        while True:
            msg = input('> ')
            if msg:
                cliente.sendall(msg.encode('utf-8'))
    except:
        pass
    finally:
        cliente.close()


