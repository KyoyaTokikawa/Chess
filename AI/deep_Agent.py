from .deep_brain import *

class Agent:
    def __init__(self, num_states, num_actions, param):
        '''課題の状態と行動の数を設定する'''
        self.brain = Brain(num_states, num_actions, param)
        self.reward_rate = param[3]

        a = 1
        # エージェントが行動を決定するための頭脳を生成
        
    def update_q_network(self):
        '''Q関数を更新する'''
        self.brain.replay()
        
    def update_target_model(self):
        self.brain.update_target_model()
        
    def get_action(self, state, episode, attck_move_dic, random_count, AI_count):
        '''行動を決定する'''
        action, random_count, AI_count, random_or_AI = self.brain.decide_action(state, episode, attck_move_dic, random_count, AI_count)
        return action, random_count, AI_count, random_or_AI
    
    def memorize(self, state, action, state_next, next_action, reward):
        '''memoryオブジェクトに、state, action, state_next, rewardの内容を保存する'''
        self.brain.memory.push(state, action, state_next, next_action, reward)
    
    def predict_action(self, state):
        action = self.brain.brain_predict(state)
        return action