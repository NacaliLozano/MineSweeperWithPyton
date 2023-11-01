
import tkinter
import tkinter.simpledialog
import random
import time
import pickle
import os


class Cell:
    def __init__(self, row, column):
        """Creates a Cell"""
        self.value = 0
        self.visible = False
        self.row = row
        self.column = column
        
    def setValue(self, value):
        """Sets the value of a Cell"""
        try:
            self.value = value
            return True
        except:
            return False
        
    def getValue(self):
        return self.value
    
    def setVisible(self):
        """Sets a Cell to visible state"""
        if self.visible:
            return False
        try:
            self.visible = True
            return True
        except:
            return False
    
    def isVisible(self):
        return self.visible
    
    def swapVisible(self):
        """Swaps the value of visible"""
        try:
            self.visible = not self.visible
            return True
        except:
            return False
        
class Board:
    def __init__(self, rows, columns, mines):
        """Initializes an empty board and sets the mines"""
        if mines >= rows * columns:
            return
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.remainingCoveredCells = rows * columns
        self.cells = []
        for row in range(rows):
            self.cells.append([])
            for column in range(columns):
                self.cells[row].append(Cell(row, column))
        #Set mines
        for mine in range(mines):
            row = random.randint(0, rows -1)
            column = random.randint(0, columns - 1)
            while self.cells[row][column].value >= 9:
                row = random.randint(0, rows -1)
                column = random.randint(0, columns - 1)
            self.cells[row][column].value = 9
            
    def setBoard(self):
        """Sets the values of the cells with a mine nearby"""
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].getValue() >= 9:
                    for incrementRows in [-1, 0, 1]:
                        for incrementColumns in [-1, 0, 1]:
                            if row + incrementRows in range(self.rows) and column + incrementColumns in range(self.columns):
                                if incrementRows == 0 and incrementColumns == 0:
                                    continue
                                self.cells[row + incrementRows][column + incrementColumns].setValue(self.cells[row + incrementRows][column + incrementColumns].getValue() + 1)
        return self
    
    def getCell(self, row, column):
        return self.cells[row][column]
    
    def getRows(self):
        return self.rows
    
    def getColumns(self):
        return self.columns
    
    def getMines(self):
        return self.mines
    
    def getRemainingCoveredCells(self):
        return self.remainingCoveredCells
    
    def setRemainingCoveredCells(self, value):
        try:
            self.remainingCoveredCells = value
            return True
        except:
            return False

        
class Player:
    def __init__(self, name):
        self.name = name
        self.fileName = self.name + ".msg" #MineSweeper Game
        self.record = None
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getRecord(self):
        return self.record
    
    def setRecord(self, record):
        self.record = record
        
    def getFileName(self):
        return self.fileName

