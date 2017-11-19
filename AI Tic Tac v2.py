# Essa aí test atodas as combinações de jogos de Tic Tac Toe e cria uma rede neural com os movimentos vencedores
# Formato do input da rede neural:,Game,1.X,1.O,2.X	2.O	3.X	3.O	4.X	4.O	5.X	5.O	6.X	6.O	7.X	7.O	8.X	8.O	9.X	9.O	1.Y	2.Y	3.Y	4.Y	5.Y	6.Y	7.Y	8.Y	9.Y	Ganhou,?

from Player import Player
from Game import Game
from Board import Board
from Player_rec import Player_rec
from Player_human import Player_human
import csv


# ============================================================================================

g = Game()
b = Board()
pX = Player('X', 'px.h5')
pO = Player('O', 'po.h5')
pHX = Player_human('X')
pHO = Player_human('O')
pR = Player_rec('O','px.h5')
for i in range(5):
    g.auto_game(b, pHX, pO, i)
#
## Save file
with open('games.csv', 'a', newline='') as file:
    wr = csv.writer(file)
    wr.writerows(g.plays[1:])
#
## load file
plays = []    
with open('games.csv', 'r') as read:
    reader = csv.reader(read, delimiter=',')
    for row in reader:
        plays.append(row)    

pO.train_ann(plays, 100, 100)
pX.train_ann(plays, 100, 100)