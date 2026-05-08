import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',12345))
server.listen(1)

conn, addr = server.accept()
print(f'Servidor recebeu a conexao de {addr}')

data = conn.recv(1024)
print(f'a informacao recebida foi {data.decode('utf-8')}')
conn.send('Ola amigo! Bora no madeirão - Pereco'.encode('utf-8'))

conn.close()
