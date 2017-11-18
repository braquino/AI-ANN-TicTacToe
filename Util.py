
def convert_board(board): # prepare the board in a formate that the ANN understand
    prep_board = []
    for f in board:
            for p in 'X','O':
                if f == p:
                    prep_board += [1]
                else:
                    prep_board += [0]
    return prep_board