class Game:
    def __init__(self):
        self.player = None
        self.board = Board(14, 18, 1)
        self.startTimer = None
        self.buttons = None
        self.labels = None
    
    def requestName(self):
        return tkinter.simpledialog.askstring("Minesweeper", "Enter your name:")
    
    def save(self):
        gameDict = {"Board": self.board, "Time": self.getTime(), "Player": self.player}
        try:
            with open(self.player.getFileName(), "wb") as f:
                f.pickle.dump(gameDict, f)
            return True
        except Exception as e:
            print(e)
            return False

    def newGame(self):
        try:
            self.board = Board(14, 18, 1)
            self.board.setBoard()
            self.startTimer = time.time()
            return True
        except:
            return False

    def load(self, fileName):
        try:
            with open(fileName, "rb") as f:
                gameDict = pickle.load(f)
                if gameDict["Board"] == None:
                    self.newGame()
                else:
                    self.board = gameDict["Board"]
                    self.startTimer = time.time() - gameDict["Time"]
                self.player = gameDict["Player"]
            return True
        except:
            return False
    
    def getPlayer(self):
        return self.player
    
    def getTime(self):
        return time.time() - self.startTimer
    
    def getBoard(self):
        return self.board
    
    def doMove(self, row, column):
        """Flips a Cell and neighbour cells"""
        if self.board is None:
            return
        #Return early if the cell is already visible
        if self.board.getCell(row, column).isVisible():
            return
        #Return early if stepped on a mine
        if self.board.getCell(row, column).getValue() >= 9:
            self.youLoose()
            return
        #Set Cell to visible
        self.board.getCell(row, column).setVisible()
        self.buttons[row][column].destroy()
        self.setLabel(row, column)
        #Decrement RemainingCoveredCells
        self.board.setRemainingCoveredCells(self.board.getRemainingCoveredCells() - 1)
        #Return if player won
        if self.board.getRemainingCoveredCells() == self.board.getMines():
            self.youWin()
            return
        #Trigger neighbour cells
        if self.board.getCell(row, column).getValue() == 0:
            for incrementRows in [-1, 0, 1]:
                for incrementColumns in [-1, 0, 1]:
                    if self.board is None:
                        break
                    if row + incrementRows in range(self.board.getRows()) and column + incrementColumns in range(self.board.getColumns()):
                        if incrementRows == 0 and incrementColumns == 0:
                            continue
                        self.doMove(row + incrementRows, column + incrementColumns)
        if self.save():
            print("Saved")
        else:
            print("Failed to save")
    
    def reset(self):
        try:
            self.board = Board(self.board.getRows(), self.board.getColumns(), self.board.getMines())
            self.startTimer = time.time()
            return True
        except:
            return False
        
    def showAllCells(self):
        try:
            for row in range(self.board.getRows()):
                for column in range(self.board.getColumns()):
                    if self.board.getCell[row][column].isVisible():
                        continue
                    self.board.getCell[row][column].setVisible()
                    self.buttons[row][column].destroy()
                    self.setLabel(row, column)
            return True
        except:
            return False
    
    def end(self):
        try:
            self.showAllCells()
            self.board = None
            self.save()
            return True
        except:
            return False
        
    def youLoose(self):
        self.end()
        tkinter.messagebox.showinfo("Game over","You lost!!!")
        
    def youWin(self):
        if self.player.getRecord() is None or self.getTime() - self.startTimer < self.player.getRecord():
            self.player.setRecord(self.getTime())
        self.end()
        tkinter.messagebox.showinfo("Game over","You Win!!!")
        
    def rightClick(self, row, column):
        self.board.getCell(row, column).button.unbind('<Button-1>')
        self.board.getCell(row, column).button.configure(bg="red")
        self.board.getCell(row, column).button.bind('<Button-3>', lambda event, row=row, column=column: self.secondRightClick(row, column))
        
    def secondRightClick(self, row, column):
        self.board.getCell(row, column).button.bind('<Button-1>', lambda event, row=row, column=column: self.doMove(row, column))
        self.board.getCell(row, column).button.bind('<Button-3>', lambda event, row=row, column=column: self.rightClick(row, column))
        self.board.getCell(row, column).button.configure(bg="SystemButtonFace")
        
    def setLabel(self, row, column):
        """Sets a label"""
        cellValue = self.board.getCell(row, column).getValue()
        if cellValue >= 9:
            self.labels[row][column] = tkinter.Label(text = "X", height = 1, width = 1)
        elif cellValue > 0:
            self.labels[row][column] = tkinter.Label(text = str(cellValue), height = 1, width = 1)
        else:
            self.labels[row][column] = tkinter.Label(text = "", height = 1, width = 1)
        self.labels[row][column].grid(row = row, column = column)
        
    def gameLoop(self):
        window = tkinter.Tk()
        playerName = self.requestName()
        if os.path.exists(playerName + ".msg"):
            if self.load(playerName + ".msg"):
                print("Game loaded succesfully. Player's name: {}".format(self.player.getName()))
            else:
                print("Game load failed")
        if self.player is None:
            self.player = Player(playerName)
        if self.board is None:
            if self.newGame():
                print("New game loaded")
            else:
                print("New game load failed")
        if self.startTimer is None:
            self.startTimer = time.time()
        
        self.labels = []
        self.buttons = []
        for row in range(self.board.getRows()):
            self.labels.append([])
            self.buttons.append([])
            for column in range(self.board.getColumns()):
                if self.board.getCell(row, column).isVisible():
                    self.labels[row].append(None)
                    self.buttons[row].append(None)
                    self.setLabel(row, column)
                else:
                    self.labels[row].append(None)
                    self.buttons[row].append(tkinter.Button(window, height = 1, width = 1))
                    self.buttons[row][column].grid(row = row, column = column)
                    self.buttons[row][column].bind('<Button-1>', lambda event, row = row, column = column: self.doMove(row, column))
                    self.buttons[row][column].bind('<Button-3>', lambda event, row = row, column = column: self.rightClick(row, column))
                
        window.mainloop()
        
if __name__ == "__main__":
    game = Game()
    game.gameLoop()