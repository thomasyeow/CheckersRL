import pygame
import pickle
#custom library containing function and constant definitions, for tidyness
import numpy as np
from gameLogic import *
from agent import Agent
from collections import defaultdict
class CheckersSUML:
    #are eligible moves being shown?
    
    def __init__(self, game):
        #initialize pygame

        pygame.init()
        pygame.display.set_caption("Checkers RL")
        self.activePieceMoveList = []
        self.showingValidMoves = False
        self.lastClickedRedPiece = ()
        self.game = game
        #VARIABLES
        self.screen = pygame.display.set_mode((640,640))

            #import assets
        self.redPieceImg = pygame.image.load("assets/redPiece.png").convert()
        self.whitePieceImg = pygame.image.load("assets/whitePiece.png").convert()
        self.redKingImg = pygame.image.load("assets/redKingPiece.png").convert()
        self.whiteKingImg = pygame.image.load("assets/whiteKingPiece.png").convert()
        self.boardImg = pygame.image.load("assets/Board.png").convert()
        self.moveMarkerImg = pygame.image.load("assets/validMoveMarker.png").convert()

    #SHORTCUT FUNCTIONS
        #draw piece to position and update boardArr ONLY for the destination
    def drawPiece(self, pieceImg, position):
        self.screen.blit(pieceImg, self.game.getCoordinatesFromSquare(position[0], position[1]))

    def victoryLossScreen(self, won: bool):
        message = ""
        if won:
            message = "VICTORY"
        else:
            message = "LOSS"
        font = pygame.font.SysFont(None, 60)
        text = font.render(message, True, (255,0,60), (0,0,128))
        textRect = text.get_rect()
        textRect.center = (640//2, 640//2)
        self.screen.fill((255,255,255))
        self.screen.blit(text, textRect)

        #redraw the entire board based on boardArr
    def redrawBoard(self, game):
        self.screen.blit(self.boardImg, (0,0))
        for x in range(8):
            for y in range(8):
                if game.boardArr[x][y] == RED:
                    self.drawPiece(self.redPieceImg, (x, y))
                elif game.boardArr[x][y] == WHITE:
                    self.drawPiece(self.whitePieceImg, (x, y))
                elif game.boardArr[x][y] == REDKING:
                    self.drawPiece(self.redKingImg, (x, y))
                elif game.boardArr[x][y] == WHITEKING:
                    self.drawPiece(self.whiteKingImg, (x, y))

    def render(self, game):
        self.redrawBoard(game)
        pygame.display.flip()
    def quitCheck(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    game = Game()
    agent = Agent(game)
    render = CheckersSUML(game)
    game.reset()
    render.redrawBoard(game)
    #Game Loop
    running = True
    gameEnded = 0
    #get AI model
    filename = "checkersModel.pkl"
    unpickleFile = open(filename, 'rb')
    agent.q_table = pickle.load(unpickleFile)
    agent.q_table = defaultdict(lambda: np.zeros(256), agent.q_table)
    x = 5
    agent.epsilon = 0
    while(running):
        if gameEnded == -10:
            render.victoryLossScreen(False)
        elif gameEnded == 10:
            render.victoryLossScreen(True)
        else:
            for event in pygame.event.get():
                #QUIT
                if event.type == pygame.QUIT:
                    running = False
                #MOUSE DOWN - does nothing but debugging
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clickedSquare = game.getSquareFromCoordinates(event.pos)
                    print("Board at " , clickedSquare, " contains a ", "WHITE" if game.getPiece(
                        clickedSquare) == WHITE else "RED" if game.getPiece(clickedSquare) == RED else "EMPTY" if game.getPiece(
                            clickedSquare) == EMPTY else "REDKING" if game.getPiece(clickedSquare) == REDKING else "WHITEKING")
            
                #MOUSE UP
                elif event.type == pygame.MOUSEBUTTONUP:
                    clickedSquare = game.getSquareFromCoordinates(event.pos)
                    #if currently showing valid moves for some piece
                    if render.showingValidMoves:
                        for move in activePieceMoveList:
                            #if clicked on valid move square
                            if clickedSquare == move:
                                gameEnded, validMoveTaken = game.makeMove((render.lastClickedRedPiece, clickedSquare))
                                #if player hasn't won, AI turn
                                if gameEnded != 10:
                                    game.reverseBoard()
                                    gameEnded, validMoveTaken = game.makeMove(game.action_from_index(agent.get_action()))
                                    #if the q_table has no response to the gamestate, do random action
                                    if not validMoveTaken:
                                        game.reverseBoard()
                                        gameEnded = game.randomBotTurn()
                                        gameEnded *= -1
                                        game.reverseBoard()
                                    game.reverseBoard()
                                    gameEnded *= -1
                        render.redrawBoard(game)
                        render.showingValidMoves = False
                    else:
                        #if clicked on own piece
                        if game.getPiece(clickedSquare) == RED or game.getPiece(clickedSquare) == REDKING:
                            activePieceMoveList = game.getMovesForPiece(clickedSquare)
                            #if clicked piece has valid moves
                            if len(activePieceMoveList) != 0:
                                render.showingValidMoves = True
                                render.lastClickedRedPiece = clickedSquare
                                render.redrawBoard(game)
                                for validSquare in activePieceMoveList:
                                    render.drawPiece(render.moveMarkerImg, validSquare)
                                
        #update display
        pygame.display.flip()
    pygame.quit()
