import socket
import json
import numpy as np
import random
from collections import deque

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

# data = [
#     'img_name':,
#     'reward':,
#
# ]


class ENV(object):
    def __init__(self, action_space, state_space):
        self.action_space = action_space
        self.state_shape = state_space
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def sample_action(self):
        return np.random.choice(len(self.action_space))

    def sendMessageOnly(self, msg, ip, port):
        msg = json.dumps(msg).encode('utf-8')
        self.sock.sendto(msg, (ip, port))

    def step(self, action):
        data = {
            'state' : 'step',
            'action' : action
        }
        self.sendMessageOnly(data, '0.0.0.0', 7777)
        received, addr = self.sock.recvfrom(1024)
        data = json.loads(received.decode('utf-8'))
        print (data)
        return data

    def reset(self):
        data = {
            'state': 'reset',
        }
        self.sendMessageOnly(data, '0.0.0.0', 7777)
        received, addr = self.sock.recvfrom(1024)
        data = json.loads(received.decode('utf-8'))
        print (data)
        return data