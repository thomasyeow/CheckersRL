import pygame
#custom library containing function and constant definitions, for tidyness
from gameLogic import *

#initialize pygame
pygame.init()
pygame.display.set_caption("Checkers RL")

#VARIABLES
screen = pygame.display.set_mode((640,640))

    #import assets
redPieceImg = pygame.image.load("assets/redPiece.png").convert()
whitePieceImg = pygame.image.load("assets/whitePiece.png").convert()
redKingImg = pygame.image.load("assets/redKingPiece.png").convert()
whiteKingImg = pygame.image.load("assets/whiteKingPiece.png").convert()
boardImg = pygame.image.load("assets/Board.png").convert()
moveMarkerImg = pygame.image.load("assets/validMoveMarker.png").convert()

#SHORTCUT FUNCTIONS
    #draw piece to position and update boardArr ONLY for the destination
def drawPiece(pieceImg, position):
    screen.blit(pieceImg, getCoordinatesFromSquare(position[0], position[1]))

def victoryLossScreen(won: bool):
    message = ""
    if won:
        message = "VICTORY"
    else:
        message = "LOSS"
    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, (255,0,60), (0,0,128))
    textRect = text.get_rect()
    textRect.center = (640//2, 640//2)
    screen.fill((255,255,255))
    screen.blit(text, textRect)

    #redraw the entire board based on boardArr
def redrawBoard():
    screen.blit(boardImg, (0,0))
    for x in range(8):
        for y in range(8):
            if boardArr[x][y] == RED:
                drawPiece(redPieceImg, (x, y))
            elif boardArr[x][y] == WHITE:
                drawPiece(whitePieceImg, (x, y))
            elif boardArr[x][y] == REDKING:
                drawPiece(redKingImg, (x, y))
            elif boardArr[x][y] == WHITEKING:
                drawPiece(whiteKingImg, (x, y))
            
redrawBoard()
#Game Loop
running = True
while(running):
    
    for event in pygame.event.get():
        
        if currentPlayerLost():
            victoryLossScreen(False)
        reverseBoard()
        if currentPlayerLost():
            victoryLossScreen(True)
        reverseBoard()
        #QUIT
        if event.type == pygame.QUIT:
            running = False
        #MOUSE DOWN - does nothing but debugging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clickedSquare = getSquareFromCoordinates(event.pos)
            print("Board at " , clickedSquare, " contains a ", "WHITE" if getPiece(
                clickedSquare) == WHITE else "RED" if getPiece(clickedSquare) == RED else "EMPTY" if getPiece(
                    clickedSquare) == EMPTY else "REDKING" if getPiece(clickedSquare) == REDKING else "WHITEKING")
            
        #MOUSE UP
        elif event.type == pygame.MOUSEBUTTONUP:
            clickedSquare = getSquareFromCoordinates(event.pos)
            #if currently showing valid moves for some piece
            if showingValidMoves:
                for move in activePieceMoveList:
                    #if clicked on valid move square
                    if clickedSquare == move:
                        if getPiece(lastClickedRedPiece) == REDKING:
                            boardArr[clickedSquare[0]][clickedSquare[1]] = REDKING
                        else:
                            boardArr[clickedSquare[0]][clickedSquare[1]] = RED
                        boardArr[lastClickedRedPiece[0]][lastClickedRedPiece[1]] = EMPTY
                        
                        removeIfAttack(lastClickedRedPiece, clickedSquare)
                        #transform into king
                        if clickedSquare[1] == 0:
                            boardArr[clickedSquare[0]][clickedSquare[1]] = REDKING
                        reverseBoard()
                        if not currentPlayerLost():
                            reverseBoard()
                            AiTurn()
                        else:
                            reverseBoard()
                redrawBoard()
                showingValidMoves = False
            else:
                #if clicked on own piece
                if getPiece(clickedSquare) == RED or getPiece(clickedSquare) == REDKING:

                    activePieceMoveList = getMovesForPiece(clickedSquare)
                    #if clicked piece has valid moves
                    if len(activePieceMoveList) != 0:
                        showingValidMoves = True
                        lastClickedRedPiece = clickedSquare
                        redrawBoard()
                        for validSquare in activePieceMoveList:
                            drawPiece(moveMarkerImg, validSquare)

    #update display
    pygame.display.flip()
pygame.quit()

