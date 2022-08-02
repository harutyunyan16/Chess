from pickletools import read_uint1
import re
from this import s
from tkinter.filedialog import asksaveasfile
from tkinter.tix import INCREASING
from colorama import Style


ICONS = {
    'soldier_white' : '♟',
    'soldier_black': '♙',
    'elephant_white': '♝',
    'elephant_black': '♗',
    'boat_black': '♖',
    'boat_white': '♜',
    'horse_black': '♘',
    'horse_white': '♞',
    'king_black': '♔',
    'king_white': '♚',
    'queen_black': '♕',
    'queen_white': '♛',
}


BOARD_ICON = {
    'white': '0;37;40m',
    'black': '0;37;48m',
    'yellow': '0;39;43m'
}


def figure_detacting(fig):
    if fig.obj == ICONS['soldier_white'] or fig.obj == ICONS['soldier_black'] :
        sold = Solider(icon=fig.obj, x=fig.x, y=fig.y)
        return sold
    elif fig.obj == ICONS['boat_white'] or fig.obj == ICONS['boat_black'] :
        boat = Boat(icon=fig.obj, x=fig.x, y=fig.y)
        return boat
    elif fig.obj == ICONS['horse_white'] or fig.obj == ICONS['horse_black'] :
        horse = Horse(icon=fig.obj, x=fig.x, y=fig.y)
        return horse
    elif fig.obj == ICONS['elephant_white'] or fig.obj == ICONS['elephant_black'] :
        el = Elephant(icon=fig.obj, x=fig.x, y=fig.y)
        return el
    elif fig.obj == ICONS['queen_white'] or fig.obj == ICONS['queen_black'] :
        quenn = Queen(icon=fig.obj, x=fig.x, y=fig.y)
        return quenn
    elif fig.obj == ICONS['king_white'] or fig.obj == ICONS['king_black'] :
        king = King(icon=fig.obj, x=fig.x, y=fig.y)
        return king

#Game models
class BoardSquare():
    obj = ' '
    obj_color = ''
    color = ''
    x = None
    y = None

    def __init__(self, color):
        self.color = color
        self.icon = f'\033[{self.color} {self.obj}'

    def setFigure(self, fig):
        self.obj = fig.icon
        self.icon = f'\033[{self.color} {self.obj}'
        for key, value in ICONS.items():
            if value == fig.icon:
                self.obj_color = key.split('_')[1]

    def empty(self):
        return True if self.obj == ' ' else False

    def get_color(self):
        return self.color

    def is_king(self):
        if self.obj == ICONS['king_black'] or self.obj == ICONS['king_white']:
            return True
        return False

    def clear(self):
        self.obj = ' ' 
        self.icon = f'\033[{self.color} {self.obj}'

    def in_hit(self, color):
        x = 0
        y = 0
        for i in range(1, 9):
            for el in range(1, 9):
                if board[i][el].obj_color == color and (board[i][el].obj == ICONS['king_black'] or board[i][el].obj == ICONS['king_white']):
                    x = el
                    y = i
        opponents = []
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i][j].obj_color == color and not board[i][j].empty():
                    res = figure_detacting(board[i][j])
                    if res.icon == ICONS['king_white'] or res.icon == ICONS['king_black']:
                        continue
                    opponents.append(res)
        for i in opponents:
            print(i.icon)
            if i.move(y, x, True) == True:
                board[y][x].color = BOARD_ICON['yellow']
                print(board[y][x].color)
                print(i.icon)
                return True
        return False
    def __str__(self):
        return self.icon

    def move(self, y, x):
        opponent_color = 'white' if self.obj_color == 'black' else 'black'
        print(opponent_color)
        figure = figure_detacting(self)
        figure.move(x, y)
        print(self.in_hit(opponent_color))
        



class Solider():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x, y):
        self.icon = icon
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return self.icon

    def can_move(self, x, y):
        if self.icon == ICONS['soldier_black']:
            if self.y == y + 1 and board[y][x].empty():
                return True
            elif self.y == y + 1 and self.x == x + 1 and 'black' != board[y][x].obj_color and not board[y][x].empty():
                return True
            elif self.y == y + 1 and self.x == x - 1 and 'black' != board[y][x].obj_color and not board[y][x].empty():
                return True
            else:
                return False
        else:
            if self.y == y - 1 and self.x == x and board[y][x].empty():
                return True
            elif self.y == y - 1 and self.x == x + 1 and 'white' != board[y][x].obj_color and not board[y][x].empty():
                return True
            elif self.y == y - 1 and self.x == x - 1 and 'white' != board[y][x].obj_color and not board[y][x].empty():
                return True
            else:
                return False


    def move(self, x, y, dont_change=False):
        global board
        if dont_change == True:
            return self.can_move(x, y)
        res = self.can_move(x, y)
        if res == True and dont_change == False:
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
   

    


