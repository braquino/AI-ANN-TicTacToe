from Player import Player

class Player_human(Player):
    
    def __init__(self, player):
        Player.__init__(self, player, '')
        
    def play(self, board):
        print(board)
        while True:
            move = int(input('Enter the number from 0 to 8 for your play:\n0 1 2\n3 4 5\n6 7 8\n'))
            if move in [x[0] for x in enumerate(board.board) if x[1] == '-']:
                return move
            else:
                print('Wrong move, try again\n')