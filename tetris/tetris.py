import sys
import random
import os

from copy import deepcopy

BOARD_WIDTH=22
BOARD_LENGTH=21

PIECES = [
    [['*'],['*'],['*'],['*']],
    
    [['*',' '],
     ['*',' '],
     ['*','*']],
    
    [[' ','*'],
     [' ','*'],
     ['*','*']],

     [[' ','*'],
     ['*','*'],
     ['*',' ']],
     
     [['*','*'],
      ['*','*']]
]

EMPTY_ROW=['*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*']

def setupBoard():
    board = [ [' ' for x in range(BOARD_WIDTH)] for y in range(BOARD_LENGTH+1)]
   
    for i in range(BOARD_LENGTH):
        board[i][0]='*'
        board[i][BOARD_WIDTH-1]='*'
    
    for i in range(1,BOARD_WIDTH-1):
        board[BOARD_LENGTH-1][i] = '*'

    return board

def getPiece():
    index = random.randrange(len(PIECES))
    return PIECES[index]

def getPosition():
    x=random.randrange(1,19)
    return [0,x]

def printInstructions():
    print("How to play\n")
    print("a (return): move piece left")
    print("d (return): move piece right")
    print("w (return): rotate piece counter clockwise")
    print("s (return): rotate piece clockwise")
    print("q (return): quit game")

def printBoard(board,activePiece,piecePosition,score):
    os.system('cls' if os.name=='nt' else 'clear')
    print("TETRIS - console version")

    board_copy = deepcopy(board)
    piece_x = len(activePiece)
    piece_y = len(activePiece[0])

    for i in range(piece_x):
        for j in range(piece_y):
            if(board_copy[piecePosition[0]+i][piecePosition[1]+j] != '*'):
                board_copy[piecePosition[0]+i][piecePosition[1]+j]=activePiece[i][j]

    for i in range(BOARD_LENGTH):
        print(''.join(board_copy[:][i]))

    printInstructions()
    print("Your score: ",score)
    print("Next move: ")
    return board_copy

def getLeftMove(piecePosition):
    newPiecePos = [piecePosition[0], piecePosition[1] - 1]
    return newPiecePos

def getRightMove(piecePosition):
    newPiecePos = [piecePosition[0], piecePosition[1] + 1]
    return newPiecePos

def getDownMove(piecePosition):
    newPiecePos = [piecePosition[0] + 1, piecePosition[1]]
    return newPiecePos

def rotateClockwise(piece):
    pieceCopy = deepcopy(piece)
    rotatedPiece = [list(reversed(col)) for col in zip(*pieceCopy)]
    return rotatedPiece

def rotateAnticlockwise(piece):
    pieceCopy = deepcopy(piece)
    piece1 = rotateClockwise(pieceCopy)
    piece2 = rotateClockwise(piece1)
    return rotateClockwise(piece2)

def checkOverlap(board,piece,piecePosition):
    pieceX = len(piece)
    pieceY = len(piece[0])
    x=piecePosition[0]
    y=piecePosition[1]
    for i in range(pieceX):
        for j in range(pieceY):
            if (board[piecePosition[0]+i][piecePosition[1]+j] == '*' and piece[i][j] == '*'):
                return False
    return True

def checkLeftMove(board,piece,piecePosition):
    piecePosition = getLeftMove(piecePosition)
    return checkOverlap(board,piece,piecePosition)

def checkRightMove(board,piece,piecePosition):
    piecePosition = getRightMove(piecePosition)
    return checkOverlap(board,piece,piecePosition)

def checkDownMove(board,piece,piecePosition):
    piecePosition = getDownMove(piecePosition)
    return checkOverlap(board,piece,piecePosition)

def checkAnticlockwiseRotation(board,piece,piecePosition):
    piece = rotateAnticlockwise(piece)
    return checkOverlap(board,piece,piecePosition)

