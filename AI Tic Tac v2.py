# Essa aí test atodas as combinações de jogos de Tic Tac Toe e cria uma rede neural com os movimentos vencedores
# Formato do input da rede neural:,Game,1.X,1.O,2.X	2.O	3.X	3.O	4.X	4.O	5.X	5.O	6.X	6.O	7.X	7.O	8.X	8.O	9.X	9.O	1.Y	2.Y	3.Y	4.Y	5.Y	6.Y	7.Y	8.Y	9.Y	Ganhou,?

from Player import Player
from Game import Game
from Board import Board
from Player_rec import Player_rec

# ============================================================================================

g = Game()
b = Board()
pX = Player('X', 'px.h5')
pO = Player('O', 'po.h5')
pR = Player_rec('O','px.h5')
g.auto_game(b, pX, pR)
plays = g.plays


