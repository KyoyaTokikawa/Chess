from hashlib import new
from pieces.King_class import *
from pieces.Queen_class import *
from pieces.Rook_class import *
from pieces.Bishop_class import *
from pieces.Knight_class import *
from pieces.Pown_class import *

a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7 
def add(player, add_piece, add_file, add_rank, cover):
    file = add_file
    rank = add_rank
    piece = add_piece
    flag = add_piece.piece_flag
    attack_position = (file, rank)
    if flag != 'P':
        symbol = flag
        player.attack_list.append(attack_position)
    else:
        if piece.file != file:
            player.attack_list.append(attack_position)
        symbol = ''
    
    file_num = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    if cover != 'C':
        if file == a:
            gamerecord = symbol + 'a' + str(rank + 1)
        if file == b:
            gamerecord = symbol + 'b' + str(rank + 1)
        if file == c:
            gamerecord = symbol + 'c' + str(rank + 1)
        if file == d:
            gamerecord = symbol + 'd' + str(rank+ 1)
        if file == e:
            gamerecord = symbol + 'e' + str(rank+ 1)
        if file == f:
            gamerecord = symbol + 'f' + str(rank+ 1)
        if file == g:
            gamerecord = symbol + 'g' + str(rank+ 1)
        if file == h:
            gamerecord = symbol + 'h' + str(rank+ 1)
        bol = False
        if gamerecord in player.temp_symbol:
            bol = True
        else:
            player.temp_symbol.append(gamerecord)
        value = player.move_dic.pop((gamerecord), False)
        if value != False:
            if value[0].file == piece.file:
                gamerecord_value = gamerecord[0:1] + str(value[0].rank + 1) + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_value)] = value
                gamerecord_add = gamerecord[0:1] + str(piece.rank + 1) + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_add)] = [piece, attack_position, gamerecord_add]
            elif value[0].rank == piece.rank:
                value_file = file_num[value[0].file]
                gamerecord_value = gamerecord[0:1] + value_file + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_value)] = value
                piece_value = file_num[piece.file]
                gamerecord_add = gamerecord[0:1] + piece_value + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_add)] = [piece, attack_position, gamerecord_add]
            else:
                value_file = file_num[value[0].file]
                gamerecord_value = gamerecord[0:1] + value_file + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_value)] = value
                piece_value = file_num[piece.file]
                gamerecord_add = gamerecord[0:1] + piece_value + gamerecord[1:len(gamerecord) + 1]
                player.move_dic[(gamerecord_add)] = [piece, attack_position, gamerecord_add]
        elif bol == True:
                gamerecord_piece = gamerecord[0:1] + str(piece.rank + 1) + gamerecord[1:len(gamerecord) + 1]
                value = player.move_dic.pop((gamerecord_piece), False)
                if value != False:
                    value_file = file_num[value[0].file]
                    gamerecord_value = gamerecord[0:1] + value_file + str(value[0].rank + 1) + gamerecord[1:len(gamerecord) + 1]
                    player.move_dic[(gamerecord_value)] = value
                    piece_file = file_num[piece.file]
                    gamerecord_piece = gamerecord[0:1] + piece_file + gamerecord[1:len(gamerecord) + 1]
                    value = player.move_dic.pop((gamerecord_piece), False)
                    if value != False:
                        value_file = file_num[value[0].file]
                        gamerecord_value = gamerecord[0:1] + value_file + str(value[0].rank + 1) + gamerecord[1:len(gamerecord) + 1]
                        player.move_dic[(gamerecord_value)] = value
                        piece_value = file_num[piece.file]
                        gamerecord_piece = gamerecord[0:1] + piece_value + str(piece.rank + 1) + gamerecord[1:len(gamerecord) + 1]
                        player.move_dic[(gamerecord_piece)] = [piece, attack_position, gamerecord_piece]
                    else:
                        player.move_dic[(gamerecord_piece)] = [piece, attack_position, gamerecord_piece]
                else:
                    piece_file = file_num[piece.file]
                    gamerecord_piece = gamerecord[0:1] + piece_file + gamerecord[2:len(gamerecord) + 1]
                    player.move_dic[(gamerecord_piece)] = [piece, attack_position, gamerecord_piece]
        else:
            if cover == 'P':
                gamerecord_Q = gamerecord + '=Q'
                gamerecord_B = gamerecord + '=B'
                gamerecord_N = gamerecord + '=N'
                gamerecord_R = gamerecord + '=R'
                player.move_dic[(gamerecord_Q)] = [piece, Queen(player,  attack_position), gamerecord_Q] 
                player.move_dic[(gamerecord_B)] = [piece, Bishop(player, attack_position), gamerecord_B] 
                player.move_dic[(gamerecord_N)] = [piece, Knight(player, attack_position), gamerecord_N] 
                player.move_dic[(gamerecord_R)] = [piece, Rook(player,   attack_position), gamerecord_R] 
            else:
                player.move_dic[(gamerecord)] = [piece, attack_position, gamerecord]

