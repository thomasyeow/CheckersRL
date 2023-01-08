import random
#CONSTANTS & VARIABLES
TILE_SIZE = 80
EMPTY = 0
RED = 1
REDKING = 2
WHITE = 3
WHITEKING = 4
    #2-dimensional array storing piece locations
boardArr = [[EMPTY] * 8 for _ in range(8)]
    
    #are eligible moves being shown?
showingValidMoves = False
    #last clicked red piece
activePiece = (0,0)

activePieceMoveList = []

#END CONSTANTS & VARIABLES

#Set up board

for x in range(8):
    for y in range(3):
        if x % 2 == 0 and y % 2 != 0:
            boardArr[x][y] = WHITE
        elif x % 2 != 0 and y % 2 == 0:
            boardArr[x][y] = WHITE
            """
for x in range(8):
    for y in range(5,8):
        if x % 2 == 0 and y % 2 != 0:
            boardArr[x][y] = RED
        elif x % 2 != 0 and y % 2 == 0:
            boardArr[x][y] = RED
            """

#boardArr[2][3] = WHITE
#boardArr[2][5] = RED
#boardArr[0][5] = RED

#METHODS
    #AI turn logic
def AiTurn():
    reverseBoard()
    #get number of possible moves
    availableMoves, numberOfMoves = getAllAvailableMoves()
    print("Number of available moves for AI", numberOfMoves)
    random.seed()
    randomMoveIndex = random.randint(0, numberOfMoves - 1)
    counter = 0
    for piece in availableMoves:
        for destination in piece[1]:
            if counter == randomMoveIndex:
                #take action
                if destination[1] == 0:
                    boardArr[destination[0]][destination[1]] = REDKING
                else:
                    boardArr[destination[0]][destination[1]] = getPiece(piece[0])
                boardArr[piece[0][0]][piece[0][1]] = EMPTY
                removeIfAttack(piece[0], destination)
                #pass to other player
                reverseBoard()
                counter = numberOfMoves
            else:
                counter += 1
    


    
    #reverse board and colors for AI
def reverseBoard():
    #switch colors
    for x in range(8):
        for y in range(8):
            piece = getPiece((x,y))
            if piece == RED:
                boardArr[x][y] = WHITE
            elif piece == REDKING:
                boardArr[x][y] = WHITEKING
            elif piece == WHITE:
                boardArr[x][y] = RED
            elif piece == WHITEKING:
                boardArr[x][y] = REDKING
    #flip board
    boardArr.reverse()
    for row in boardArr:
        row.reverse()
    #if move was an attack, remove attacked piece

