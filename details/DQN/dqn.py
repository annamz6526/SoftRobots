import socket
import json
import numpy as np
import random
from env import ENV
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Activation, MaxPooling2D, Flatten
from keras.optimizers import Adam

from collections import deque

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

# data = [
#     'img_name':,
#     'reward':,
#
# ]




class DQN:
    def __init__(self, env, batch_size):
        self.env = env
        self.memory = deque(maxlen=2000)
        self.batch_size = batch_size

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        state_shape = self.env.state_shape

        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=state_shape.shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(256, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(len(self.env.action_space)))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.sample_action()
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        samples = random.sample(self.memory, self.batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)


# def main():
#     env = gym.make("MountainCar-v0")
#     gamma = 0.9
#     epsilon = .95
#
#     trials = 1000
#     trial_len = 500
#
#     # updateTargetNetwork = 1000
#     dqn_agent = DQN(env=env)
#     steps = []
#     for trial in range(trials):
#         cur_state = env.reset().reshape(1, 2)
#         for step in range(trial_len):
#             action = dqn_agent.act(cur_state)
#             new_state, reward, done, _ = env.step(action)
#
#             # reward = reward if not done else -20
#             new_state = new_state.reshape(1, 2)
#             dqn_agent.remember(cur_state, action, reward, new_state, done)
#
#             dqn_agent.replay()  # internally iterates default (prediction) model
#             dqn_agent.target_train()  # iterates target model
#
#             cur_state = new_state
#             if done:
#                 break
#         if step >= 199:
#             print("Failed to complete in trial {}".format(trial))
#             if step % 10 == 0:
#                 dqn_agent.save_model("trial-{}.model".format(trial))
#         else:
#             print("Completed in {} trials".format(trial))
#             dqn_agent.save_model("success.model")
#             break


# if __name__ == "__main__":
#     # main()