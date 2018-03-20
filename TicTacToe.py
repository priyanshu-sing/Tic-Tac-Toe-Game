import random, sys, pygame, time, copy
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 120 # width & height of each space on the board, in pixels
BOARDWIDTH = 3 # how many columns of spaces on the game board
BOARDHEIGHT = 3 # how many rows of spaces on the game board
WHITE_TILE = 'WHITE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation
bot_moves=0
win_combo = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[2,4,6],[0,4,8]]
win_combo1 = [[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]],[[0,0],[1,0],[2,0]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]],[[0,2],[1,1],[2,0]],[[0,0],[1,1],[2,2]]]
# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Tic Tac Toe')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Set up the background image.
    boardImage = pygame.image.load('flippyboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)
    while True:
        if runGame()==False:
        	break

def runGame():
    # Plays a single game of reversi each time this function is called.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    turn = random.choice(['computer', 'player'])
    bot_moves=0
    flag=0
    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = BIGFONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright= (WINDOWWIDTH - 8, 10)
    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            # Player's turn:
            if getValidMoves(mainBoard, playerTile) == False:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.
                boardToDraw = mainBoard
                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                            movexy = None
                        elif movexy!=None: 
                            mainBoard[movexy[0]][movexy[1]]=playerTile
                            if check_win(mainBoard,playerTile)==True:
                            	flag=1
                            break
                
                # Draw the game board.
                drawBoard(mainBoard)
                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                MAINCLOCK.tick(FPS)
                pygame.display.update()
            if flag==1 :
            	break
            # Make the move and end the turn.
            #makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) != False:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            # Computer's turn:
            if getValidMoves(mainBoard, computerTile) == False:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break
            if flag==1 :
            	break
            # Draw the board.
            drawBoard(mainBoard)
            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(newGameSurf, newGameRect)

            # Make it look like the computer is thinking by pausing a bit.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            x, y = getComputerMove(mainBoard, computerTile,playerTile)
            bot_moves=bot_moves+1
            mainBoard[x][y]=computerTile
            if check_win(mainBoard,computerTile)==True:
            	flag=2
            	break
            if getValidMoves(mainBoard, playerTile) != False:
                # Only set for the player's turn if they can make a move.
                turn = 'player'

   
    drawBoard(mainBoard)
    # Determine the text of the message to display.
    if flag==0:
        text="Match Tie"
    if flag==1:
    	text="You Won"
    if flag==2:
    	text="Computer Won"
    textSurf = BIGFONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
def getComputerMove(board,cTile,pTile):
    moved = False
    first_corner = None 

    #checks for a win in next turn (getting 3 in a row)
    for x,y,z in win_combo:
        x1, x2 = func(x)
        y1, y2 = func(y)
        z1, z2 = func(z)
        if board[x1][x2] == cTile and board[y1][y2] == cTile and board[z1][z2] ==EMPTY_SPACE:
            return func(z)
            break
            moved = True
        if board[z1][z2] == cTile and board[y1][y2] == cTile and board[x1][x2] ==EMPTY_SPACE:
            return func(x)
            break
            moved = True
        if board[x1][x2] == cTile and board[z1][z2] == cTile and board[y1][z2] ==EMPTY_SPACE:
            return func(y)
            break
            moved = True

        # Offensive !! Blocks Player for getting (3 in a row i.e Win)
    for x,y,z in win_combo:
        x1,x2=func(x)
        y1,y2=func(y)
        z1,z2=func(z)
        if board[x1][x2] == pTile and board[y1][y2] == pTile and board[z1][z2] ==EMPTY_SPACE:
            return func(z)
            break
            moved = True
        if board[z1][z2] == pTile and board[y1][y2] == pTile and board[x1][x2] ==EMPTY_SPACE:
            return func(x)
            break
            moved = True
        if board[x1][x2] == pTile and board[z1][z2] == pTile and board[y1][y2] ==EMPTY_SPACE:
            return func(y)
            break
            moved = True
    if bot_moves == 0 and moved == False:
        if board[1][1] ==EMPTY_SPACE:
            return func(4)
            moved = True
    if bot_moves == 1 and moved == False:
        if board[0][0] == board[2][2] == pTile or board[0][3] == board[2][0] == pTile:
            return random.choice([func(1),func(3),func(5),func(7)])
            moved = True
    off_corner = None 
    if bot_moves == 0 and moved == False:
        if board[1][1] == pTile:
            off_corner = random.choice([func(0),func(2),func(6),func(8)])
            return off_corner
            moved = True
    if moved == False:
        Board1 = []
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[y][x]==EMPTY_SPACE:
                    Board1.append(func1(y,x))
        return func(random.choice(Board1))
def func1(x,y):
    if x==0 and y==0:
        return 0
    if x==0 and y==1:
    	return 1
    if x==0 and y==2:
    	return 2
    if x==1 and y==0:
    	return 3
    if x==1 and y==1:
    	return 4
    if x==1 and y==2:
    	return 5
    if x==2 and y==0:
    	return 6
    if x==2 and y==1:
    	return 7
    if x==2 and y==2:
    	return 8
def func(x):
	if x==0:
	    return [0,0]
	if x==1:
		return [0,1]
	if x==2:
		return [0,2]
	if x==3:
		return [1,0]
	if x==4:
		return [1,1]
	if x==5:
		return [1,2]
	if x==6:
		return [2,0]
	if x==7:
		return [2,1]
	if x==8:
		return [2,2]

def check_win(board,player):
    for x,y,z in win_combo:
        x1,x2=func(x)
        y1,y2=func(y)
        z1,z2=func(z)
        if board[x1][x2] == board[y1][y2] == board[z1][z2] == player:
            return True
            break
    return False
 
def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the black & white tiles or hint spots.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            if board[x][y] == HINT_TILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None
def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board
def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

   
def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)
def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [WHITE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, WHITE_TILE] if Black.

    # Create the text.
    textSurf = BIGFONT.render('choose your colour :', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITE_TILE, BLACK_TILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACK_TILE, WHITE_TILE]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y]==EMPTY_SPACE:
                return True
    return False
def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    return True


if __name__ == '__main__':
    main()
