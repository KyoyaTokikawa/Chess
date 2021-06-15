import random
from copy import deepcopy
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

class Net(nn.Module):
    
    def __init__(self, num_states, num_actions):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(num_states, 256)
        self.fc2 = nn.Linear(256, 256) #中間層
        self.fc3 = nn.Linear(256, 256) #中間層
        self.fc4 = nn.Linear(256, 256) #中間層
        self.fc5 = nn.Linear(256, 256) #中間層
        self.fc6 = nn.Linear(256, 256) #中間層
        self.fc7 = nn.Linear(256, 256) #中間層
        self.fc8 = nn.Linear(256, 256) #中間層
        self.fc9 = nn.Linear(256, 256) #中間層
        self.fc10 = nn.Linear(256, num_actions)
    
    def forward(self, x):
        if False:
            h1 = F.leaky_relu(self.fc1(x)) # 活性化関数にはReLu
            h2 = F.leaky_relu(self.fc2(h1))
            h3 = F.leaky_relu(self.fc3(h2))
            h4 = F.leaky_relu(self.fc4(h3))
            h5 = F.leaky_relu(self.fc5(h4))
        else:
            h1 = F.relu(self.fc1(x)) # 活性化関数にはReLu
            h2 = F.relu(self.fc2(h1))
            h3 = F.relu(self.fc3(h2))
            h4 = F.relu(self.fc4(h3))
            h5 = F.relu(self.fc5(h4))
            h6 = F.relu(self.fc5(h5))
            h7 = F.relu(self.fc5(h6))
            h8 = F.relu(self.fc5(h7))
            h9 = F.relu(self.fc5(h8))
            h10 = F.relu(self.fc5(h9))
        output = self.fc10(h10)
        return output