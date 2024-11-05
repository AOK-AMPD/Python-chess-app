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
    def __init__(self,surface,color,pos,type,direction):
        self.surface=surface
        self.pos=pos
        self.color=color
        self.type=type
        self.font=pg.font.Font(None,36)
        self.direction=direction
    
    def draw(self):
        pg.draw.circle(self.surface,self.color,self.pos,40)
        if self.color==(0,0,0):
            text_surface = self.font.render(self.type, True, (255, 255, 255))
        else:
            text_surface = self.font.render(self.type,True,(0,0,0))

        self.surface.blit(text_surface,(self.pos[0]-40,self.pos[1]))

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.pos[0])**2 + (pos[1] - self.pos[1])**2)
        return distance <= 40
    
    def move_diagonally(self, target): #Bishop movement
        x = (100 * (target[0] // 100)) + 50
        y = (100 * (target[1] // 100)) + 50
        if abs(x - self.pos[0]) == abs(y - self.pos[1]):  
            self.pos = (x, y)

    def move_vertically(self,target): #rook movement
        x=(100*(target[0]//100))+50
        y=(100*(target[1]//100))+50

        if x==self.pos[0] and y!=self.pos[1]:
            self.pos=(x,y)
        elif x!=self.pos[0] and y==self.pos[1]:
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
            self.pos = (x, y)

        if x==self.pos[0] and y!=self.pos[1]:
            self.pos=(x,y)
        elif x!=self.pos[0] and y==self.pos[1]:
            self.pos=(x,y)

    def move_king(self, target):  #King movement
        x = (100 * (target[0] // 100)) + 50 
        y = (100 * (target[1] // 100)) + 50 
        if abs(x - self.pos[0]) <= 100 and abs(y - self.pos[1]) <= 100: 
            self.pos = (x,y)

    def promote(self,choice):
        self.type = choice
        
    def move_pawn(self, target): # Pawn movement 
        x = self.pos[0]
        y = (100 * (target[1] // 100)) + 50 

        if self.color==(0,0,0):
            if self.pos[1]==650: # Check if pawn is on 2nd rank (white) or 7th rank (black) 
                if y == self.pos[1] + (100 * self.direction) or y == self.pos[1] + (200 * self.direction): # Allow one or two squares move 
                    self.pos = (x, y) 
            else: 
                if y == self.pos[1] + (100 * self.direction): # Allow only one square move 
                    self.pos = (x, y)

            if self.pos[1]==50:
                buttons.append(button1)
                buttons.append(button2)
                buttons.append(button3)
                buttons.append(button4)

        elif self.color==(255,255,255):
            if self.pos[1]==150:
                if y == self.pos[1]+(100*self.direction) or y == self.pos[1]+(200*self.direction): # Same concept here
                    self.pos=(x,y)
            else:
                if y == self.pos[1]+(100*self.direction):
                    self.pos(x,y)

            if self.pos[1]==750:
                buttons.append(button1)
                buttons.append(button2)
                buttons.append(button3)
                buttons.append(button4)

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
            self.move_king(target)
        elif self.type=='pawn':
            self.move_pawn(target)

        for player in players:
            if player.pos == self.pos and player.color != self.color:
                players.remove(player)

    def is_checked(self, players):
        for player in players:
            if player.color != self.color:
                if player.can_attack(self.pos):
                    return True
        return False

    def can_attack(self, target_pos):
        # This function checks if the current piece can attack the target position
        if self.type == 'rook':
            return self.pos[0] == target_pos[0] or self.pos[1] == target_pos[1]
        elif self.type == 'bishop':
            return abs(self.pos[0] - target_pos[0]) == abs(self.pos[1] - target_pos[1])
        elif self.type == 'queen':
            return (self.pos[0] == target_pos[0] or self.pos[1] == target_pos[1] or 
                    abs(self.pos[0] - target_pos[0]) == abs(self.pos[1] - target_pos[1]))
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
    Player(screen, WHITE, (50, 50), 'rook',0),
    Player(screen, BLACK, (150, 750), 'knight',0),
    Player(screen, WHITE, (250, 50), 'bishop',0),
    Player(screen, WHITE, (750,50), 'queen',0),
    Player(screen, BLACK, (550,750), 'king',0),
    Player(screen, BLACK, (650,750),'pawn',-1)
]

buttons = []

is_running = True

selected_player=None

while is_running: #Game loop
    
    screen.fill((0,100,0))
    
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
                        print(f"{player.type} clicked")
            else:
                selected_player.move(pos,players)
                selected_player=None

            if buttons:
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

    pg.display.update()
    