class Boat():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x=0, y=0):
        self.icon = icon
        self.x = x
        self.y = y
     
    def __str__(self) -> str:
        return self.icon

    def can_move(self, x, y):
        global board

        obj_color = 'white' if self.icon == ICONS['boat_white'] else 'black'
        if not board[y][x].empty():
            if obj_color == board[y][x].obj_color:
                return False


        if x == self.x:
            if self.y < y:
                i = self.y
                while i != y:
                    i += 1
                    if board[i][x].empty():
                        continue
                    elif i == y and  obj_color != board[y][x].obj_color:
                        return True
                    else:
                        return False
                return True
            elif self.y > y:
                i = self.y
                while i != y:
                    i -= 1
                    if board[i][x].empty():
                        continue
                    elif i == y and  obj_color != board[y][x].obj_color:
                        return True
                    else:
                        return False
                return True
        elif y == self.y:
            if self.x < x:

                i = self.x
                while i != x:
                    i += 1
                    if board[x][i].empty():
                        continue
                    elif i == x and  obj_color != board[y][x].obj_color:
                        return True
                    else:
                        return False
                
                return True
            elif self.x > x:

                i = self.x
                while i != x:
                    i -= 1
                    if board[y][i].empty():
                        continue
                    elif i == x and  obj_color != board[y][x].obj_color:
                        return True
                    else:
                        return False
                
                return True

        


    def move(self, x, y, dont_change=False):
        if dont_change == True:
            return self.can_move(x, y)
        if self.can_move(x, y) == True and dont_change == False:
            print(self.x ,self.y)
            print(x, y)
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
            print('boat')


class Elephant():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x=0, y=0):
        self.icon = icon
        self.x = x
        self.y = y

    def can_move(self, x, y):
        obj_color = 'white' if self.icon == ICONS['elephant_white'] else 'black'

        if not board[y][x].empty():
            if obj_color == board[y][x].obj_color:
                return False

        if self.y > y:
            if self.x > x:
                i = self.x
                tmp_y = self.y
                while x != i:
                    i -= 1
                    tmp_y -= 1
                    if not board[tmp_y][i].empty() and x != i:
                        return False
                if tmp_y == y:
                    return True
            if self.x < x:
                i = self.x
                tmp_y = self.y
                while x != i:
                    i += 1
                    tmp_y -= 1
                    if not board[tmp_y][i].empty() and x != i:
                        return False
                if tmp_y == y:
                    return True
        elif self.y < y:
            if self.x > x:
                i = self.x
                tmp_y = self.y

                while x != i:
                    i -= 1
                    tmp_y += 1
                    if not board[tmp_y][i].empty() and x != i:
                        return False
                if tmp_y == y:
                    return True
            if self.x < x:
                i = self.x
                tmp_y = self.y

                while x != i:
                    i += 1
                    tmp_y += 1
                    if not board[tmp_y][i].empty() and x != i:
                        return False
                if tmp_y == y:
                    return True
       

    def move(self, x, y, dont_change=False):
        global board
        res = self.can_move(x, y)
        if dont_change == True:
            return res
        if res == True and dont_change == False:
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
      


    def __str__(self) -> str:
        return self.icon


class Horse():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x=0, y=0):
        self.icon = icon
        self.x = x
        self.y = y


    def can_move(self, x, y):
        obj_color = 'white' if self.icon == ICONS['horse_white'] else 'black'

        if not board[y][x].empty() and  obj_color == board[y][x].obj_color:
            return False
        
        if ((x == self.x + 2 and y == self.y + 1) or (x == self.x + 2 and y == self.y - 1)) or ((x == self.x - 2 and y == self.y + 1) or (x == self.x - 2 and y == self.y - 1)):
            return True
        elif ((y == self.y + 2 and x == self.x + 1) or (y == self.y + 2 and x == self.x - 1)) or ((y == self.y - 2 and x == self.x + 1) or (y == self.y - 2 and x == self.x - 1)):
            return True
        return False

    def move(self, x, y, dont_change=False):
        if dont_change == True:
            return self.can_move(x, y)
        if self.can_move(x, y) and dont_change == False:
            print(x, y)
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
            print('horse')
    

    def __str__(self) -> str:
        return self.icon


