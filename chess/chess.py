import pygame as pg
import math

pg.init()

WINDOWHEIGHT = 800
WINDOWWITDH=950
TILESIZE=100
TILEVERTICAL=8
TILEHORIZONTAL=8
WHITE=(255,255,255)
BLACK=(0,0,0)
promote = False
screen=pg.display.set_mode([WINDOWWITDH,WINDOWHEIGHT])

def is_path_clear(start, end, players):

    x1,y1 = start
    x2,y2=end

    if x1 == x2:  # Vertical movement (rook)
        step = 1 if y2 > y1 else -1
        for y in range(y1 + step, y2, step):
            if any(player.pos == (x1, y) for player in players):
                return False
    elif y1 == y2:  # Horizontal movement (rook)
        step = 1 if x2 > x1 else -1
        for x in range(x1 + step, x2, step):
            if any(player.pos == (x, y1) for player in players):
                return False
    else:  # Diagonal path
        x_step = 100 if start[0] < end[0] else -100
        y_step = 100 if start[1] < end[1] else -100
        x, y = start[0] + x_step, start[1] + y_step
        while x != end[0] and y != end[1]:
            if any(player.pos == (x, y) for player in players):
                return False
            x += x_step
            y += y_step
    return True

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pg.font.Font(None, 36)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

