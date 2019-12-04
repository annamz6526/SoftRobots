import socket
from threading import Thread
import threading


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.listen(1)
# while True:
# 	conn, addr = sock.accept()
# 	while conn:
# 	# received, addr = sock.accept()
# 		data = conn.recv(1024)
# 		if data:
# 			conn.send('ack')
# 		else:
# 			break
# while True:
# 	data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
# 	print(data)
# 	if data:
# 		sock.sendto('ack', addr)
# 	else:
# 		continue


# data = {
# 	'state': 'init', #string
# 	'action': 1, #int
#
# }
def listenToEnv(server_addr):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((server_addr))
	while True:
		data, addr = sock.recvfrom(1024)
		state = data['state']
		if state == 'init':
			pass
		elif state == 'action':
			pass
			break
		else:
			pass






if __name__ == "__main__":
	server_addr = ('0.0.0.0', 7777)
	listenToEnv(server_addr)