class King():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x=0, y=0):
        self.icon = icon
        self.x = x
        self.y = y

    def can_move(self, x, y):
        obj_color = 'white' if self.icon == ICONS['king_white'] else 'black'

        if not board[y][x].empty() and  obj_color == board[y][x].obj_color:
            print('this case')
            return (False, False)

        (1, 5)
        (2, 5)

        board[self.y][self.x].clear()
        board[y][x].setFigure(self)
        
        if y == 1:
            if x == 1:
                if board[y][x + 1].is_king() or board[y + 1][x].is_king() or board[y + 1][x + 1]:
                    return False
            elif x == 8:
                if board[y][x - 1].is_king() or board[y + 1][x - 1].is_king() or board[y + 1][x].is_king():
                    return False
            elif board[y][x].is_king() or board[y][x + 1].is_king() or board[y][x - 1].is_king() or board[y + 1][x].is_king() or board[y + 1][x + 1].is_king() or board[y + 1][x - 1].is_king():
                return False
        elif y == 8:
            if x == 1:
                if board[y][x + 1].is_king() or board[y - 1][x].is_king() or board[y - 1][x + 1]:
                    return False
            elif x == 8:
                if board[y][x - 1].is_king() or board[y - 1][x - 1].is_king() or board[y - 1][x].is_king():
                    return False
            elif board[y][x].is_king() or board[y][x + 1].is_king() or board[y][x - 1].is_king() or board[y - 1][x].is_king() or board[y - 1][x + 1].is_king() or board[y - 1][x - 1].is_king():
                return False
        else:
            if x == 1:
                if board[y][x + 1].is_king() or board[y + 1][x].is_king() or board[y + 1][x + 1] or board[y - 1][x].is_king() or board[y - 1][x + 1].is_king():
                    return False
            elif x == 8:
                if board[y][x - 1].is_king() or board[y + 1][x - 1].is_king() or board[y + 1][x].is_king() or board[y - 1][x - 1].is_king() or board[y - 1][x].is_king():
                    return False
            else:
                if board[y][x + 1].is_king() or board[y][x - 1].is_king() or board[y - 1][x].is_king() or board[y - 1][x + 1].is_king() or board[y - 1][x - 1].is_king() or board[y + 1][x].is_king() or board[y + 1][x + 1].is_king() or board[y + 1][x - 1].is_king():
                    return False
        return True
        
        

    def move(self, x, y, dont_change=False):
        if dont_change == True:
            print('returing case')
            return self.can_move(x, y)

        res = self.can_move(x, y)
        if res == True  and dont_change == False:
            self.x = x
            self.y = y
        elif res == (False, False):
            board[self.y][self.x].setFigure(self)
        else:
            board[y][x].clear()
            board[self.y][self.x].setFigure(self)
        

    def __str__(self) -> str:
        return self.icon


class Queen():
    icon = ''
    x = None
    y = None

    def __init__(self, icon, x=0, y=0):
        self.icon = icon
        self.x = x
        self.y = y
    
    def can_move(self, x, y):
        boat = Boat(self.icon, self.x, self.y)
        el = Elephant(self.icon, self.x, self.y)
        obj_color = 'white' if self.icon == ICONS['queen_white'] else 'black'
        if obj_color == 'white':
            boat = Boat(ICONS['boat_white'], self.x, self.y)
            el = Elephant(ICONS['elephant_white'], self.x, self.y)
        else:
            boat = Boat(ICONS['boat_black'], self.x, self.y)
            el = Elephant(ICONS['elephant_black'], self.x, self.y)

        if boat.can_move(x, y):
            return True
        elif el.can_move(x, y):
            return True
        else:
            return False

    def move(self, x, y, dont_change=False):
        if dont_change == True:
            return self.can_move(x, y)
        if self.can_move(x, y) and dont_change == False:
            print('chlp -' ,self.x ,self.y)
            print(x, y)
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
            print('Queen')
        

    def __str__(self) -> str:
        return self.icon



board = [
    ['    A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H'],
    ['1', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['2', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) ],
    ['3', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['4', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) ],
    ['5', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['6', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) ],
    ['7', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black'])],
    ['8', BoardSquare(BOARD_ICON['black']) ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) ],
]




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

board[2][5].move(3, 5)
board[3][5].move(4, 5)
board[1][5].move(4, 6)
board[7][7].move(6, 7)
board[6][7].move(5, 7)
board[5][7].move(4, 7)
board[8][6].move(6, 8)
board[6][8].move(5, 7)
board[4][5].move(5, 5)
board[4][7].move(4, 6)



for el in board:
    for i in el:
        if i in POSITIONS:
            (print(f'{BOARD_BLACK}{i}', end=''))
            continue
        print(i.__str__(), end=' ')
    print(Style.RESET_ALL)

