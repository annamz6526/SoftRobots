from flat_game import carmunk
import numpy as np
import random
import csv
from nn import neural_net, LossHistory
import os.path
import timeit

NUM_INPUT = 40 +3
GAMMA = 0.9  # Forgetting.
TUNING = False  # If False, just use arbitrary, pre-selected params.
negreward = -200
posreward = 100
step_size = 4
def train_net(model, params):

    filename = params_to_filename(params)

    observe =40000  # Number of frames to observe before training.
    epsilon = 1
    train_frames = 11*observe # Number of frames to play.
    batchSize = params['batchSize']
    buffer = params['buffer']

    # Just stuff used below.
    max_car_distance = 400000
    car_distance = 400000
    t = 0
    data_collect = []
    replay = []  # stores tuples of (S, A, R, S').

    loss_log = []
    reward_log = []
    cu_reward = 0

    # Create a new game instance.
    game_state = carmunk.GameState()

    # Get initial state by doing nothing and getting the state.
    _, state = game_state.frame_step((2))

    # Let's time it.
    start_time = timeit.default_timer()

    # Run the frames.
    while t < train_frames:

        t += 1
        car_distance += 1

        # Choose an action.
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0, 3)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best

        # Take action, observe new state and get our treat.
        reward, new_state = game_state.frame_step(action)
        if t < observe:
        # Experience replay storage.
           replay.append((state, action, reward, new_state))
        if t%1000 == 0 :
           log_results(filename, data_collect, loss_log,reward_log)
           print("S,A,R,S,",(state, action, reward, new_state))
        # If we're done observing, start training.
        if t > observe and t%20 == 0:

            # If we've stored enough in our buffer, pop the oldest.
            if len(replay) > buffer:
                replay.pop(0)

            # Randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)

            # Get training values.
            X_train, y_train = process_minibatch2(minibatch, model)

            # Train the model on this batch.
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
            )
            loss_log.append(history.losses)

        # Decrement epsilon over time.
        if epsilon > 0.1 and t > observe:
             epsilon -= (1.0/(train_frames))

        # Update the starting state with S'.
        state = new_state

        cu_reward = cu_reward + reward
        reward_log.append([t,cu_reward])        
        if reward !=negreward:
            cu_reward = cu_reward
        else:
            cu_reward = 0
        #print(cu_reward)

       
        #print("reward is ",reward)
        # We died, so update stuff.
        if reward == negreward:
            # Log the car's distance at this T.
            data_collect.append([t, car_distance])

            # Update max.
            if car_distance < max_car_distance:
                max_car_distance = car_distance

            # Time it.
            tot_time = timeit.default_timer() - start_time
            fps = car_distance / tot_time

            # Output some stuff so we can watch.
            print("Min: %d at %d\tepsilon %f\t(%d)\t%f fps" %
                  (max_car_distance, t, epsilon, car_distance, fps))

            # Reset.
            car_distance = 0
            start_time = timeit.default_timer()

        # Save the model every 25,000 frames.
        if t % (train_frames/10) == 0:
            model.save_weights('saved-models/' + filename + '-' +
                               str(t) + '.h5',
                               overwrite=True)
             
            model.save_weights('saved-models/continuous.h5',
                               overwrite=True)
            print("Saving model %s - %d" % (filename, t))
            #log_results(filename, data_collect, loss_log)

    # Log results after we're done all frames.
    log_results(filename, data_collect, loss_log,reward_log)


def log_results(filename, data_collect, loss_log, reward_log):
    # Save the results to a file so we can graph it later.
    with open('results/sonar-frames/learn_data-' + filename + '.csv', 'w') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/sonar-frames/loss_data-' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)
    with open('results/sonar-frames/reward_data-' + filename + '.csv', 'w') as rw:
        wr = csv.writer(rw)
        for loss_item in reward_log:
            wr.writerow(loss_item)

def process_minibatch2(minibatch, model):
    # by Microos, improve this batch processing function 
    #   and gain 50~60x faster speed (tested on GTX 1080)
    #   significantly increase the training FPS
    
    # instead of feeding data to the model one by one, 
    #   feed the whole batch is much more efficient

    mb_len = len(minibatch)

    old_states = np.zeros(shape=(mb_len, NUM_INPUT))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, NUM_INPUT))

    for i, m in enumerate(minibatch):
        old_state_m, action_m, reward_m, new_state_m = m
        old_states[i, :] = old_state_m[...]
        actions[i] = action_m
        rewards[i] = reward_m
        new_states[i, :] = new_state_m[...]

    old_qvals = model.predict(old_states, batch_size=mb_len)
    new_qvals = model.predict(new_states, batch_size=mb_len)

    maxQs = np.max(new_qvals, axis=1)
    y = old_qvals
    #non_term_inds = np.where(np.logical_and(rewards != posreward, rewards != negreward))[0]
    #term_inds = np.where(np.logical_or(rewards == posreward, rewards == negreward))[0]
    non_term_inds = np.where(rewards != negreward)[0]
    term_inds = np.where(rewards == negreward)[0]

    y[non_term_inds, actions[non_term_inds].astype(int)] = rewards[non_term_inds] + (GAMMA * maxQs[non_term_inds])
    y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]
    #print (y[non_term_inds, actions[non_term_inds].astype(int)] )
    X_train = old_states
    y_train = y
    return X_train, y_train

def params_to_filename(params):
    return str(params['nn'][0]) + '-' + str(params['nn'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params):
    filename = params_to_filename(params)
    print("Trying %s" % filename)
    # Make sure we haven't run this one.
    if not os.path.isfile('results/sonar-frames/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('results/sonar-frames/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(NUM_INPUT, params['nn'])
        train_net(model, params)
    else:
        print("Already tested.")


if __name__ == "__main__":
    if TUNING:
        param_list = []
        nn_params = [[164, 150], [256, 256],
                     [512, 512], [1000, 1000]]
        batchSizes = [40, 100, 400]
        buffers = [10000, 50000]

        for nn_param in nn_params:
            for batchSize in batchSizes:
                for buffer in buffers:
                    params = {
                        "batchSize": batchSize,
                        "buffer": buffer,
                        "nn": nn_param
                    }
                    param_list.append(params)

        for param_set in param_list:
            launch_learn(param_set)

    else:
        nn_param = [512, 512]
        params = {
            "batchSize": 100,
            "buffer": 50000,
            "nn": nn_param
        }
#        model = neural_net(NUM_INPUT, nn_param,load='saved-models/64-128-64-50000-50000.h5')
        #model = neural_net(NUM_INPUT, nn_param,load='saved-models/continuous.h5')
        model = neural_net(NUM_INPUT, nn_param)
        train_net(model, params)


