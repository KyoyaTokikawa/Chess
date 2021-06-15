from numpy import true_divide
from torch._C import Value
from .Board import *
from .Player_class import *
import random
import copy
from AI.deep_Agent import *
from AI.deep_q import *
import time
l = [] 
king = 100
queen = 200
bishop = 300
knight = 400
rook = 500
pown = 600

a, b, c, d, e, f, g, h = 1, 2, 3, 4, 5, 6, 7, 8

class master():
    def __init__(self, white_agent, black_agent, gamerecord_dic, device):
        self.gamerecord_dic = gamerecord_dic
        self.white = player(1, white_agent)
        self.black = player(-1, black_agent)
        self.white.set_enemy(self.black)
        self.black.set_enemy(self.white)
        self.Board = board(self.white, self.black)
        # self.Board.print_board()
        self.turn = self.white
        self.piece_amount = 32
        self.count_fifty = 0
        self.game_record = []
        self.count = 0
        self.device = device

    def __call__(self, gameNo):
        list_check = False
        if list_check:
            for key in l:
                if self.turn == self.white:
                    self.count += 1
                    self.game_record.append(self.count)
                    print(self.count)
                    player = self.white
                    piece_amount, draw = self.Board(self.turn)
                    self.turn = self.black
                    if piece_amount == self.piece_amount:
                        self.count_fifty += 1
                    else:
                        self.piece_amount = piece_amount
                else:
                    player = self.black
                    temp_piece_amount,draw = self.Board(self.turn)
                    self.turn = self.white
                if draw == False:
                    game_continue = self.check_king(player)
                else:
                    game_continue = False
                if game_continue:
                    # key = choose_random(player)
                    piece_info = player.move_dic[key]
                    piece, move = piece_info
                    if key == 'O-O':
                        self.Board.castling_oo(piece, move)
                    elif key == 'O-O-O':
                        self.Board.castling_ooo(piece, move)
                    elif '=' in key:
                        self.count_fifty = self.Board.promotion(piece, move, self.count_fifty)
                    else:
                        self.count_fifty = self.Board.move(piece, move, self.count_fifty)
                    self.game_record.append(key)
                    self.Board.print_board()
                    if self.count_fifty == 50:
                        print('DRAW')
                        break
                else:
                    if self.turn == self.white:
                        king = self.Board.white_king
                    else:
                        king = self.Board.black_king
                    king_position = (king.file, king.rank)
                    if king_position in player.enemy.attack_list:
                        print(self.turn.name, end='')
                        print('LOSE')
                        break
                    else:
                        print('stalemate')
                    break
            print(self.game_record)
        else:
            board_status = change_board(self.Board.board)
            state = board_status
            state = torch.from_numpy(state).type(torch.FloatTensor)
            state = torch.unsqueeze(state, 0).to(self.device)
            start = time.time()
            while True:
                # self.Board.print_board()
                if self.turn == self.white:
                    self.count += 1
                    self.game_record.append(self.count)
                    # print(self.count)
                    player = self.white
                    enemy = self.black
                    piece_amount = self.Board(self.turn)
                    next = self.black
                    if piece_amount == self.piece_amount:
                        self.count_fifty += 1
                    else:
                        self.piece_amount = piece_amount
                else:
                    player = self.black
                    enemy = self.white
                    self.Board(self.turn)
                    next = self.white

                game_continue = self.check_king(player)
                if game_continue:

                    # key = choose_random(player)
                    legal_list = []
                    for key, val in self.gamerecord_dic.items():
                        if val in player.move_dic:
                            legal_list.append(key)
                    if self.turn == self.white:
                        key = player.agent.get_action(state, gameNo, legal_list)
                        next_legal = legal_list
                        rec = self.gamerecord_dic[key]
                    else:
                        key = choose_random(legal_list)
                        next_legal = legal_list
                        rec = self.gamerecord_dic[key]
                    piece_info = player.move_dic[rec]
                    piece, move, gamerecord = piece_info
                    if gamerecord == 'O-O':
                        self.Board.castling_oo(piece, move)
                    elif gamerecord == 'O-O-O':
                        self.Board.castling_ooo(piece, move)
                    elif '=' in gamerecord:
                        self.count_fifty = self.Board.promotion(piece, move, self.count_fifty)
                    else:
                        self.count_fifty = self.Board.move(piece, move, self.count_fifty)
                    self.game_record.append(gamerecord)
                    # self.Board.print_board()
                    next_status = change_board(self.Board.board)
                    state_next = next_status
                    state_next = torch.from_numpy(state_next).type(torch.FloatTensor)
                    state = state_next.to(self.device)
                    temp_next_legal = []
                    player.temp_memory.append([state, key, state_next, temp_next_legal, self.count * player.agent.reward_rate])
                    if self.turn == self.white:
                        if len(enemy.temp_memory) > 0:
                            enemy.temp_memory[len(enemy.temp_memory) - 1][3] = list(next_legal)
                    else:
                        enemy.temp_memory[len(enemy.temp_memory) - 1][3] = list(next_legal)
                    if self.count_fifty == 50:
                        player.temp_memory[self.count - 1][2] = None
                        end = time.time()
                        # print('DRAW',end=' ')
                        print(str(self.count) + ':'+ str(end - start))
                        much = 0
                        break

                    self.turn = next
                else:
                    if self.turn == self.white:
                        king = self.Board.white_king
                        enemy.temp_memory[len(enemy.temp_memory) - 1][2] = None
                        # player.temp_memory[len(player.temp_memory) - 1][2] = None
                        winner = self.black
                        much = -1
                    else:
                        king = self.Board.black_king
                        enemy.temp_memory[len(enemy.temp_memory) - 1][2] = None
                        # player.temp_memory[len(player.temp_memory) - 1][2] = None
                        winner = self.white
                        much = 1
                    king_position = (king.file, king.rank)
                    if king_position in player.enemy.attack_list:
                        end = time.time()
                        # print(winner.name, end=' ')
                        # print('WIN',end=' ')
                        print(str(self.count) + ':'+ str(end - start))
                        break
                    else:
                        enemy.temp_memory[len(enemy.temp_memory) - 1][2] = None
                        much = 0
                        end = time.time()
                        # print('stalemate', end=' ')
                        print(str(self.count) + ':'+ str(end - start))
                    break
            # print(self.game_record)
            return much, self.white.temp_memory, self.black.temp_memory

    def check_king(self, player):

        move_record = list(player.move_dic.keys())
        temp_move_dic = copy.copy(player.move_dic)
        for key in move_record:
            check_board = copy.copy(self.Board)
            check_board.board = copy.copy(self.Board.board)
            check_board.piece_copy()
            check_board(self.turn)
            
            piece_info = temp_move_dic[key]
            piece = copy.copy(piece_info[0])
            move  = copy.copy(piece_info[1])
            check_board(self.turn)
            gamerecord = piece_info[2]
            if gamerecord == 'O-O':
                check_board.castling_oo(piece, move)
            elif gamerecord == 'O-O-O':
                check_board.castling_ooo(piece, move)
            elif '=' in gamerecord:
                check_board.promotion(piece, move)
            else:
                check_board.move(piece, move)
            # check_board.print_board()
            check_board.scan_board(self.turn.enemy)

            if player == self.white:
                king = check_board.white_king
                enemy = self.black
            else:
                king = check_board.black_king
                enemy = self.white

            king_position = (king.file, king.rank)
            if king_position in enemy.attack_list:
                temp_move_dic.pop(key)

        player.move_dic = temp_move_dic

        if len(player.move_dic) == 0:
            return False
        else:
            return True


def choose_random(legal_list):
    key = random.choice(legal_list)
    return key

