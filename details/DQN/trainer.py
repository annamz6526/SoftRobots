import socket
from env import ENV
from dqn import DQN
import cv2
import numpy as np
import os
import pickle


actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

def main():
	original_size = (782, 600)
	env = ENV(actions, (original_size[0]/5, original_size[1]/5))
	gamma = 0.9
	epsilon = .95
	model_ph = 'models'
	if not os.path.exists(model_ph):
		os.mkdir(model_ph)
	trials = 500
	trial_len = 1000
	rewards = []
	q_values = []

	dqn_agent = DQN(env=env)
	success_num = 0
	steps = []
	for trial in range(1, trials):
		t_reward = []
		t_qvalue = []
		cur_state = env.reset()
		for step in range(trial_len):
			action = dqn_agent.act(cur_state)
			new_state, reward, done, success = env.step(action)
			t_reward.append(reward)
			
			# reward = reward if not done else -20
			new_state = new_state
			dqn_agent.remember(cur_state, action, reward, new_state, done)
	
			q_value = dqn_agent.replay()  # internally iterates default (prediction) model
			if q_value:
				t_qvalue.append(q_value)
			else:
				t_qvalue.append(0.0)
			dqn_agent.target_train()  # iterates target model
			dqn_agent.log_result()
			cur_state = new_state
			if success:
				success_num += 1
				print("Completed in {} trials".format(trial))
				dqn_agent.save_model(os.path.join(model_ph, "success-model.h5"))
				break
			if done:
				print("Failed to complete in trial {}, step {}".format(trial, step))
				dqn_agent.save_model(os.path.join(model_ph, "trial-{}-model.h5").format(trial))
				break
		rewards.append(np.mean(t_reward) if t_reward else 0.0)
		q_values.append(np.mean(t_qvalue) if t_qvalue else 0.0)
		# dqn_agent.log_result()
		with open('reward_and_Q/reward.txt', 'wb') as f:
			pickle.dump(rewards, f)
		with open('reward_and_Q/qvalue.txt', 'wb') as f:
			pickle.dump(q_values, f)
		print('trial: {}, success acc: {}'.format(trial, success_num / float(trial)))
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