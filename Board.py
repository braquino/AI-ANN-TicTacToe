
class Board(object):
    
    def __init__(self):
        self.board = ['-','-','-','-','-','-','-','-','-']
    
    def __str__(self):
        result = ''
        for line in range(3):
            result += self.board[line * 3 + 0]+self.board[line * 3 + 1]+self.board[line * 3 + 2]+'\n'
        return result
    
    def move(self, player, field):
        if self.board[field] == '-':
            self.board[field] = player.player
            return True
        else:
            return False
    
    def clear(self):
        self.board = ['-','-','-','-','-','-','-','-','-']
    
    def check_win(self): 
        b = self.board
        for p in ('X','O'):
            check =[]
            for i in range(3):
                x = i * 3
                check += [b[0 + x] == b[1 + x] == b[2 + x] == p]
                check += [b[0 + i] == b[3 + i] == b[6 + i] == p]
            check += [b[0] == b[4] == b[8] == p]
            check += [b[2] == b[4] == b[6] == p]
            if any(check):
                return p
        if '-' not in b:
            return 'draw'
        return '-'
    
