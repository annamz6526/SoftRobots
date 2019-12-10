import csv
import numpy as np
import random
from env import ENV
import math
import os 
os.environ["CUDA_VISIBLE_DEVICES"]="1"
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Activation, MaxPooling2D, Flatten, BatchNormalization
from keras.callbacks import Callback
from keras.optimizers import Adam

from collections import deque

actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))



class DQN:
    def __init__(self, env, batch_size = 32):
        self.env = env
        self.memory = deque(maxlen=10000)
        self.batch_size = batch_size
        self.step = 0
        self.gamma = 0.9
        self.eps_start = 0.9
        self.eps_end = 0.1
        self.eps_decay = 500
        self.epsilon = 0.9
        # self.epsilon_min = 0.05
        # self.epsilon_decay = 0.995
        self.learning_rate = 0.0005
        self.tau = .125
        self.loss_log = []
        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        state_shape = self.env.img_size

        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=(state_shape[0], state_shape[1], 1)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        # model.add(Conv2D(32, (3, 3)))
        # model.add(BatchNormalization())
        # model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, (3, 3), padding='same'))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))



        model.add(Flatten())
        model.add(Dense(512, activation="relu"))
        model.add(Dense(256, activation="relu"))
        # model.add(BatchNormalization())
        model.add(Dense(128, activation="relu"))
        model.add(Dense(len(self.env.action_space)))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        model.summary()
        return model

    def act(self, state):
        # if self.step % 25 == 0:
        #     self.epsilon *= self.epsilon_decay
        #     self.epsilon = max(self.epsilon_min, self.epsilon)
        #     print('eps: ', self.epsilon)
        self.epsilon = self.eps_end + (self.eps_start - self.eps_end) * math.exp(-1. * self.step / self.eps_decay)
        self.step += 1
        if random.random() < self.epsilon:
            return self.env.sample_action()
        print('eps: ', self.epsilon)
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        # q_value = []
        samples = random.sample(self.memory, self.batch_size)

        state, target, q_value = self.create_minibatch(samples)
        history = LossHistory()

        self.model.fit(state, target, epochs=1, batch_size = self.batch_size,
                        verbose=1,callbacks=[history])
        self.loss_log.append(history.losses)
        q_value = np.mean(q_value)

        return q_value


        # for sample in samples:
        #     state, action, reward, new_state, done = sample
        #     target = self.target_model.predict(state)
        #     if done:
        #         target[0][action] = reward
        #     else:
        #         Q_future = max(self.target_model.predict(new_state)[0])
        #         print('Q_future: {}, reward: {}'.format(Q_future, reward))
        #         target[0][action] = reward + Q_future * self.gamma
        #         q_value.append(Q_future)
        #     history = LossHistory()

        #     self.model.fit(state, target, epochs=1, verbose=0,callbacks=[history])
        #     self.loss_log.append(history.losses)

        # return np.mean(q_value) if q_value else 0.0

    def create_minibatch(self, samples):
        mb_len = len(samples)
        state_shape = self.env.img_size
        old_states = np.zeros(shape=(mb_len, state_shape[0], state_shape[1], 1))
        actions = np.zeros(shape=(mb_len,))
        rewards = np.zeros(shape=(mb_len,))
        terminations = np.empty(shape=(mb_len,))
        new_states = np.zeros(shape=(mb_len, state_shape[0], state_shape[1], 1))

        
        for i, sample in enumerate(samples):
            state, action, reward, new_state, done = sample
            old_states[i, :] = state[...]
            actions[i] = action
            rewards[i] = reward
            terminations[i] = done
            new_states[i, :] = new_state[...]
        # print('reward: {}'.format(rewards))
        old_qvals = self.target_model.predict(old_states, batch_size=mb_len)
        new_qvals = self.target_model.predict(new_states, batch_size=mb_len)

        maxQs = np.max(new_qvals, axis=1)

        y = old_qvals
        #non_term_inds = np.where(np.logical_and(rewards != posreward, rewards != negreward))[0]
        #term_inds = np.where(np.logical_or(rewards == posreward, rewards == negreward))[0]
        non_term_inds = np.where(terminations == False)[0]
        term_inds = np.where(terminations == True)[0]

        y[non_term_inds, actions[non_term_inds].astype(int)] = rewards[non_term_inds] + (self.gamma * maxQs[non_term_inds])
        y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]
        #print (y[non_term_inds, actions[non_term_inds].astype(int)] )
        X_train = old_states
        y_train = y
        return X_train, y_train, maxQs

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)
        self.target_model.save(''.join(fn.split('.')[:-1])+'target.h5')

    def log_result(self):
        with open('reward_and_Q/loss_data.csv', 'w') as f:
            wr = csv.writer(f)
            for loss_item in self.loss_log:
                wr.writerow(loss_item)
