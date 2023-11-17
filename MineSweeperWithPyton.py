
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
        """Sets a Cell to visible state and returns True when it could do it and False otherwise"""
        if self.visible:
            return False
        else:
            self.visible = True
            return True
    
    def isVisible(self):
        return self.visible
    
    def swapVisible(self):
        """Swaps the value of visible"""
        self.visible = not self.visible
            
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
        placedMines = 0
        while placedMines < mines:
            row = random.randint(0, rows - 1)
            column = random.randint(0, columns - 1)
            if self.cells[row][column].value != 9:  # Only set if it's not already a mine
                self.cells[row][column].value = 9
                placedMines += 1
            
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
            self.remainingCoveredCells = value
        
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
        self.board = None
        self.startTimer = None
        self.buttons = None
        self.labels = None
    
    def requestInfo(self, info_type):
        return tkinter.simpledialog.askstring("Minesweeper", "Enter " + str(info_type) + ":")
    
    def save(self):
        gameDict = {"Board": self.board, "Time": self.getTime(), "Player": self.player}
        try:
            with open(self.player.getFileName(), "wb") as f:
                pickle.dump(gameDict, f)
            return True
        except Exception as e:
            print("save exception: " + str(e))
            return False

    def newGame(self, dim1 = 14, dim2 = 18, mines = 40):
        self.board = Board(dim1, dim2, mines)
        self.board.setBoard()
        self.startTimer = time.time()

    def load(self, fileName):
        try:
            with open(fileName, "rb") as f:
                gameDict = pickle.load(f)
                if gameDict["Board"] is not None:
                    self.board = gameDict["Board"]
                if gameDict["Time"] is not None:
                    self.startTimer = time.time() - gameDict["Time"]
                self.player = gameDict["Player"]
            return True
        except Exception as e:
            print("load exception: " + str(e))
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
        except Exception as e:
            print("reset exception: " + str(e))
            return False
        
    def showAllCells(self):
        try:
            for row in range(self.board.getRows()):
                for column in range(self.board.getColumns()):
                    if self.board.getCell(row, column).isVisible():
                        continue
                    self.board.getCell(row, column).setVisible()
                    self.buttons[row][column].destroy()
                    self.setLabel(row, column)
            return True
        except Exception as e:
            print("sowAllCells exception: " + str(e))
            return False
    
    def end(self):
        try:
            self.showAllCells()
            self.board = None
            self.save()
            return True
        except Exception as e:
            print("end exception:" + str(e))
            return False
        
    def youLoose(self):
        self.end()
        tkinter.messagebox.showinfo("Game over","You lost!!!")
        
    def youWin(self):
        if self.player.getRecord() is None or self.getTime() < self.player.getRecord():
            self.player.setRecord(self.getTime())
            tkinter.messagebox.showinfo("Game over","You Win!!!\nYour new record is: " + str(round(self.getTime())))
        else:
            tkinter.messagebox.showinfo("Game over","You Win!!!")
        self.end()
        
        
    def rightClick(self, row, column):
        self.buttons[row][column].unbind('<Button-1>')
        self.buttons[row][column].configure(bg="red")
        self.buttons[row][column].bind('<Button-3>', lambda event, row=row, column=column: self.secondRightClick(row, column))
        
    def secondRightClick(self, row, column):
        self.buttons[row][column].bind('<Button-1>', lambda event, row=row, column=column: self.doMove(row, column))
        self.buttons[row][column].bind('<Button-3>', lambda event, row=row, column=column: self.rightClick(row, column))
        self.buttons[row][column].configure(bg="SystemButtonFace")
        
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
        
    def requestDim(self, dim):
        dimStr = self.requestInfo(dim)
        if not dimStr.isnumeric():
            tkinter.messagebox.showinfo("Wrong input","Please enter a number.")
            return self.requestDim(dim)
        elif int(dimStr) < 2 or int(dimStr) > 30:
            tkinter.messagebox.showinfo("Wrong input","Please enter a number between 2 and 30.")
            return self.requestDim(dim)
        else:
            return int(dimStr)
        
    def requestMines(self, rows, columns):
        minesStr = self.requestInfo("Mines")
        if not minesStr.isnumeric():
            tkinter.messagebox.showinfo("Wrong input","Please enter a number.")
            return self.requestMines(rows, columns)
        elif int(minesStr) < 1 or int(minesStr) > rows * columns - 1:
            tkinter.messagebox.showinfo("Wrong input","Please enter another number.")
            return self.requestMines(rows, columns)
        else:
            return int(minesStr)
        
    def gameLoop(self):
        window = tkinter.Tk()
        
        playerName = self.requestInfo("Name")
        
        if os.path.exists(playerName + ".msg"):
            if self.load(playerName + ".msg"):
                print("Game loaded succesfully. Player's name: {}".format(self.player.getName()))
            else:
                rows = self.requestDim("Rows")
                columns = self.requestDim("Columns")
                mines = self.requestMines(rows, columns)
                
        if self.player is None:
            self.player = Player(playerName)
            
        if self.board is None:
            self.newGame(rows, columns, mines)
            
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