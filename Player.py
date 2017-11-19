import numpy
import random
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import operator
from Util import convert_board

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
#        for i,v in enumerate(plays_data):
#            plays_data[i] += [self.game_win[plays_data[i][0]]]
        dataset = list(filter(lambda x: x[28] == self.player, plays_data))
        dataset = numpy.asarray(dataset)[:,1:28]
        dataset = dataset.astype(int)
        X = dataset[:,:18]
        y = dataset[:,18:]
        # split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        # do the work
        self.ann.fit(X_train, y_train, batch_size = batch, epochs = epochs)
    
    def play(self, board):
        # Run the ANN
        result = self.ann.predict(numpy.asarray([convert_board(board.board)]))
        # Convert the result to dictionary
        result = dict(enumerate(result.flatten(),0))
        # Extract all the completed fields from the dictionay
        for i in range(9):
            if board.board[i] != '-':
                result.pop(i)
        # Convert the result to the accumulated sum in the largerst order
        result = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
        for i in range(1,len(result)):
            result[i] = list(result[i])
            result[i][1] += result[i-1][1]
        rand = random.uniform(0,result[-1][1])
        move_list = [n for n,v in result if v > rand]    
        return move_list[0]
        
    def save(self):
        self.ann.save_weights(self.path)
        
    def load(self):
        self.ann.load_weights(self.path)