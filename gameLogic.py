from argparse import Action
import random
#CONSTANTS & VARIABLES
TILE_SIZE = 80
EMPTY = 0
RED = 1
REDKING = 2
WHITE = 3
WHITEKING = 4
#nA == number of usable squares * maximum number of moves per square(disregarding borders)



class Game:

    def __init__(self):
        #turn counter
        self.turnCounter = 0
        #2-dimensional array storing piece locations
        self.boardArr = [[EMPTY] * 8 for _ in range(8)]
            #last clicked red piece
        self.activePiece = (0,0)
        self.activePieceMoveList = []
        self.nA = 256
        self.aiMissedGuesses = 0
        self.aiCorrectGuesses = 0
        
    #get a copy of boardArr
    def getStateCopy(self):
        copyArr = [[EMPTY] * 8 for _ in range(8)]
        for x in range(8):
            copyArr[x] = tuple(self.boardArr[x])
        return tuple(copyArr)

    #translates an int (0 - 255) into a tuple (origin, destination)
    def action_from_index(self, actionIndex):
        
        originIndex = actionIndex%32
        moveDirection = actionIndex//32
        origin: tuple = (0,0)
        destination: tuple = (0,0)
        #get board coordinates from originIndex
        x = originIndex//8
        y = originIndex - x*8
        if y%2==0:
            x = x*2
            x += 1
        else:
            x *= 2
        origin = (x,y)

        #get move direction
        if moveDirection == 0:
            destination = self.getRightDiagPos(origin)
        elif moveDirection == 1:
            destination = self.getRightDiagPos(self.getRightDiagPos(origin))
        elif moveDirection == 2:
            destination = self.getBottomRightPos(origin)
        elif moveDirection == 3:
            destination = self.getBottomRightPos(self.getBottomRightPos(origin))
        elif moveDirection == 4:
            destination = self.getBottomLeftPos(origin)
        elif moveDirection == 5:
            destination = self.getBottomLeftPos(self.getBottomLeftPos(origin))
        elif moveDirection == 6:
            destination = self.getLeftDiagPos(origin)
        elif moveDirection == 7:
            destination = self.getLeftDiagPos(self.getLeftDiagPos(origin))
        return ((x,y), destination)

        

    def reset(self):
        self.turnCounter = 0
        self.boardArr = [[EMPTY] * 8 for _ in range(8)]
        #Set up board
        for x in range(8):
            for y in range(3):
                if x % 2 == 0 and y % 2 != 0:
                    self.boardArr[x][y] = WHITE
                elif x % 2 != 0 and y % 2 == 0:
                    self.boardArr[x][y] = WHITE
            
        for x in range(8):
            for y in range(5,8):
                if x % 2 == 0 and y % 2 != 0:
                    self.boardArr[x][y] = RED
                elif x % 2 != 0 and y % 2 == 0:
                    self.boardArr[x][y] = RED
        return self.boardArr
    
            
    """
    boardArr[2][3] = WHITE
    boardArr[2][5] = RED
    boardArr[0][5] = RED
    """
    #METHODS
        #Random AI turn logic, returns -1 if AI wins
    def randomBotTurn(self):
        self.turnCounter += 1
        reward = 0
        self.reverseBoard()
        #get number of possible moves
        availableMoves, numberOfMoves = self.getAllAvailableMoves()
        random.seed()
        randomMoveIndex = random.randint(0, numberOfMoves - 1)
        counter = 0
        for piece in availableMoves:
            for destination in piece[1]:
                if counter == randomMoveIndex:
                    #take action and retrieve reward if game is won
                    reward, done = self.makeMove((piece[0], destination))
                    self.reverseBoard()
                    reward *= -1
                    return reward
                else:
                    counter += 1

    #can the passed action ((x,y),(x,y)) be taken?
    def isActionValid(self, action):
        possibleActions, nrOfPossibleActions = self.getAllAvailableMoves()
        #print(nrOfPossibleActions, "available moves, ", action, " action attempted")
        for piece in possibleActions:
            if piece[0] == action[0]:
                for destination in piece[1]:
                    if action[1] == destination:
                        self.aiCorrectGuesses += 1
                        return True
        self.aiMissedGuesses += 1
        return False

    #modifies boardArr when move is made. If the move wins the game, returns a reward
    #returns (reward, wasActionTaken)
    def makeMove(self, action):
        captured = False
        #get action tuple ((originX,originY), (destinationX, destinationY))
        if(self.isActionValid(action)):
            origin = action[0]
            destination = action[1]
            if destination[1] == 0:
                self.boardArr[destination[0]][destination[1]] = REDKING
            else:
                self.boardArr[destination[0]][destination[1]] = self.getPiece(origin)
            self.boardArr[origin[0]][origin[1]] = EMPTY
            captured = self.removeIfAttack(origin, destination)
            #if current player won
            if self.didOpponentLose():
                return 10, True
            #if piece was captured
            elif captured:
                return 1, True
            #if normal move
            else:
                return 0, True
        #if no action taken
        else:
            return 0, False
    

        #reverse board and colors for AI
    def reverseBoard(self):
        #switch colors
        for x in range(8):
            for y in range(8):
                piece = self.getPiece((x,y))
                if piece == RED:
                    self.boardArr[x][y] = WHITE
                elif piece == REDKING:
                    self.boardArr[x][y] = WHITEKING
                elif piece == WHITE:
                    self.boardArr[x][y] = RED
                elif piece == WHITEKING:
                    self.boardArr[x][y] = REDKING
        #flip board
        self.boardArr.reverse()
        for row in self.boardArr:
            row.reverse()
        #if move was an attack, remove attacked piece

    def removeIfAttack(self, origin, destination):
        if abs(origin[1] - destination[1]) > 1:
            self.boardArr[(origin[0] + destination[0])//2][(origin[1] + destination[1])//2] = EMPTY
            return True
        
        #get squares at diagonal of arg position
    def getRightDiagPos(self, position):
        return (position[0] + 1, position[1] - 1)
    def getLeftDiagPos(self, position):
        return (position[0] - 1, position[1] - 1)
    def getBottomLeftPos(self, position):
        return(position[0] - 1, position[1] + 1)
    def getBottomRightPos(self, position):
        return(position[0] + 1, position[1] + 1)
    
    #returns list of tuples -> (origin: (x,y),destinations: list<(x, y)>, attackAvailable: boolean) for each red piece
    #also returns number of possible moves (for AI use)
    def getAllAvailableMoves(self):
        noOfMoves = 0
        resultList = []
        permitAttacksOnly = False
        #1st pass - append result list with every piece's options, regardless of whether attack is available
        for x in range(8):
            for y in range(8):
                if(self.getPiece((x,y)) == RED or self.getPiece((x,y)) == REDKING):
                    validMoves, attackMoveAvailable = self.getValidMoves((x,y))
                    if len(validMoves) != 0:
                        if attackMoveAvailable:
                            permitAttacksOnly = True
                        resultList.append(((x,y), validMoves, attackMoveAvailable))
                        noOfMoves += len(validMoves)

        #2nd pass - prepare a new list containing only attacking pieces
        if permitAttacksOnly:
            noOfMoves = 0
            tempList = []
            for element in resultList:
                #if has attack moves
                if element[2]:
                    tempList.append(element)
                    noOfMoves += len(element[1])
            resultList = tempList
        return resultList, noOfMoves
    #returns a list of eligible moves for this piece, returns empty list if no moves available
    def getMovesForPiece(self, position):
        allAvailableMoves, numberOfMoves = self.getAllAvailableMoves()
        for element in allAvailableMoves:
            if element[0] == position:
                return element[1]
        return []
        # -returns list of valid moves for arg position
        # -assumes there is a RED piece on position
    def getValidMoves(self, position):
        isKing = True if self.getPiece(position)==REDKING else False
        attackMoveAvailable = False
        atLeftExtremum = True
        atRightExtremum = True
        validMoveArray = []
            #if not at left extremum, check move options on left
        if self.getLeftDiagPos(position)[0] != -1 :
            atLeftExtremum = False
            if self.getLeftDiagPos(position)[1] != -1:
                    #if left attack available
                if self.getLeftDiagPos(self.getLeftDiagPos(position))[0] != -1 and self.getPiece(self.getLeftDiagPos(self.getLeftDiagPos(position))) == EMPTY and (
                    self.getPiece(self.getLeftDiagPos(position)) == WHITE or self.getPiece(self.getLeftDiagPos(position)) == WHITEKING):
                    validMoveArray.append(self.getLeftDiagPos(self.getLeftDiagPos(position)))
                    attackMoveAvailable = True
            #if not at right extremum...
        if self.getRightDiagPos(position)[0] != 8:
            atRightExtremum = False
            if self.getRightDiagPos(position)[1] != -1:
                    #if right attack available
                if self.getRightDiagPos(self.getRightDiagPos(position))[0] != 8 and self.getPiece(self.getRightDiagPos(self.getRightDiagPos(position))) == EMPTY and (
                    self.getPiece(self.getRightDiagPos(position)) == WHITE or self.getPiece(self.getRightDiagPos(position)) == WHITEKING):
                    validMoveArray.append(self.getRightDiagPos(self.getRightDiagPos(position)))
                    attackMoveAvailable = True
        #if KING and not at bottom row
        if isKing and position[1] != 7:
            if not atRightExtremum and self.getBottomRightPos(position)[0] != 7 and self.getBottomRightPos(position)[1] != 7:
                #if bottom right attack available
                if self.getBottomRightPos(self.getBottomRightPos(position))[0] != 8 and self.getPiece(
                    self.getBottomRightPos(self.getBottomRightPos(position))) == EMPTY and (
                    self.getPiece(self.getBottomRightPos(position)) == WHITE or self.getPiece(self.getBottomRightPos(position)) == WHITEKING):
                    validMoveArray.append(self.getBottomRightPos(self.getBottomRightPos(position)))
                    attackMoveAvailable = True
            if not atLeftExtremum and self.getBottomLeftPos(position)[0] != -1 and self.getBottomLeftPos(position)[1] != 7:
                #if bottom left attack available
                if self.getBottomLeftPos(self.getBottomLeftPos(position))[0] != -1 and self.getPiece(self.getBottomLeftPos(self.getBottomLeftPos(position))) == EMPTY and (
                    self.getPiece(self.getBottomLeftPos(position)) == WHITE or self.getPiece(self.getBottomLeftPos(position)) == WHITEKING):
                    validMoveArray.append(self.getBottomLeftPos(self.getBottomLeftPos(position)))
                    attackMoveAvailable = True
        if not attackMoveAvailable:
            #right up move
            if not atRightExtremum:
                if self.getPiece(self.getRightDiagPos(position)) == EMPTY:
                    validMoveArray.append(self.getRightDiagPos(position))
            #left up move
            if not atLeftExtremum:
                if self.getPiece(self.getLeftDiagPos(position)) == EMPTY:
                    validMoveArray.append(self.getLeftDiagPos(position))
            #king move
            if isKing:
                if position[1] != 7:
                    if self.getBottomRightPos(position)[0] != 8 and self.getPiece(self.getBottomRightPos(position)) == EMPTY:
                        validMoveArray.append(self.getBottomRightPos(position))
                    if self.getBottomLeftPos(position)[0] != -1 and self.getPiece(self.getBottomLeftPos(position)) == EMPTY:
                        validMoveArray.append(self.getBottomLeftPos(position))
        return validMoveArray, attackMoveAvailable
        
    def getPiece(self, squareCoordinates):
        if self.boardArr[squareCoordinates[0]][squareCoordinates[1]] == WHITE:
            return WHITE
        elif self.boardArr[squareCoordinates[0]][squareCoordinates[1]] == RED:
            return RED
        elif self.boardArr[squareCoordinates[0]][squareCoordinates[1]] == EMPTY:
            return EMPTY
        elif self.boardArr[squareCoordinates[0]][squareCoordinates[1]] == WHITEKING:
            return WHITEKING
        elif self.boardArr[squareCoordinates[0]][squareCoordinates[1]] == REDKING:
            return REDKING

        #pass the position of a square from (0,0) to (7,7), get pixel coordinates back
    def getCoordinatesFromSquare(self, hor, ver):
        return (hor * TILE_SIZE + 8, ver * TILE_SIZE + 8)

    def getSquareFromCoordinates(self, mousePosition):
        return (mousePosition[0]//TILE_SIZE, mousePosition[1]//TILE_SIZE)
        #did current player lose? Should be called at the beginning of the current player's turn
    def didOpponentLose(self):
        self.reverseBoard()
        validMoves, numberOfMoves = self.getAllAvailableMoves()
        if numberOfMoves == 0:
            return True
        else:
            self.reverseBoard()
            return False

#END METHODS