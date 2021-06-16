import random
import numpy as np
import copy
import torch
from torch import nn
from torch import optim
from torch._C import device
import torch.nn.functional as F
from collections import namedtuple
from .deep_net import *
from .ReplayMemory import *
from src.util import *
import math
Transition = namedtuple('Transicion', ('state', 'action', 'next_state', 'next_action', 'reward'))


# CAPACITY = 10000000
GAMMA = 0.90 # 時間割引率

class Brain:
    def __init__(self, num_states, num_actions, param):
        self.num_actions = num_actions # 行動の数を取得
        self.BATCH_SIZE = param[1]
        self.epsilonrate = param[2] 
        # 経験を保存するメモリオブジェクトを生成
        self.memory = ReplayMemory()
        # NNを構築
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        self.model = Net(num_states, num_actions).to(device)

        # target_net
        self.target_net = copy.deepcopy(self.model)
        self.target_net.load_state_dict(self.model.state_dict())
        
        # 最適化手法の設定
        if param[0] == 'Adam':
            self.optimizer = optim.Adam(self.model.parameters(), lr=param[4])
        elif param[0] == 'SGD':
            self.optimizer = optim.SGD(self.model.parameters(), lr=param[4])
    def replay(self):
        '''Experience Replayでネットワークの結合パラメータを出力'''
        
        # 1.1 メモリサイズがミニバッチより小さい間は何もしない
        if len(self.memory) < self.BATCH_SIZE:
            return
        
        
        # 2.1 メモリからミニバッチ分のデータを取り出す
        transitions = self.memory.sample(self.BATCH_SIZE)
        
        # 2.2 各変数をミニバッチに対応する形に変形
        # trainsicionsは1stepごとの(state, action. state_next, reward)が、self.BATCH_SIZE分格納されている
        # つまり、(state, action, state_next, reward)xself.BATCH_SIZE
        # これをミニバッチにしたい
        # (state x self.BATCH_SIZE, action x self.BATCH_SIZE, state_next x self.BATCH_SIZE, reward x self.BATCH_SIZE)にする
        batch = Transition(*zip(*transitions))
        
        # 2.3  各変数の要素をミニバッチに対応する形に変形する
        # 例えばstateの場合、[torch.FloatTensor of size 1x4]がself.BATCH_SIZE分並んでいるが、
        # それを torch.FloatTensor of self.BATCH_SIZE x 4に変換する
        
        state_batch = torch.cat(batch.state).to(self.device)
        action_batch = torch.cat(batch.action).unsqueeze(0).to(self.device)
        reward_batch = torch.cat(batch.reward).to(self.device)
        non_final_next_actions_list = []
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None]).to(self.device)
        next_action = batch.next_action
        for next_actions in next_action:
            if next_actions[0] is not None:
                a = [next_actions[0]]
                b = (self.BATCH_SIZE - len(next_actions))
                c = a * b
                temp = torch.tensor(next_actions)
                non_final_next_actions_list.append(temp)
        non_final_next_actions_list = non_final_next_actions_list
        
        
        # 3. 教師信号となるQ(s_t, a_t)値を求める
        self.model.eval()
        
        # 3.2 ネットワークが出力したQ(s_t, a_t)を求める
        # self.model(state_batch)は、各指し手のQ値を出力しており
        # [torch.FloatTensor of size self.BATCH_SIZE x N]になっている
        # ここから実行したアクションa_tに対応するQ値を求めるため、action_batchで行った行動a_t
        # のindexを求め、それに対応するQ値をgatherで引っ張り出す
        state_action_values = self.model(state_batch).to(self.device)
        state_action_values = state_action_values.gather(1, action_batch).to(self.device)
        
        # 3.3 max{Q(s_t+1, a)}値を求める。ただし、次の状態があるかに注意。
        
        # flappybirdがdoneになっておらず、next_stateがあるかをチェックするインデックスマスクを作成
        non_final_mask = torch.ByteTensor(
            tuple(map(lambda s: s is not None, batch.next_state))).to(self.device)
        
        # まずは全部0にしておく
        next_state_values = torch.zeros(self.BATCH_SIZE)
        # 次の状態があるindexの最大Q値を求める
        # 出力にアクセスし、max(1)で列方向の最大値の[値、index]を求める
        # そしてそのQ値を取り出します
        self.target_net.eval()
        target = self.target_net(non_final_next_states).to(self.device)
        for num in range(0, self.BATCH_SIZE):
            a = non_final_mask[num].item()
            bol = a == 1
            if  a == 1:
                for next_actions in non_final_next_actions_list[num]:
                    temp = list()
                    for action in next_actions:
                        temp.append(target[0][action])
                next_state_values[num] = -max(temp)
                next_state_values = next_state_values.to(self.device)
        # 3.4 教師となるQ値を、Q学習の式から求める
        expected_state_action_values = (next_state_values * GAMMA) + reward_batch
        expected_state_action_values = expected_state_action_values.unsqueeze(1).to(self.device)
        # ------------------------------------------------------------
        # 4. 結合パラメータの更新　
        # ------------------------------------------------------------
        # 4.1 ネットワークを訓練モードに切り替える
        self.model.train()
        
        # 4.2 損失関数を計算する (smooth_l1_lossはHuberloss)
        # expected_state_action_valuesは
        # sizeが[minbatch]になっているから、unsqueezeで[minbatch x 1]へ
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values).to(self.device)
        # print(loss.item())
        # 4.3 結合パラメータを更新する
        self.model.grad = None # 勾配をリセット
        loss.backward() # バックプロパゲーションを計算
        self.optimizer.step() # 結合パラメータを更新
    
    def update_target_model(self):
        # モデルの重みをtarget_networkにコピー
        self.target_net.load_state_dict(self.model.state_dict())
    
    def decide_action(self, state, episode, legal_list, random_count, AI_count):
        '''現在の状態に応じて、行動を決定する'''
        EPS_START = 0.9
        EPS_END = 0.05
        sample = random.random()
        EPS_DECAY = 2000
        random_or_AI = ''
        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
            math.exp(-1. * episode / EPS_DECAY)

        epsilon = 0.41 * (1 / (episode * self.epsilonrate + 1))
        
        if sample > eps_threshold:
        # if epsilon <= np.random.uniform(0, 1):
            AI_count += 1
            random_or_AI = 'AI'
            self.model.eval()
            with torch.no_grad():
                action = self.model(state)
                if action.dim() == 2:
                    action = action.unsqueeze(0)

                action_list = []
                for num in legal_list:
                    action_list.append(action[0][0][num])
                action = action_list.index(max(action_list))
                action = legal_list[action]
                # action = action.view(1, 1)

            # ネットワークの出力の最大値のindexを取り出す = max(1)[1]
            # .view(1, 1)は[torch.LongTensor of size 1] を size 1x1 に変換する
        
        else:
            # 0, 1の行動をランダムに返す
            random_count += 1
            random_or_AI = 'random'
            key = random.choice(legal_list)
            action = key
            # actionは[torch.LongTensor of size 1x1]の形になる
        return action, random_count, AI_count, random_or_AI
    
    def brain_predict(self, state):
        self.model.eval() # ネットワークを推論モードに切り替える
        with torch.no_grad():
            action = self.model(state).max(1)[1].view(1, 1)
        return action