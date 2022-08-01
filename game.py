from .models import BoardSquare
from colorama import Style


BOARD_WHITE = BoardSquare(BOARD_ICON['white']) 
BOARD_BLACK = BoardSquare(BOARD_ICON['black'])


POSITIONS = list('12345678')

#white figurs
white = [Boat(ICONS['boat_white']), Horse(ICONS['horse_white']), Elephant(ICONS['elephant_white']), Queen(ICONS['queen_white']), King(ICONS['king_white']), Elephant(ICONS['elephant_white']), Horse(ICONS['horse_white']), Boat(ICONS['boat_white'])]

#black figurs
black = [Boat(ICONS['boat_black']), Horse(ICONS['horse_black']),Elephant(ICONS['elephant_black']), King(ICONS['king_black']), Queen(ICONS['queen_black']), Elephant(ICONS['elephant_black']), Horse(ICONS['horse_black']), Boat(ICONS['boat_black'])]


for i in range(8):
    for j in range(8):
        board[i + 1][j + 1].y = i + 1
        board[i + 1][j + 1].x = j + 1

for i in range(8):
    soldier_white = Solider(ICONS['soldier_white'], 0, 0)
    soldier_black = Solider(ICONS['soldier_black'], 0, 0)

    board[2][i + 1].setFigure(soldier_white)
    white[i].x = 1
    white[i].y = i
    board[1][i + 1].setFigure(white[i])
    board[7][i + 1].setFigure(soldier_black)
    black[i].x = 8
    black[i].y = i
    board[8][i + 1].setFigure(black[i])


board[2][4].move(3, 4)
board[7][4].move(6, 4)
board[8][3].move(5, 6)
board[5][6].move(3, 4)
board[3][4].move(2, 5)
board[1][6].move(2, 5)
board[2][5].move(3, 6)
board[3][6].move(6, 3)
board[7][2].move(6, 3)


for el in board:
    for i in el:
        if i in POSITIONS:
            (print(f'{BOARD_BLACK}{i}', end=''))
            continue
        print(i.__str__(), end=' ')
    print(Style.RESET_ALL)
