import copy
import numpy as np

from pieces.Rook_class import *
from pieces.Queen_class import *
from pieces.Bishop_class import *
from pieces.Pown_class import *
from pieces.Knight_class import *
from pieces.King_class import *

from pieces.Piece_class import *

a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7
class board():
    def __init__(self, white, black) -> None:
        self.board = np.zeros((8, 8) , dtype=Piece)
        self.white = white
        self.black = black
        self.white_king = None
        self.black_king = None
        for file_num in range(0, 8):
            for rank_num in range(0, 8):
                position = [file_num, rank_num]
                if rank_num == 0 or rank_num == 7:
                    if file_num == a or file_num == h:
                        self.Create_Piece(position, 'ROOK')
                    elif file_num == b or file_num == g:
                        self.Create_Piece(position, 'KNIGHT')
                    elif file_num == c or file_num == f:
                        self.Create_Piece(position, 'BISHOP')
                    elif file_num == d:
                        self.Create_Piece(position, 'QUEEN')
                    elif file_num == e:
                        self.Create_Piece(position, 'KING')
                if rank_num == 1 or rank_num == 6:
                    self.Create_Piece(position, 'POWN')

    def __call__(self, turn):
        piece_amount = self.scan_board(turn)
        return piece_amount

    def scan_board(self, turn):
        self.white()
        self.black()

        white_piece = []
        black_piece = []
        piece_all = self.board[self.board != 0]
        for piece in piece_all:
            if piece.player == self.white:
                white_piece.append(piece)
            else:
                black_piece.append(piece)

        if turn == self.white:
            self.scan_piece(black_piece, turn)
            self.scan_piece(white_piece, turn)
        else:
            self.scan_piece(white_piece, turn)
            self.scan_piece(black_piece, turn)

        return len(piece_all)
    def scan_piece(self, piece_list, turn):
        for piece in piece_list:
            if type(piece) == King:
                if piece.player == self.white:
                    self.white_king = piece
                else:
                    self.black_king = piece
            if type(piece) == Pown:
                if turn == piece.player:
                    piece.can_Enpassant = False
            piece(self.board)

    def move(self, piece, move, count_fifty = None):
        file = piece.file
        rank = piece.rank
        self.board[move] = piece
        piece.file = move[0]
        piece.rank = move[1]
        piece.move_count += 1
        self.board[file][rank] = 0
        if type(piece) == Pown:
            if count_fifty != None:
                count_fifty = 0
            if abs(rank - piece.rank) == 2:
                piece.can_Enpassant = True
        return count_fifty

    def promotion(self, piece, change_piece, count_fifty = None):
        file = piece.file
        rank = piece.rank
        position = (change_piece.file, change_piece.rank)
        self.board[position] = change_piece
        self.board[file][rank] = 0
        if count_fifty != None:
            count_fifty = 0
        return count_fifty

    def castling_oo(self, piece, rook):
        king_file = piece.file
        king_rank = piece.rank
        piece.file = g
        self.board[g][king_rank] = piece
        self.board[king_file][king_rank] = 0
        
        rook_file = rook.file
        rook_rank = rook.rank
        rook.file = f
        self.board[f][rook_rank] = rook
        self.board[rook_file][rook_rank] = 0

    def castling_ooo(self, piece, rook):
        king_file = piece.file
        king_rank = piece.rank
        piece.file = c
        self.board[c][king_rank] = piece
        self.board[king_file][king_rank] = 0
        
        rook_file = rook.file
        rook_rank = rook.rank
        rook.file = d
        self.board[d][rook_rank] = rook
        self.board[rook_file][rook_rank] = 0


    def Create_Piece(self, position, name):
        # 1 of index is rank_num
        if position[1] == 0 or position[1] == 1:
            player = self.white
        elif position[1] == 6 or position[1] == 7:
            player = self.black

        if name == 'KING':
            piece = King(player, position)
        elif name == 'QUEEN':
            piece = Queen(player, position)
        elif name == 'ROOK':
            piece = Rook(player, position)
        elif name == 'BISHOP':
            piece = Bishop(player, position)
        elif name == 'KNIGHT':
            piece = Knight(player, position)
        elif name == 'POWN':
            piece = Pown(player, position)
        self.board[position[0], position[1]] = piece

    def piece_copy(self):
        pieces = self.board[self.board != 0]
        for piece in pieces:
            file = piece.file
            rank = piece.rank
            self.board[file][rank] = copy.copy(piece)
    def print_board(self):
        for rank_num in range(7, -1, -1):
            print(str(rank_num + 1) + ' ', end='')
            for file_num in range(0, 8):
                if self.board[file_num][rank_num] == 0:
                    print("{:^9d}".format(self.board[file_num][rank_num]), end='')
                else:
                    print("{:^9s}".format(self.board[file_num][rank_num].name + '_' + str(self.board[file_num][rank_num].player.flag)), end='')
            print('\n')
        print("  {0:^9s}{1:^9s}{2:^9s}{3:^9s}{4:^9s}{5:^9s}{6:^9s}{7:^9s}".format('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'))
        print('-----------------------------------------------------------------------')


