import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',12345))

client.send('Olá meu amigo! partiu Calourada'.encode('utf-8'))

msg = client.recv(1024)
print(f'O servidor enviou {msg.decode('utf-8')}')

client.close()

