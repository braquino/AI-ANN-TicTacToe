# Essa aí test atodas as combinações de jogos de Tic Tac Toe e cria uma rede neural com os movimentos vencedores
# Formato do input da rede neural:,Game,1.X,1.O,2.X	2.O	3.X	3.O	4.X	4.O	5.X	5.O	6.X	6.O	7.X	7.O	8.X	8.O	9.X	9.O	1.Y	2.Y	3.Y	4.Y	5.Y	6.Y	7.Y	8.Y	9.Y	Ganhou,?

import numpy
import random
from functools import reduce
from heapq import nlargest
from collections import Counter, defaultdict
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import operator
import pdb

# ============================================================================================
# Tic Tac Toe Ramdom part

def convert_board(board): # prepare the board in a formate that the ANN understand
    prep_board = []
    for f in board:
            for p in 'X','O':
                if f == p:
                    prep_board += [1]
                else:
                    prep_board += [0]
    return prep_board

class Player(object):
    
    def __init__(self, player, path):
        self.player = player
        self.path = path
        self.ann = Sequential()
        self.create_ann()
        
    def create_ann(self, nodes=50, layers=3):    
        self.ann.add(Dense(units = nodes, kernel_initializer = 'uniform', activation = 'relu', input_dim = 18))
        for i in range(layers-1):
            self.ann.add(Dense(units = nodes, kernel_initializer = 'uniform', activation = 'relu'))
        self.ann.add(Dense(units = 9, kernel_initializer = 'uniform', activation = 'sigmoid'))
        self.ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    def train_ann(self, plays_data, batch=100, epochs=100):
        # prepare data from an 2d list with 30 cols
        plays_data = plays_data[1::2]
        for i,v in enumerate(plays_data):
            plays_data[i] += [self.game_win[plays_data[i][0]]]
        dataset = list(filter(lambda x: x[29] == x[28] =='X',plays_data))
        dataset = numpy.asarray(dataset)[:,1:28]
        dataset = dataset.astype(int)
        X = dataset[:,:18]
        y = dataset[:,18:]
        # split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        # do the work
        self.ann.fit(X_train, y_train, batch_size = 100, epochs = 100)
    
    def play(self, board):
        # Run the ANN
        result = self.ann.predict(numpy.asarray([convert_board(board)]))
        # Convert the result to dictionary
        result = dict(enumerate(result.flatten(),0))
        # Extract all the completed fields from the dictionay
        for i in range(9):
            if board[i] != '-':
                result.pop(i)
        # Convert the result to the accumulated sum in the largerst order
        result = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
        for i in range(1,len(result)):
            result[i] = list(result[i])
            result[i][1] += result[i-1][1]
        rand = random.uniform(0,result[-1][1])
        for n,v in result:
            if v > rand:
                move = n
        return move
        
    def save(self):
        self.ann.save_weights(self.path)
        
    def load(self):
        self.ann.load_weights(self.path)
        
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
                    play = player.play(board.board)
                    dummy_board = [0,0,0,0,0,0,0,0,0]
                    dummy_board[play] = 1
                    self.plays += [[game] + convert_board(board.board) + dummy_board + [player.player]]
                    board.move(player, play)
                else:
                    break
        print(board)
        print(board.check_win())

g = Game()
b = Board()
pX = Player('X', 'px.h5')
pO = Player('O', 'po.h5')
g.auto_game(b, pX, pO)
plays = g.plays
#b.move(pX,3)
#g.pX.play(g.board.board)
#print(b)
