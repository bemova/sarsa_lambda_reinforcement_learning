import numpy as np
import pandas as pd
from copy import deepcopy


class SARSALambdaLearning():
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, eligibility_trace_decay=0.9, df=None):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.eligibility_trace_decay = eligibility_trace_decay

        # df is a data frame of pretrained Q table
        if df is None:
            self.Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        else:
            self.Q = df

        # et is our eligibility trace matrix which we are using in q lambda learning approach
        self.et = deepcopy(self.Q)

    def choose_action(self, state):
        self.check_state_exist(state)
        rand = np.random.uniform()
        if rand < self.epsilon:
            # this case we have to select the beast action based on Q table
            # which is the action that has the max value
            state_action = self.Q.loc[state, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            #  in this case we let the agent to have some exploration on the environment
            action = np.random.choice(self.actions)
        return action

    def sarsa_lambda(self, state, action, reward, next_state, next_action):
        self.check_state_exist(next_state)
        predict = self.Q.ix[state, action]
        if next_state != 'terminal':
            target = reward + self.gamma * self.Q.loc[next_state, next_action]
        else:
            target = reward

        self.et.loc[state, action] += 1
        # Q update
        self.Q += self.lr * (target - predict) * self.et

        # decay eligibility trace after update
        self.et *= self.gamma * self.eligibility_trace_decay

    def check_state_exist(self, state):
        if state not in self.Q.index.astype(str):
            zero_series = pd.Series([0] * len(self.actions), index=self.Q.columns, name=state)
            self.Q = self.Q.append(zero_series)
            self.et = self.et.append(zero_series)