def checkClockwiseRotation(board,piece,piecePosition):
    piece = rotateClockwise(piece)
    return checkOverlap(board,piece,piecePosition)

def checkIfMovable(board,piece,piecePosition):
    leftFlag = checkLeftMove(board,piece,piecePosition)
    rightFlag = checkRightMove(board,piece,piecePosition)
    clkFlag = checkClockwiseRotation(board,piece,piecePosition)
    antclkFlag = checkAnticlockwiseRotation(board,piece,piecePosition)
    dwnFlag = checkDownMove(board,piece,piecePosition)
    return (leftFlag or rightFlag or clkFlag or antclkFlag or dwnFlag)

def cleanRow(board,score):
    rowsToClean=0
    
    board_copy=deepcopy(board)
    for i in range(BOARD_LENGTH-1):
        stars=0
        for j in range(BOARD_WIDTH):
            if(board[i][j] == '*'):
                stars+=1
        if(stars==22):
            rowsToClean+=1
    if(rowsToClean>0):
        i = BOARD_LENGTH-2
        while(i>=rowsToClean):
            for j in range(BOARD_WIDTH):
                board_copy[i][j]=board[i-1][j]
            i-=1
        for j in range(rowsToClean):
            board_copy[:][j]=EMPTY_ROW
    
    score+=(rowsToClean*100)
    return [board_copy,score]
        
    
    

def game():
    board = setupBoard()
    piece = getPiece()
    piecePosition=getPosition()
    endGame=False
    score=0
    
    temp=printBoard(board,piece,piecePosition,score)
    
    nextMove=input()
    
    if(nextMove=='a'):
        if(checkLeftMove(board,piece,piecePosition)):
            piecePosition=getLeftMove(piecePosition)
    elif(nextMove=='d'):
        if(checkRightMove(board,piece,piecePosition)):
            piecePosition=getRightMove(piecePosition)
    elif(nextMove=='w'):
        if(checkAnticlockwiseRotation(board,piece,piecePosition)):
            piece=rotateAnticlockwise(piece)
    elif(nextMove=='s'):
        if(checkClockwiseRotation(board,piece,piecePosition)):
            piece=rotateClockwise(piece)
    elif(nextMove=='q'):
        quit()

    if(checkDownMove(board,piece,piecePosition)):
        piecePosition=getDownMove(piecePosition)

    updateBoard=True
    movePiece=True

    while not endGame:
        if updateBoard:
            temp=printBoard(board,piece,piecePosition,score)
            
        nextMove=input()
        
        if(movePiece):

            updateBoard=True    
            if(nextMove=='a'):
                if(checkLeftMove(board,piece,piecePosition)):
                    piecePosition=getLeftMove(piecePosition)
                else:
                    updateBoard=False
                    print("Move not possible. Enter valid move")
            elif(nextMove=='d'):
                if(checkRightMove(board,piece,piecePosition)):
                    piecePosition=getRightMove(piecePosition)
                else:
                    updateBoard=False
                    print("Move not possible. Enter valid move")
            elif(nextMove=='w'):
                if(checkAnticlockwiseRotation(board,piece,piecePosition)):
                    piece=rotateAnticlockwise(piece)
                else:
                    updateBoard=False
                    print("Move not possible. Enter valid move")
            elif(nextMove=='s'):
                if(checkClockwiseRotation(board,piece,piecePosition)):
                    piece=rotateClockwise(piece)
                else:
                    updateBoard=False
                    print("Move not possible. Enter valid move")
            elif(nextMove=='q'):
                quit()

            if(checkDownMove(board,piece,piecePosition)):
                movePiece=True
                piecePosition=getDownMove(piecePosition)
            else:
                movePiece=False
        else:
            board=temp
            tmp=cleanRow(board,score)
            board=tmp[0]
            score=tmp[1]
            piece=getPiece()
            piecePosition=getPosition()
            movePiece=True
            if (not checkIfMovable(board,piece,piecePosition)):
                print("Game over")
                endGame=True

game()