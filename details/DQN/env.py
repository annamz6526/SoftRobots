import socket
import json
import numpy as np

# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import random
from collections import deque

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

root_path = '/home/zshen15'

# data = [
#     'imgName':,
#     'reward':,
#
# ]

class ENV(object):
    def __init__(self, action_space = None, img_size = (224,224)):
        self.action_space = action_space
        self.img_size = img_size
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
            'action' : int(action)
        }
        self.sendMessageOnly(data, '0.0.0.0', 7777)
        received, addr = self.sock.recvfrom(1024)
        data = json.loads(received.decode('utf-8'))
        state = (self.img_loader(data['imgName']))

        return state, data['reward'], data['done']

    def reset(self):
        data = {
            'state': 'reset',
        }
        self.sendMessageOnly(data, '0.0.0.0', 7777)
        received, addr = self.sock.recvfrom(1024)
        data = json.loads(received.decode('utf-8'))
        state = (self.img_loader(data['imgName']))

        return state

    def img_loader(self, fn):
        fn = fn.replace('~', root_path)
        image = cv2.imread(fn)
        resized_img = cv2.resize(image, self.img_size)
        gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        gray = gray.astype('float32') / 255
        gray = gray.reshape(-1, self.img_size[0], self.img_size[1], 1)
        return gray
