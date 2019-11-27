import socket
from threading import Thread
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 7777))
sock.listen(5)
while True:
	conn, addr = sock.accept()
	while conn:
	# received, addr = sock.accept()
		data = conn.recv(1024)
		if data:
			conn.send('ack')
		else:
			break


