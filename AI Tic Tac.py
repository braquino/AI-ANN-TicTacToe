# Essa aí test atodas as combinações de jogos de Tic Tac Toe e cria uma rede neural com os movimentos vencedores
# Formato do input da rede neural:,Game,1.X,1.O,2.X	2.O	3.X	3.O	4.X	4.O	5.X	5.O	6.X	6.O	7.X	7.O	8.X	8.O	9.X	9.O	1.Y	2.Y	3.Y	4.Y	5.Y	6.Y	7.Y	8.Y	9.Y	Ganhou,?

import numpy
import random
from functools import reduce
import heapq 
from collections import Counter, defaultdict

# ============================================================================================
# Tic Tac Toe Ramdom part

# checa vitória
def check_victory(l, game):
    #l é uma lista de 18 jogadas 0 e 1
    check = []
    if sum(l) == 9:
        return True
    for i in range(2):
        check += [l[0+i] == l[2+i] == l[4+i] == 1]
        check += [l[6+i] == l[8+i] == l[10+i] == 1]
        check += [l[12+i] == l[14+i] == l[16+i] == 1]
        check += [l[0+i] == l[6+i] == l[12+i] == 1]
        check += [l[2+i] == l[8+i] == l[14+i] == 1]
        check += [l[4+i] == l[10+i] == l[16+i] == 1]
        check += [l[0+i] == l[8+i] == l[16+i] == 1]
        check += [l[4+i] == l[8+i] == l[12+i] == 1]
        if any(check) and i == 0:
            game_win[game] = 'X'
            break
        elif any(check) and i == 1:
            game_win[game] = 'O'
            break
    return any(check)

def print_board(play_line):
    def XO(tuple_casa):
        if tuple_casa[0] == 1:
            return 'X'
        elif tuple_casa[1] == 1:
            return 'O'
        else:
            return '-'
    for i in range(3):
        print(XO((play_line[(i*6)+1],play_line[(i*6)+2])),XO((play_line[(i*6)+3],play_line[(i*6)+4])),XO((play_line[(i*6)+5],play_line[(i*6)+6])))
    print('\n')

n_games = 20

plays = [['Game','1.X','1.O','2.X','2.O','3.X','3.O','4.X','4.O','5.X','5.O','6.X','6.O','7.X','7.O','8.X','8.O','9.X','9.O','1.Y','2.Y','3.Y','4.Y','5.Y','6.Y','7.Y','8.Y','9.Y']]
game_win = defaultdict(lambda: '-')

for game in range(n_games):
    line = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    while not check_victory(line, game):  
        lineY = [0,0,0,0,0,0,0,0,0]
        X,Y = False, False
        #moveX = list(range(20)[0:18:2])
        unit_test = numpy.asarray([line])
        jogada = playerX.predict(unit_test)
        nlarg = heapq.nlargest(5, list(jogada[0]))
        moveX = [list(jogada[0]).index(nlarg[0])*2,list(jogada[0]).index(nlarg[1])*2,list(jogada[0]).index(nlarg[2])*2,list(jogada[0]).index(nlarg[3])*2]
#        if nlarg[0] > 0.5:
#            moveX = moveX[:2]
#        elif nlarg[0] > 0.2:
#            moveX = moveX[:3]
        xx = 0
        while X == False and 0 in line[::2]:
            xx += 1
            if xx > 200:
                raise Exception('infinite loop')
            try:
                p = moveX.pop(moveX.index(random.choice(moveX)))
            except:
                moveX = list(range(20)[0:18:2])
                p = moveX.pop(moveX.index(random.choice(moveX)))
            if line[p] == line[p + 1] == 0:
                lineY[int(p / 2)] = 1
                line[p] = 0 #workaround pra salvar o registro corretamente
                plays += [[game] + line + lineY + ['X']]
                line[p] = 1
                lineY = [0,0,0,0,0,0,0,0,0]
                X = True
                plays += [[game] + line + lineY]
        # moveO = list(range(20)[1:19:2])
        unit_test = numpy.asarray([line])
        jogada = playerO.predict(unit_test)
        nlarg = heapq.nlargest(5, list(jogada[0]))
        moveO = [list(jogada[0]).index(nlarg[0])*2+1,list(jogada[0]).index(nlarg[1])*2+1,list(jogada[0]).index(nlarg[2])*2+1,list(jogada[0]).index(nlarg[3])*2+1]
