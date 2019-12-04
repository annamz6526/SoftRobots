import socket
from env import ENV
# import numpy as np
# import random
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.optimizers import Adam
#
# from collections import deque

# def listenToInit():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(('0.0.0.0', 7777))

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

def main():
    env = ENV(actions, (0,0,0))
    env.reset()
    env.sample_action()
    env.step(2)



if __name__ == "__main__":
    main()