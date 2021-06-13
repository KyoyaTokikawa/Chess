from .Piece_class import *
from src.piece_move import *

class Pown(Piece):
    def __init__(self, player, position, name = 'POWN'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'P'
        self.can_Enpassant = False

    def __call__(self, board):
        pown_move(board, self)