class Player:

    piece_images = {
    'white_rook': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whiterook.png").convert_alpha(),
    'black_rook': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackrook.png").convert_alpha(),
    'white_knight': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whiteknight.png").convert_alpha(),
    'black_knight': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackknight.png").convert_alpha(),
    'white_bishop': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whitebishop.png").convert_alpha(),
    'black_bishop': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackbishop.png").convert_alpha(),
    'white_queen': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whitequeen.png").convert_alpha(),
    'black_queen': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackqueen.png").convert_alpha(),
    'white_king': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whiteking.png").convert_alpha(),
    'black_king': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackking.png").convert_alpha(),
    'white_pawn': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/whitepawn.png").convert_alpha(),
    'black_pawn': pg.image.load("C:/Users/Aarav/Documents/VsCode/chess/pieces/blackpawn.png").convert_alpha()
    }

    def __init__(self,surface,color,pos,type,direction):
        self.surface=surface
        self.pos=pos
        self.color=color
        self.type=type
        self.font=pg.font.Font(None,36)
        self.direction=direction
        self.image = self.piece_images[f"{'white' if color == WHITE else 'black'}_{type}"]
    
    def draw(self):
        # Calculate the top-left corner position of the image
        top_left_pos = ((self.pos[0] - self.image.get_width() // 2)-2, (self.pos[1] - self.image.get_height() // 2))
        # Draw the piece image at its position
        self.surface.blit(self.image, top_left_pos)

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.pos[0])**2 + (pos[1] - self.pos[1])**2)
        return distance <= 40
    
    def move_diagonally(self, target): #Bishop movement
        x = (100 * (target[0] // 100)) + 50
        y = (100 * (target[1] // 100)) + 50
        if abs(x - self.pos[0]) == abs(y - self.pos[1]):  
            if is_path_clear(self.pos,(x,y),players):
                self.pos = (x, y)

    def move_vertically(self,target): #rook movement
        x=(100*(target[0]//100))+50
        y=(100*(target[1]//100))+50

        if x==self.pos[0] and y!=self.pos[1]:
            if is_path_clear(self.pos,(x,y),players):
                self.pos=(x,y)
        elif x!=self.pos[0] and y==self.pos[1]:
            if is_path_clear(self.pos,(x,y),players):
                self.pos=(x,y)

    def move_lshape(self,target): # Knight movement
        x=(self.pos[0])
        y=(self.pos[1])

        possible_moves=[
            (x+200,y+100),
            (x+200,y-100),
            (x-200,y+100),
            (x-200,y-100),
            (x+100,y+200),
            (x+100,y-200),
            (x-100,y+200),
            (x-100,y-200)
        ]

        for move in possible_moves:
            if abs(move[0] - target[0]) < 100 and abs(move[1] - target[1]) < 100:
                self.pos = (move[0], move[1])
                break

    def move_queen(self,target):

        x = (100 * (target[0] // 100)) + 50
        y = (100 * (target[1] // 100)) + 50

        if abs(x - self.pos[0]) == abs(y - self.pos[1]):  
            if is_path_clear(self.pos,(x,y),players):
                self.pos = (x, y)
        if x==self.pos[0] and y!=self.pos[1]:
            if is_path_clear(self.pos,(x,y),players):
                self.pos = (x, y)
        elif x!=self.pos[0] and y==self.pos[1]:
            if is_path_clear(self.pos,(x,y),players):
                self.pos = (x, y)

    def move_king(self, target,players):  #King movement
        x = (100 * (target[0] // 100)) + 50 
        y = (100 * (target[1] // 100)) + 50 
        if abs(x - self.pos[0]) <= 100 and abs(y - self.pos[1]) <= 100: 
            original_pos = self.pos
            self.pos = (x,y)
            if not self.is_checked(players):
                return
            self.pos = original_pos

    def promote(self,choice):
        self.type = choice
        
    def move_pawn(self, target): # Pawn movement 
        x_target = (100 * (target[0] // 100)) + 50  # Calculate target x position
        y_target = (100 * (target[1] // 100)) + 50  # Calculate target y position

        starting_row = 150 if self.color == WHITE else 650
        one_square_move = self.pos[1] + (100 * self.direction)
        two_square_move = self.pos[1] + (200 * self.direction)

        print(f"Pawn position: {self.pos}, Target: {target}, x_target: {x_target}, y_target: {y_target}")

    # Allow two-square move from the starting row
        if self.pos[1] == starting_row and y_target == two_square_move and x_target == self.pos[0]:
            print("Moving pawn two squares from starting row.")
            self.pos = (x_target, y_target)
    # Allow one-square move from any other row
        elif y_target == one_square_move and x_target == self.pos[0]:
            print("Moving pawn one square.")
            self.pos = (x_target, y_target)
        else:
            print("Invalid pawn move.")


    def move(self,target,players):

        if self.type=='rook':
            self.move_vertically(target)
        elif self.type=='bishop':
            self.move_diagonally(target)
        elif self.type=='knight':
            self.move_lshape(target)
        elif self.type=='queen':
            self.move_queen(target)
        elif self.type=='king':
            self.move_king(target,players)
        elif self.type=='pawn':
            self.move_pawn(target)

        for player in players:
            if player.pos == self.pos and player.color != self.color:
                players.remove(player)

    def is_checked(self, players):
        for player in players:
            if player.color != self.color:
                if player.can_attack(self.pos,players):
                    return True
        return False

    def can_attack(self, target_pos,players):
        # This function checks if the current piece can attack the target position
        if self.type == 'rook':
            return self.pos[0] == target_pos[0] or self.pos[1] == target_pos[1] and is_path_clear(self.pos,target_pos,players)
        elif self.type == 'bishop':
            return abs(self.pos[0] - target_pos[0]) == abs(self.pos[1] - target_pos[1]) and is_path_clear(self.pos,target_pos,players)
        elif self.type == 'queen':
            return (self.pos[0] == target_pos[0] or self.pos[1] == target_pos[1] or 
                    abs(self.pos[0] - target_pos[0]) == abs(self.pos[1] - target_pos[1])) and is_path_clear(self.pos,target_pos,players)
        elif self.type == 'knight':
            return (abs(self.pos[0] - target_pos[0]), abs(self.pos[1] - target_pos[1])) in [(200, 100), (100, 200)]
        elif self.type == 'pawn':
            direction = 100 * self.direction
            return self.pos[0] == target_pos[0] and self.pos[1] + direction == target_pos[1]
        return False

button1 = Button(800,0,150,50,(100,100,100),'queen')
button2 = Button(800,50,150,50,(100,100,100),'knight')
button3 = Button(800,100,150,50,(100,100,100),'bishop')
button4 = Button(800,150,150,50,(100,100,100),'rook')

players = [
    # White pieces
    Player(screen, WHITE, (50, 50), 'rook', 0),  # White rook
    Player(screen, WHITE, (150, 50), 'knight', 0),  # White knight
    Player(screen, WHITE, (250, 50), 'bishop', 0),  # White bishop
    Player(screen, WHITE, (350, 50), 'queen', 0),  # White queen
    Player(screen, WHITE, (450, 50), 'king', 0),  # White king
    Player(screen, WHITE, (550, 50), 'bishop', 0),  # White bishop
    Player(screen, WHITE, (650, 50), 'knight', 0),  # White knight
    Player(screen, WHITE, (750, 50), 'rook', 0),  # White rook
    # White pawns
    Player(screen, WHITE, (50, 150), 'pawn', 1),
    Player(screen, WHITE, (150, 150), 'pawn', 1),
    Player(screen, WHITE, (250, 150), 'pawn', 1),
    Player(screen, WHITE, (350, 150), 'pawn', 1),
    Player(screen, WHITE, (450, 150), 'pawn', 1),
    Player(screen, WHITE, (550, 150), 'pawn', 1),
    Player(screen, WHITE, (650, 150), 'pawn', 1),
    Player(screen, WHITE, (750, 150), 'pawn', 1),

    # Black pieces (at the bottom of the board now)
    Player(screen, BLACK, (50, 750), 'rook', 0),  # Black rook
    Player(screen, BLACK, (150, 750), 'knight', 0),  # Black knight
    Player(screen, BLACK, (250, 750), 'bishop', 0),  # Black bishop
    Player(screen, BLACK, (350, 750), 'queen', 0),  # Black queen
    Player(screen, BLACK, (450, 750), 'king', 0),  # Black king
    Player(screen, BLACK, (550, 750), 'bishop', 0),  # Black bishop
    Player(screen, BLACK, (650, 750), 'knight', 0),  # Black knight
    Player(screen, BLACK, (750, 750), 'rook', 0),  # Black rook
    # Black pawns
    Player(screen, BLACK, (50, 650), 'pawn', -1),
    Player(screen, BLACK, (150, 650), 'pawn', -1),
    Player(screen, BLACK, (250, 650), 'pawn', -1),
    Player(screen, BLACK, (350, 650), 'pawn', -1),
    Player(screen, BLACK, (450, 650), 'pawn', -1),
    Player(screen, BLACK, (550, 650), 'pawn', -1),
    Player(screen, BLACK, (650, 650), 'pawn', -1),
    Player(screen, BLACK, (750, 650), 'pawn', -1),
]



buttons = []

is_running = True

selected_player=None

while is_running: #Game loop
    
    screen.fill((0,100,0))

    rect = pg.draw.rect(screen,(0,0,0),(800,0,10,800))
    
    for row in range(TILEHORIZONTAL): # drawing the grid
        for col in range(row%2,TILEHORIZONTAL,2):
            pg.draw.rect(
                    screen,
                    (220, 200, 200),
                    (row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE),
                )

    for player in players:
        player.draw()

    for button in buttons:
        button.draw(screen)

    for event in pg.event.get(): # event handler
        if event.type == pg.KEYDOWN:
            print(event.key)
            if event.key == pg.K_ESCAPE:
                is_running=False
        elif event.type == pg.QUIT:
            is_running=False
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            print(pos)
            if selected_player is None:
                for player in players:
                    if player.is_clicked(pos):
                        selected_player=player
                        print(selected_player)
                        print(f"{player.type} clicked")
            else:
                selected_player.move(pos,players)
                selected_player=None

            if buttons:                                                     # PAWN PROMOTION LOGIC
                for button in buttons:
                    if button.is_clicked(pos):
                        choice = button.text
                        for player in players:
                            if player.color==(0,0,0):
                                if player.type=='pawn' and player.pos[1]==50:
                                    player.promote(choice)
                                    selected_player=None
                                    buttons.remove(button1)
                                    buttons.remove(button2)
                                    buttons.remove(button3)
                                    buttons.remove(button4)
                            elif player.color==WHITE:
                                if player.type=='pawn' and player.pos[1]==750:
                                    player.promote(choice)
                                    selected_player=None
                                    buttons.remove(button1)
                                    buttons.remove(button2)
                                    buttons.remove(button3)
                                    buttons.remove(button4)

    for player in players:
        if player.type == 'king' and player.is_checked(players):
            print("King is in check!")
            font = pg.font.Font(None,32)
            if player.color == (0,0,0):
                text_surface = font.render('King in check!', True, (0, 0, 0))
            else:
                text_surface = font.render('King in check!', True, (255, 255, 255))
            screen.blit(text_surface,(800,250))

    pg.display.update()
    