import random

from collections import namedtuple
Transition = namedtuple('Transicion', ('state', 'action', 'next_state', 'next_action', 'reward'))

class ReplayMemory:
    
    def __init__(self):
        # self.capacity = CAPACITY #メモリの最大値
        self.memory = [] # 経験を保存するリスト
        self.index = 0 # 保存するindexを表す変数

    def push(self, state, action, state_next, next_action, reward):
        '''trasicion = (state, action, state_next, reward)をメモリ保存する'''
        self.memory.append(None) # メモリが満タンじゃないときは足す

        # namedtupleのTransitionを用意し、値とフィールド名をペアにする
        self.memory[self.index] = Transition(state, action, state_next, next_action, reward)

        self.index = (self.index + 1) # 保存するindexを1つずらす

    def sample(self, batch_size):
        '''batch_sizeだけ、ランダムに取り出す'''
        return random.sample(self.memory, batch_size)

    def __len__(self):
        '''関数lenに対して、現在のmemoryの長さを返す'''
        return len(self.memory)