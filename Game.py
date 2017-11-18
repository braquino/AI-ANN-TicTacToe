from Util import convert_board

class Game(object):
    
    def __init__(self):
        self.plays = [['Game','1.X','1.O','2.X','2.O','3.X','3.O','4.X','4.O','5.X','5.O','6.X','6.O','7.X','7.O','8.X','8.O','9.X','9.O','1.Y','2.Y','3.Y','4.Y','5.Y','6.Y','7.Y','8.Y','9.Y']]
    
    def auto_game(self, board, player1, player2):  
        game = 1
        while True:
            if board.check_win() != '-':
                break
            for player in [player1, player2]:
                if board.check_win() == '-':
                    play = player.play(board)
                    dummy_board = [0,0,0,0,0,0,0,0,0]
                    dummy_board[play] = 1
                    self.plays += [[game] + convert_board(board.board) + dummy_board + [player.player]]
                    board.move(player, play)
                else:
                    break
        print(board)
        print(board.check_win())