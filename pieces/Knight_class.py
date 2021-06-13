import numpy as np
from src.piece_move import knight_move
from pieces.Piece_class import Piece

class Knight(Piece):
    def __init__(self, player, position, name = 'KNIGHT'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'N'

    def __call__(self, board):
        knight_move(board, self)