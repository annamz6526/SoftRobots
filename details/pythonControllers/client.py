
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('0.0.0.0',7777))

sock.send('I am here')
ack = sock.recv(1024)
print(ack)
assert ack == 'ack'
sock.close()