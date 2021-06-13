from .util import *

class player():
    def __init__(self, player, Agent):
        self.attack_list = []
        self.move_dic = {}
        self.player = player
        self.enemy = None
        self.agent = Agent
        if player == 1:
            self.flag = 'W'
            self.name = 'white'
        else:
            self.flag = 'B'
            self.name = 'black'
        self.temp_symbol = []
        self.temp_memory = []
    def __call__(self):
        self.attack_list = []
        self.move_dic = {}
        self.temp_symbol = []

    def add_move(self, piece, file, rank, cover_flag):
        add(self, piece, file, rank, cover_flag)

    def add_oo(self, player, king, rook):
        add_oo(player, king, rook)

    def add_ooo(self, player, king, rook):
        add_ooo(player, king, rook)
    def set_enemy(self, enemy):
        self.enemy = enemy
