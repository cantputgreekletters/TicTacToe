#Imports
import pygame
#Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
X = pygame.image.load("Images\X.png")
O = pygame.image.load("Images\O.png")

Clicked = False
Player = "X"
def ChangePlayer():
    global Player
    if Player == "X": Player = "O" 
    else: Player = "X"
#Classes
class MenuButton:
    def __init__(self,image,hovered_image,command) -> None:
        self._image = image
        self._hovered_image = hovered_image
        self._command = command

    
    def Draw(self,pos:tuple):
        self._pos = pos
        Image = self._image
        if self._CheckIfMouseHovering():
            Image = self._hovered_image
            if Clicked:
                self._command()
        SCREEN.blit(Image,pos)
    
    def _CheckIfMouseHovering(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        imW,imH = self._image.get_size()
        return mouseX in range(int(self._pos[0]),int(self._pos[0]) + imW + 1) and mouseY in range(int(self._pos[1]), int(self._pos[1]) + imH + 1)

class Button:
    def __init__(self) -> None:
        self._state = None

    def Draw(self,pos:tuple):
        global Clicked
        if self._state == "X":
            SCREEN.blit(X,pos)
        elif self._state == "O":
            SCREEN.blit(O,pos)
        imW,imH = X.get_size()
        mouseX,mouseY = pygame.mouse.get_pos()
        if mouseX in range(int(pos[0]),int(pos[0]) + imW + 1) and mouseY in range(int(pos[1]), int(pos[1]) + imH + 1):
            self._OnHover(pos)
            if Clicked: 
                self._OnClick()

    def _OnHover(self,pos):
        x,y = pos
        width,height = X.get_size()
        rect = pygame.Rect(x,y,width,height)
        color = pygame.Color(10,10,10,255)
        pygame.draw.rect(SCREEN,color,rect)
    
    def _OnClick(self):
        print(f"Turned {Player}")
        if self._state == None:
            self._state = Player
            ChangePlayer()

    def ViewState(self):
        return self._state
    
class Board:
    def __init__(self,size = 30) -> None:
        self.size = size
        self.color = "white"
        self.board = {
            0:(None, "X", None),
            1:(None, None, "O"),
            2:(None, "X", None)
        }
        self.Ended = False
        self.Won = 0
        self.Reset()
        

    def __GetPiece(self,x,y):
        return self.board[y][x]

    def __draw_horizontal(self):
        StartPos = pygame.Vector2(self.size,SCREEN_HEIGHT / 4 + self.size)
        EndPos = pygame.Vector2(SCREEN_WIDTH - self.size, SCREEN_HEIGHT / 4 + self.size)
        pygame.draw.line(SCREEN,self.color,StartPos,EndPos)
        StartPos = pygame.Vector2(self.size,SCREEN_HEIGHT - self.size - SCREEN_HEIGHT / 4)
        EndPos = pygame.Vector2(SCREEN_WIDTH - self.size, SCREEN_HEIGHT - self.size - SCREEN_HEIGHT / 4)
        pygame.draw.line(SCREEN,self.color,StartPos,EndPos)

    def __draw_vertical(self):
        StartPos = pygame.Vector2(SCREEN_WIDTH / 3,self.size)
        EndPos = pygame.Vector2(SCREEN_WIDTH / 3, SCREEN_HEIGHT - self.size)
        pygame.draw.line(SCREEN,self.color,StartPos,EndPos)
        StartPos = pygame.Vector2(SCREEN_WIDTH - SCREEN_WIDTH / 3,self.size)
        EndPos = pygame.Vector2(SCREEN_WIDTH - SCREEN_WIDTH / 3, SCREEN_HEIGHT - self.size)
        pygame.draw.line(SCREEN,self.color,StartPos,EndPos)

    def __draw_board(self):
        
        for x in range(3):
            
            for y in range(3):
                xpos = x * (SCREEN_WIDTH / 3) + 30
                ypos = y * (SCREEN_HEIGHT / 3) + 30
                self.__GetPiece(x,y).Draw((xpos,ypos))                

    def __ver_check(self):
        for x in range(3):
            if self.__GetPiece(x,0).ViewState() and self.__GetPiece(x,0).ViewState() == self.__GetPiece(x,1).ViewState() == self.__GetPiece(x,2).ViewState():
                if self.__GetPiece(x,0).ViewState() == "X":
                    self.Won = 1
                else:
                    self.Won = 2
                self.Ended = True
                return
            
    def __hor_check(self):
        for y in range(3):
            if self.__GetPiece(0,y).ViewState() and self.__GetPiece(0,y).ViewState() == self.__GetPiece(1,y).ViewState() == self.__GetPiece(2,y).ViewState():
                if self.__GetPiece(0,y).ViewState() == "X":
                    self.Won = 1
                else:
                    self.Won = 2
                self.Ended = True
                return

    def __diagn_check(self):
        cond1 = self.__GetPiece(0,0).ViewState() == self.__GetPiece(1,1).ViewState() == self.__GetPiece(2,2).ViewState()
        cond11 = self.__GetPiece(0,0).ViewState() and self.__GetPiece(1,1).ViewState() and self.__GetPiece(2,2).ViewState()
        cond2 = self.__GetPiece(0,2).ViewState() == self.__GetPiece(1,1).ViewState() == self.__GetPiece(2,0).ViewState()
        cond22 = self.__GetPiece(0,2).ViewState() and self.__GetPiece(1,1).ViewState() and self.__GetPiece(2,0).ViewState()
        if (cond1 and cond11) or (cond2 and  cond22):
            if self.__GetPiece(1,1) == "X":
                self.Won = 1
            else:
                self.Won = 2
            self.Ended = True
            return

    def __check_if_full(self):
        for x in range(3):
            for y in range(3):
                if not self.__GetPiece(x,y).ViewState():
                    return
        self.Ended = True

    def CheckBoard(self):
        """Checks if someone won"""
        self.__ver_check()
        if self.Ended: return
        self.__hor_check()
        if self.Ended: return
        self.__diagn_check()
        if self.Ended: return
        self.__check_if_full()
    
    def HasEnded(self):
        if self.Ended:
            self.Reset()
    
    def Reset(self):
        self.board = {}
        for i in range(3):
            self.board[i] = []
            for _ in range(3):
                self.board[i].append(Button())
        self.Ended = False
        self.Won = 0
        global Player
        Player = "X"

    def Draw(self):
        self.__draw_horizontal()
        self.__draw_vertical()
        self.__draw_board()



#Functions

def StartButtonC():
    mainloop()

def QuitButtonC():
    Running = False

def StartScreen():
    global Clicked
    im1 = pygame.image.load("Images\Start.png")
    im2 = pygame.image.load("Images\Start_Hovered.png")
    StartButton = MenuButton(im1,im2,StartButtonC)
    im1 = pygame.image.load("Images\Quit.png")
    im2 = pygame.image.load("Images\Quit_Hovered.png")
    QuitButton = MenuButton(im1,im2,QuitButtonC)
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                Clicked = False

        SCREEN.fill('black')
        #Render:
        StartButton.Draw((SCREEN_WIDTH / 2 - im1.get_width() / 2, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 3))
        QuitButton.Draw((SCREEN_WIDTH / 2 - im1.get_width() / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 3))
        pygame.display.flip()
        CLOCK.tick(60)

def mainloop():
    global Clicked
    RUNNING = True
    board = Board()
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                Clicked = False
        SCREEN.fill('black')
        board.Draw()
        board.CheckBoard()
        board.HasEnded()
        
        pygame.display.flip()
        CLOCK.tick(60)


#Main
pygame.init()
StartScreen()
pygame.quit()