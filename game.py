from models import *
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


def detect_y(sym: str):
    vals = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7,
        'H': 8
    }
    try:
        return vals[sym]
    except:
        return None


def board_printing():
    global board
    for el in board:
        for i in el:
            if i in POSITIONS:
                (print(f'{BOARD_BLACK}{i}', end=''))
                continue
            print(i.__str__(), end=' ')
        print(Style.RESET_ALL)




player = 'White'
hit_status = False
while True:
    system('clear')

    x, y = 0, 0
    board_printing()
    print(player)

    pos = input('Type the figure position :')
    if len(pos) != 2:
        continue
    
    y = detect_y(pos[0].upper())
    x = int(pos[1])

    if board[y][x].obj_color != player.lower():
        continue


    pos = input('Type the move position')
    if len(pos) != 2:
        continue
    
    y_move = detect_y(pos[0].upper())
    x_move = int(pos[1])

    if hit_status == True:
        state = input('Type "lose" to surrender : ')
        if state[0] == 'l' or state[0] == 'L':
            player = 'White' if player == 'Black' else 'Black'
            print(f'{player} win!!!')
            exit()

    hit_status = board[y][x].move(y_move, x_move)

    system('clear')
    player = 'White' if player == 'Black' else 'Black'