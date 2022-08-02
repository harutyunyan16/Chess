from os import system
from time import sleep
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

    def in_hit(self, color, self_color):
        x = 0
        y = 0
        for i in range(1, 9):
            for el in range(1, 9):
                if board[i][el].obj_color == color and (board[i][el].obj == ICONS['king_black'] or board[i][el].obj == ICONS['king_white']):
                    y = i
                    x = el
        opponents = []
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i][j].obj_color == self_color and not board[i][j].empty():
                    res = figure_detacting(board[i][j])
                    if res.icon == ICONS['king_white'] or res.icon == ICONS['king_black']:
                        continue
                    opponents.append(res)

        j = 0
        for i in opponents:
            if i.move(x, y, True) == True:
                board[y][x].color = BOARD_ICON['yellow']
                board[y][x].setFigure(figure_detacting(board[y][x]))
                return True
            j += 1

        return False

    def __str__(self):
        return self.icon

    def move(self, y, x):
        opponent_color = 'white' if self.obj_color == 'black' else 'black'
        color = 'white' if self.obj_color == 'white' else 'black'
        figure = figure_detacting(self)
        figure.move(x, y)
        hit_status = self.in_hit(opponent_color, color)
        



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
            if self.y == y + 1 and self.x == x and board[y][x].empty() or (self.y == 7 and self.x == x and self.y - 2 == y and board[y][x].empty()):
                return True
            elif self.y == y + 1 and self.x == x + 1 and 'black' != board[y][x].obj_color and not board[y][x].empty():
                return True
            elif self.y == y + 1 and self.x == x - 1 and 'black' != board[y][x].obj_color and not board[y][x].empty():
                return True
            else:
                return False
        else:
            if self.y == y - 1 and self.x == x and board[y][x].empty() or (self.y == 2 and self.x == x and self.y + 2 == y and board[y][x].empty()):
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
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y


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
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
    

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
            board[self.y][self.x].clear()
            board[y][x].setFigure(self)
            self.x = x
            self.y = y
        

    def __str__(self) -> str:
        return self.icon



board = [
    ['1', '2', '3', '4', '5', '6', '7', '8'],
    ['A', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['B', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) ],
    ['C', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['D', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) ],
    ['E', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) ],
    ['F', BoardSquare(BOARD_ICON['black'])  ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']) , BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) ],
    ['G', BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black'])],
    ['H', BoardSquare(BOARD_ICON['black']) ,BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) , BoardSquare(BOARD_ICON['black']), BoardSquare(BOARD_ICON['white']) ],
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

while True:
    system('clear')

    x, y = 0, 0
    board_printing()
    print(player)

    pos = input('Type the figure position :')
    if len(pos) > 2:
        continue
    
    y = detect_y(pos[0].upper())
    x = int(pos[1])

    if board[y][x].obj_color != player.lower():
        continue


    pos = input('Type the move position')
    if len(pos) > 2:
        continue
    
    y_move = detect_y(pos[0])
    x_move = int(pos[1])

    board[y][x].move(y_move, x_move)

    system('clear')
    player = 'White' if player == 'Black' else 'Black'
    
