import numpy as np
import copy
from pieces.Queen_class import Queen
from pieces.Rook_class import Rook
from pieces.Pown_class import *
from pieces.King_class import *
from pieces.Bishop_class import *
from pieces.Knight_class import *


def change_board(sample):
    tmp_board = np.empty((1, 64) , dtype=int)
    tmp_sample = copy.copy(sample)
    tmp_sample = tmp_sample.flatten()
    for num in range(0, len(tmp_sample)):
        boad_inf = tmp_sample[num]
        if boad_inf == 0:
            tmp_board[0][num] = 0
        if type(boad_inf) == King:
            tmp_board[0][num] = 2 * boad_inf.player.player
        if type(boad_inf) == Pown:
            tmp_board[0][num] = 3 * boad_inf.player.player
        if type(boad_inf) == Queen:
            tmp_board[0][num] = 4 * boad_inf.player.player
        if type(boad_inf) == Rook:
            tmp_board[0][num] = 5 * boad_inf.player.player
        if type(boad_inf) == Knight:
            tmp_board[0][num] = 6 * boad_inf.player.player
        if type(boad_inf) == Bishop:
            tmp_board[0][num] = 7 * boad_inf.player.player
    return tmp_board