def add_oo(player, king, rook):
    gamerecord = 'O-O'
    player.move_dic[(gamerecord)] = [king, rook, gamerecord]

def add_ooo(player, king, rook):
    gamerecord = 'O-O-O'
    player.move_dic[(gamerecord)] = [king, rook, gamerecord]


def append_list(gamerecord_dic, record):
    if record in gamerecord_dic.keys():
        pass
    else:
        count = list(gamerecord_dic.keys())
        if len(count) == 0:
            count = 1
        else:
            count = max(count) + 1
        gamerecord_dic[count] = record
    return gamerecord_dic

def gamerecord():
    piece_list = ['K', 'Q', 'R', 'B', 'N']
    file_list = ['a', 'b','c','d','e','f','g','h',]
    promotion_list = ['=Q', '=B', '=N', '=R']
    count = 0
    gamerecord_dic = {}
    gamerecord_dic = append_list(gamerecord_dic, 'O-O')
    gamerecord_dic = append_list(gamerecord_dic, 'O-O-O')
    for file_num in range(0, 8):
        for rank_num in range(1, 9):
            if file_num == 0:
                file = 'a'
            if file_num == 1:
                file = 'b'
            if file_num == 2:
                file = 'c'
            if file_num == 3:
                file = 'd'
            if file_num == 4:
                file = 'e'
            if file_num == 5:
                file = 'f'
            if file_num == 6:
                file = 'g'
            if file_num == 7:
                file = 'h'

            record = file + str(rank_num)
            # append_list(gamerecord_dic, record)
            for file_ in file_list:
                if file_ != file:
                    if file == 'a':
                        if file_ in ['b']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'b':
                        if file_ in ['a', 'c']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'c':
                        if file_ in ['b', 'd']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'b':
                        if file_ in ['c', 'e']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'e':
                        if file_ in ['d', 'f']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'f':
                        if file_ in ['e', 'g']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'g':
                        if file_ in ['f', 'h']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    elif file == 'h':
                        if file_ in ['g']:
                            record_ = file_ + record
                        else:
                            record_ = record
                    else:
                        record_ = record
                else:
                    record_ = record
                gamerecord_dic = append_list(gamerecord_dic, record_)
                if rank_num == 8 or rank_num == 1:
                    for promotion in promotion_list:
                        promotion_record_ = record_ + promotion
                        gamerecord_dic = append_list(gamerecord_dic, promotion_record_)
            for rec in piece_list:
                piece_record = rec + record
                gamerecord_dic = append_list(gamerecord_dic, piece_record)
                if rec != 'K':
                    for file_ in file_list:
                        bol_piece = rec in ['B', 'N']
                        bol_file  = file == file_
                        if (bol_file and bol_piece) != True:
                            record_ = rec + file_ + record
                            gamerecord_dic = append_list(gamerecord_dic, record_)
                            for rank_ in range(1, 9):
                                rank_ = str(rank_)
                                bol_piece = rec in ['R', 'B']
                                if bol_piece != True:
                                    bol_knight = rec == "N"
                                    bol_rank   = rank_ == str(rank_num)
                                    if (bol_knight and bol_rank) != True:
                                        record_ = rec + rank_ + record
                                        gamerecord_dic = append_list(gamerecord_dic, record_)
                                if rec == 'Q':
                                    record_ = rec + file_ + rank_ + record
                                    gamerecord_dic = append_list(gamerecord_dic, record_)

    return gamerecord_dic