def removeIfAttack(origin, destination):
    if abs(origin[1] - destination[1]) > 1:
        boardArr[(origin[0] + destination[0])//2][(origin[1] + destination[1])//2] = EMPTY
    #get squares at diagonal of arg position
def getRightDiagPos(position):
    return (position[0] + 1, position[1] - 1)
def getLeftDiagPos(position):
    return (position[0] - 1, position[1] - 1)
def getBottomLeftPos(position):
    return(position[0] - 1, position[1] + 1)
def getBottomRightPos(position):
    return(position[0] + 1, position[1] + 1)

#returns list containing tuple (origin: (x,y),destinations: list<(x, y)>, attackAvailable: boolean) for each red piece
#also returns number of possible moves (for AI use)
def getAllAvailableMoves():
    noOfMoves = 0
    resultList = []
    permitAttacksOnly = False
    #1st pass - append result list with every piece's options, regardless of whether attack is available
    for x in range(8):
        for y in range(8):
            if(getPiece((x,y)) == RED or getPiece((x,y)) == REDKING):
                validMoves, attackMoveAvailable = getValidMoves((x,y))
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
def getMovesForPiece(position):
    allAvailableMoves, numberOfMoves = getAllAvailableMoves()
    for element in allAvailableMoves:
        if element[0] == position:
            return element[1]
    return []
    # -returns list of valid moves for arg position
    # -assumes there is a RED piece on position
def getValidMoves(position):
    isKing = True if getPiece(position)==REDKING else False
    attackMoveAvailable = False
    atLeftExtremum = True
    atRightExtremum = True
    validMoveArray = []
        #if not at left extremum, check move options on left
    if getLeftDiagPos(position)[0] != -1 and getLeftDiagPos(position)[1] != -1:
        atLeftExtremum = False
            #if left attack available
        if getLeftDiagPos(getLeftDiagPos(position))[0] != -1 and getPiece(getLeftDiagPos(getLeftDiagPos(position))) == EMPTY and (
            getPiece(getLeftDiagPos(position)) == WHITE or getPiece(getLeftDiagPos(position)) == WHITEKING):
            validMoveArray.append(getLeftDiagPos(getLeftDiagPos(position)))
            attackMoveAvailable = True
        #if not at right extremum...
    if getRightDiagPos(position)[0] != 8 and getRightDiagPos(position)[1] != -1:
        atRightExtremum = False
            #if right attack available
        if getRightDiagPos(getRightDiagPos(position))[0] != 8 and getPiece(getRightDiagPos(getRightDiagPos(position))) == EMPTY and (
            getPiece(getRightDiagPos(position)) == WHITE or getPiece(getRightDiagPos(position)) == WHITEKING):
            validMoveArray.append(getRightDiagPos(getRightDiagPos(position)))
            attackMoveAvailable = True
    #if KING and not at bottom row
    if isKing and position[1] != 7:
        if not atRightExtremum and getBottomRightPos(position)[0] != 7 and getBottomRightPos(position)[1] != 7:
            #if bottom right attack available
            if getBottomRightPos(getBottomRightPos(position))[0] != 8 and getPiece(
                getBottomRightPos(getBottomRightPos(position))) == EMPTY and (
                getPiece(getBottomRightPos(position)) == WHITE or getPiece(getBottomRightPos(position)) == WHITEKING):
                validMoveArray.append(getBottomRightPos(getBottomRightPos(position)))
                attackMoveAvailable = True
        if not atLeftExtremum and getBottomLeftPos(position)[0] != -1 and getBottomLeftPos(position)[1] != 7:
            #if bottom left attack available
            if getBottomLeftPos(getBottomLeftPos(position))[0] != -1 and getPiece(getBottomLeftPos(getBottomLeftPos(position))) == EMPTY and (
                getPiece(getBottomLeftPos(position)) == WHITE or getPiece(getBottomLeftPos(position)) == WHITEKING):
                validMoveArray.append(getBottomLeftPos(getBottomLeftPos(position)))
                attackMoveAvailable = True
    if not attackMoveAvailable:
        #right up move
        if not atRightExtremum:
            if getPiece(getRightDiagPos(position)) == EMPTY:
                validMoveArray.append(getRightDiagPos(position))
        #left up move
        if not atLeftExtremum:
            if getPiece(getLeftDiagPos(position)) == EMPTY:
                validMoveArray.append(getLeftDiagPos(position))
        #king move
        if isKing:
            if position[1] != 7:
                if getBottomRightPos(position)[0] != 8 and getPiece(getBottomRightPos(position)) == EMPTY:
                    validMoveArray.append(getBottomRightPos(position))
                if getBottomLeftPos(position)[0] != -1 and getPiece(getBottomLeftPos(position)) == EMPTY:
                    validMoveArray.append(getBottomLeftPos(position))
    return validMoveArray, attackMoveAvailable
        
def getPiece(squareCoordinates):
    if boardArr[squareCoordinates[0]][squareCoordinates[1]] == WHITE:
        return WHITE
    elif boardArr[squareCoordinates[0]][squareCoordinates[1]] == RED:
        return RED
    elif boardArr[squareCoordinates[0]][squareCoordinates[1]] == EMPTY:
        return EMPTY
    elif boardArr[squareCoordinates[0]][squareCoordinates[1]] == WHITEKING:
        return WHITEKING
    elif boardArr[squareCoordinates[0]][squareCoordinates[1]] == REDKING:
        return REDKING

    #pass the position of a square from (0,0) to (7,7), get pixel coordinates back
def getCoordinatesFromSquare(hor, ver):
    return (hor * TILE_SIZE + 8, ver * TILE_SIZE + 8)

def getSquareFromCoordinates(mousePosition):
    return (mousePosition[0]//TILE_SIZE, mousePosition[1]//TILE_SIZE)
    #did current player lose? Should be called at the beginning of the current player's turn
def currentPlayerLost():
    
    validMoves, numberOfMoves = getAllAvailableMoves()
    if numberOfMoves == 0:
        return True
    

#END METHODS