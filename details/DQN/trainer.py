import socket
from env import ENV
from dqn import DQN
import cv2
import numpy as np
import os
# import random
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.optimizers import Adam
#
# from collections import deque

# def listenToInit():
#	 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#	 sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#	 sock.bind(('0.0.0.0', 7777))

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

def main():
	env = ENV(actions, (224, 224))
	gamma = 0.9
	epsilon = .95
	model_ph = 'models'
	if not os.path.exists(model_ph):
		os.mkdir(model_ph)
	trials = 1000
	trial_len = 500
	
	# updateTargetNetwork = 1000
	dqn_agent = DQN(env=env)
	steps = []
	for trial in range(trials):
		cur_state = env.reset()
		for step in range(trial_len):
			print('trial: {}, step: {}'.format(trial, step))
			action = dqn_agent.act(cur_state)
			new_state, reward, done = env.step(action)
	
			# reward = reward if not done else -20
			new_state = new_state
			dqn_agent.remember(cur_state, action, reward, new_state, done)
	
			dqn_agent.replay()  # internally iterates default (prediction) model
			dqn_agent.target_train()  # iterates target model
	
			cur_state = new_state
			if done:
				break
		if step >= 10:
			print("Failed to complete in trial {}".format(trial))
			if step % 10 == 0:
				dqn_agent.save_model(os.path.join(model_ph, "trial-{}.model").format(trial))
		else:
			print("Completed in {} trials".format(trial))
			dqn_agent.save_model(os.path.join(model_ph, "success.model"))
			break
	# Test
	# env = ENV(actions, (224, 224))
	# # fn = 'test_data/1.jpg'
	# # resized_img = env.img_loader(fn)
	# # print(resized_img)
	# image = env.reset()
	# # cv2.imshow('img', image)

	# # cv2.waitKey(0)
	# # cv2.destroyAllWindows()
	
	# env.sample_action()
	# print(env.step(2))
	# for i in range(399):
	# 	env.step(np.random.randint(7))



if __name__ == "__main__":
	main()