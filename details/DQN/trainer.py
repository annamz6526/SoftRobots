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
	env = ENV(actions, (original_size[0]/6, original_size[1]/6))
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
	rewards = []
	q_values = []
	Q = []
	for trial in range(1, trials):
		t_reward = []
		t_qvalue = []
		cur_state = env.reset()
		for step in range(trial_len):
			action = dqn_agent.act(cur_state)
			new_state, reward, done, success = env.step(action)
			t_reward.append(reward)
			
			# reward = reward if not done else -20
			dqn_agent.remember(cur_state, action, reward, new_state, done)
	
			q_value = dqn_agent.replay()  # internally iterates default (prediction) model
			if q_value:
				t_qvalue.append(q_value)
				Q.append(q_value)
			else:
				t_qvalue.append(0.0)
				Q.append(0.0)
			dqn_agent.target_train()  # iterates target model
			cur_state = new_state

			dqn_agent.log_result()

			save_q(Q)

			if success:
				success_num += 1
				dqn_agent.step = 100
				print("Completed in {} trials".format(trial))
				dqn_agent.save_model(os.path.join(model_ph, "success-model.h5"))
				break
			if done:
				print("Failed to complete in trial {}, step {}".format(trial, step))
				dqn_agent.save_model(os.path.join(model_ph, "trial-{}-model.h5").format(trial))
				break
		rewards.append(np.sum(t_reward) if t_reward else 0.0)
		q_values.append(np.mean(t_qvalue) if t_qvalue else 0.0)
		
		with open('reward_and_Q/reward.txt', 'wb') as f:
			pickle.dump(rewards, f)
		with open('reward_and_Q/qvalue.txt', 'wb') as f:
			pickle.dump(q_values, f)
		print('trial: {}, success acc: {}'.format(trial, success_num / float(trial)))

def save_q(Q):
	with open('reward_and_Q/Q.txt', 'wb') as f:
		pickle.dump(Q, f)



if __name__ == "__main__":
	main()