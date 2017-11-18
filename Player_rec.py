from Player import Player
from Board import Board



class Player_rec(Player):
    
    def __init__(self, player, path):
        Player.__init__(self, player, path)

    def search(self, board, player, move=0):
        new_board = Board()
        new_board.board = board.board.copy()
        new_player = [x for x in ['X','O'] if x != player][0]
        if new_board.check_win() == new_player:
            return move
        if move is False or '-' not in new_board.board or new_board.check_win() == player:
            return False      
        for pos in [x[0] for x in enumerate(new_board.board) if x[1] == '-']:
            new_board.board = board.board.copy()
            new_board.board[pos] = player
            attempt = self.search(new_board, new_player, pos)
            if attempt:
                return attempt
            
    def play(self, board):
        move = self.search(board, self.player)
        if move is False:
            return Player.play(board)
        else:
            return move
