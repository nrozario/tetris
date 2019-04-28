from tkinter import *
import random

# Defines the game dimensions and stores them inside gameDimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def init(data):
    data.rows = gameDimensions()[0]
    data.cols = gameDimensions()[1]
    data.cellSize = gameDimensions()[2]
    data.margin = gameDimensions()[3]
    data.emptyColor = "blue"
    data.score = 0
    board = []
    for row in range(data.rows):
        board += [[data.emptyColor] * data.cols]
    data.board = board

    iPiece = [
        [True, True, True, True]
    ]

    jPiece = [
        [True, False, False],
        [True, True, True]
    ]

    lPiece = [
        [False, False, True],
        [True, True, True]
    ]

    oPiece = [
        [True, True],
        [True, True]
    ]

    sPiece = [
        [False, True, True],
        [True, True, False]
    ]

    tPiece = [
        [False, True, False],
        [True, True, True]
    ]

    zPiece = [
        [True, True, False],
        [False, True, True]
    ]

    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan",
                              "green", "orange"]

    newFallingPiece(data)

    data.isGameOver = False

    pass

# Starts the tetris game
def playTetris():
    height = gameDimensions()[0] * gameDimensions()[2] + 2 * gameDimensions()[3]
    width = gameDimensions()[1] * gameDimensions()[2] + 2 * gameDimensions()[3]
    run(width, height)

# Draws a cell with given row, column, and color
def drawCell(canvas, data, row, col, color):
    canvas.create_rectangle(col * data.cellSize + data.margin, row * data.cellSize + data.margin, (col + 1) * data.cellSize + data.margin, (row + 1) * data.cellSize + data.margin, fill = color, width = data.cellSize / 5)

# Creates a randomly placed new falling piece when called
def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols // 2 - len(data.fallingPiece[0]) // 2

# Draws the randomly created piece created from newFallingPiece
def drawFallingPiece(canvas,data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]:
                drawCell(canvas, data, data.fallingPieceRow + i, data.fallingPieceCol + j, data.fallingPieceColor)

# Checks to see if the falling piece is within the game dimensions
def fallingPieceIsLegal(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if not (0 <= data.fallingPieceRow + i and data.fallingPieceRow + i < data.rows and 0 <= data.fallingPieceCol + j and data.fallingPieceCol + j < data.cols and (not data.fallingPiece[i][j] or data.board[i + data.fallingPieceRow][j + data.fallingPieceCol] == data.emptyColor)):
                return False
    return True

# Allows movement of the falling piece through key inputs
def moveFallingPiece(data,drow,dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

# Rotates the falling piece given the key input
def rotateFallingPiece(data):
    oldPiece = data.fallingPiece
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    oldNumRows = len(oldPiece)
    oldNumCols = len(oldPiece[0])
    newNumRows = oldNumCols
    newNumCols = oldNumRows
    newPiece = []
    for row in range(len(oldPiece[0])):
        newPiece += [[False] * len(oldPiece)]
    for i in range(len(oldPiece)):
        for j in range(len(oldPiece[0])):
            newPiece[j][i] = oldPiece[i][len(oldPiece[0]) - 1 - j]
    data.fallingPiece = newPiece

    oldCenterRow = oldRow + oldNumRows // 2
    newRow = oldRow + oldNumRows // 2 - newNumRows // 2

    oldCenterCol = oldCol + oldNumCols // 2
    newCol = oldCol + oldNumCols // 2 - newNumCols // 2

    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol

    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldPiece
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol

# Places the falling piece as part of the board after it can no longer move
def placeFallingPiece(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]:
                data.board[data.fallingPieceRow + i][data.fallingPieceCol + j] = data.fallingPieceColor
    newFallingPiece(data)
    removeFullRows(data)

# Removes a full row for any row of the board when detected
def removeFullRows(data):
    newBoard = []
    for row in range(data.rows):
        newBoard += [[data.emptyColor] * data.cols]
    rowCounter = 0
    currentRow = len(data.board) - 1
    for i in range(len(data.board) - 1, -1, -1):
        rowFull = True
        for j in range(len(data.board[0])):
            if data.board[i][j] == data.emptyColor:
                rowFull = False
        if rowFull == False:
            for j in range(len(data.board[0])):
                newBoard[currentRow][j] = data.board[i][j]
            currentRow -= 1
        else:
            rowCounter += 1
    data.score += rowCounter ** 2
    data.board = newBoard

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if not data.isGameOver:
        drow = 0
        dcol = 0
        if event.keysym == "Down":
            drow = 1
        elif event.keysym == "Left":
            dcol = -1
        elif event.keysym == "Right":
            dcol = 1
        elif event.keysym == "Up":
            rotateFallingPiece(data)
        moveFallingPiece(data, drow, dcol)
    else:
        if event.keysym == "r":
            init(data)
    pass

def timerFired(data):
    if not data.isGameOver:
        if not moveFallingPiece(data, +1, 0):
            if not fallingPieceIsLegal(data):
                data.isGameOver = True
            placeFallingPiece(data)

    pass

# Draws the board by iterating through the game dimensions and calling drawCell
def drawBoard(canvas,data):
    for i in range(gameDimensions()[0]):
        for j in range(gameDimensions()[1]):
            drawCell(canvas, data, i, j, data.board[i][j])

# Draws the player's score
def drawScore(canvas,data):
    canvas.create_text(data.width / 2, data.margin / 2,
                       text="Score: " + str(data.score), fill = "blue", font = "TimesNewRoman 12")

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if data.isGameOver:
        canvas.create_rectangle(data.margin, data.cellSize + data.margin, data.width - data.margin, data.margin + 3 * data.cellSize, fill = "black")
        canvas.create_text(data.width / 2, (data.cellSize * 2 + data.margin), text = "Game Over!", fill = "White", font = "TimesNewRoman 24")
    pass

def run(width = 300, height = 300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill = 'white', width = 0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width = False, height = False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width = data.width, height = data.height)
    canvas.configure(bd = 0, highlightthickness = 0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()