#        if nlarg[0] > 0.5:
#            moveO = moveO[:2]
#        elif nlarg[0] > 0.2:
#            moveO = moveO[:3]
        oo = 0
        while Y == False and 0 in line[1::2]:
            oo += 1
            if oo > 200:
                raise Exception('infinite loop')
            try:
                p = moveO.pop(moveO.index(random.choice(moveO)))
            except:
                 moveO = list(range(20)[1:19:2])
                 p = moveO.pop(moveO.index(random.choice(moveO)))
            if line[p] == line[p - 1] == 0:
                lineY[int(p/ 2)] = 1 
                line[p] = 0 #workaround pra salvar o registro corretamente
                plays += [[game] + line + lineY + ['O']]
                line[p] = 1
                lineY = [0,0,0,0,0,0,0,0,0]
                Y = True
                plays += [[game] + line + lineY]
                
#scoreX = len(list(filter(lambda x: x == 'X',game_win.values())))
#scoreO = len(list(filter(lambda x: x == 'O',game_win.values())))
#score_even = len(list(filter(lambda x: x == '-',game_win.values())))
store = Counter(game_win.values())

for g in plays:
    if g[0] != 'Game':
        print_board(g)
# =================================================================================================
# Data preparation part
plays = plays[1::2]
for i,v in enumerate(plays):
    plays[i] += [game_win[plays[i][0]]]
    
dataset = list(filter(lambda x: x[29] == x[28] =='X',plays))
dataset = numpy.asarray(dataset)[:,1:28]
dataset = dataset.astype(int)
X = dataset[:,:18]
y = dataset[:,18:]
from sklearn.model_selection import train_test_split
# O test size de 0.2 representa 20% da base
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

del plays

# ==================================================================================================
# Initiating Neural Network

from keras.models import Sequential
# will initialize the weights at number close to zero
from keras.layers import Dense

# Initialising the ANN
playerX = Sequential()

# Adding the input layer and the first hidden layer
playerX.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu', input_dim = 18))
# Adding the second hidden layer
playerX.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu'))
# Adding the second hidden layer
playerX.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu'))
# Adding the output layer
playerX.add(Dense(units = 9, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
playerX.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
playerX.fit(X_train, y_train, batch_size = 100, epochs = 10)

# Save and Load the weights
playerX.save_weights('randomX.HDF5')
playerX.load_weights('randomX.HDF5')


unit_test = numpy.asarray([[0,0,0,0,0,0,
                            0,0,0,0,0,0,
                            0,0,0,0,0,0]])
playerX.predict(unit_test)

# =================================================================================================
# Data preparation part
plays = plays[1::2]
for i,v in enumerate(plays):
    plays[i] += [game_win[plays[i][0]]]
    
dataset = list(filter(lambda x: x[29] == x[28] =='O',plays))
dataset = numpy.asarray(dataset)[:,1:28]
dataset = dataset.astype(int)
X = dataset[:,:18]
y = dataset[:,18:]
from sklearn.model_selection import train_test_split
# O test size de 0.2 representa 20% da base
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, test_size = 0.2, random_state = 0)

del plays

# ==================================================================================================
# Initiating Neural Network

from keras.models import Sequential
# will initialize the weights at number close to zero
from keras.layers import Dense

# Initialising the ANN
playerO = Sequential()

# Adding the input layer and the first hidden layer
playerO.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu', input_dim = 18))
# Adding the second hidden layer
playerO.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu'))
# Adding the second hidden layer
playerO.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu'))
# Adding the output layer
playerO.add(Dense(units = 9, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
playerO.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
playerO.fit(X_train2, y_train2, batch_size = 100, epochs = 100)

# Save and Load the weights
playerO.save_weights('randomO.HDF5')
playerO.load_weights('randomO.HDF5')