import numpy as np
import time



class PuzzleGame:
    size = 4
    mat = [[1, 2, 3, 4], [0, 5, 7, 8], [10, 6, 11, 12] , [9, 13, 14, 15]]
    goal = [[ 1, 2, 3, 4], [ 5, 6, 7, 8], [ 9, 10, 11, 12], [ 13, 14, 15, 0]]
    lst = np.arange(size*size)
    limit = 0
    emptyTilePosition = [2,1]
    def __init__(self, mat=0, size=0):
        if size >= 3:
            self.size = size
            self.mat = mat
        elif size <3 and size >=1:
            print("Not Possible to make this PuzzleGame")
        
        # self.showMatrix()
        self.makingList()
        self.findingEmptyTileRow()
        self.goal = self.convertToTuple(self.goal)
        # self.showList()

    def makingList(self):
        count = 0
        for i in self.mat:
            for j in i:
                self.lst[count] = j
                count += 1
    
    def showList(self):
        print(self.lst)
    

    def showMatrix(self):
        flag = 0
        for i in self.mat:
            if len(i) != self.size:
                flag += 1
            print(i)
        if flag != 0:
            print("Row Column mismatch")
    
    def isSolvable(self):
        if self.size%2 == 1:
            inversions = self.checkingInversion()
            if inversions%2 == 0:
                print("Puzzle is Solvable")
            else:
                print("Puzzle is not Solvable")
        else:
            inversions = self.checkingInversion()
            self.findingEmptyTileRow()

            if (inversions%2 == 1 and self.emptyTilePosition[0]%2 == 0) or (inversions%2 == 0 and self.emptyTilePosition[0]%2 == 1):
                print("Inversion: ",inversions)
                print("Empty tile row from top :", self.emptyTilePosition)
                print("Puzzle is Solvable")
            else:
                print("Inversion: ",inversions)
                print("Empty tile row from top :", self.emptyTilePosition)
                print("Puzzle is not solvable")
    
    
    
    def checkingInversion(self):
        count = 0
        for i in range(0,15):
            for j in range(i+1, 16):
                if self.lst[i] > self.lst[j] and self.lst[j] != 0:
                    count += 1
        return count

    def findingEmptyTileRow(self):
        count = 0
        for i in self.mat:
            if 0 in i:
                count
                self.emptyTilePosition[0] = count
                for j in range(0, self.size):
                    if i[j] == 0:
                        self.emptyTilePosition[1] = j
                break
            count += 1


    def moveLeft(self): # move empty block left
        try:
            if self.emptyTilePosition[1] != 0:
                tmp = self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]-1]
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]-1] = 0
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]] = tmp
                self.emptyTilePosition = [self.emptyTilePosition[0], self.emptyTilePosition[1]-1]
        except IndexError:
            pass
    
    
    def moveRight(self):   # move empty block right
        try:
            if self.emptyTilePosition[1] != self.size-1:
                tmp = self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]+1]
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]+1] = 0
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]] = tmp
                self.emptyTilePosition = [self.emptyTilePosition[0], self.emptyTilePosition[1]+1]
        except IndexError:
            pass

    def moveDown(self):  # move empty block down
        try:
            if self.emptyTilePosition[0] != self.size-1:
                tmp = self.mat[self.emptyTilePosition[0]+1][self.emptyTilePosition[1]]
                self.mat[self.emptyTilePosition[0]+1][self.emptyTilePosition[1]] = 0
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]] = tmp
                self.emptyTilePosition = [self.emptyTilePosition[0]+1, self.emptyTilePosition[1]]
        except IndexError:
            pass


    def moveUp(self): # move empty block up
        try:
            if self.emptyTilePosition[0] != 0:
                tmp = self.mat[self.emptyTilePosition[0]-1][self.emptyTilePosition[1]]
                self.mat[self.emptyTilePosition[0]-1][self.emptyTilePosition[1]] = 0
                self.mat[self.emptyTilePosition[0]][self.emptyTilePosition[1]] = tmp
                self.emptyTilePosition = [self.emptyTilePosition[0]-1, self.emptyTilePosition[1]]
        except IndexError:
            pass

    def convertToTuple(self, arr):
        result = []
        for i in arr:
            result.append(tuple(i))
        return tuple(result)


    def match(self, copy):
        a = PuzzleGame()
        a.mat = copy
        for row in range(0, 4):
            for col in range(0, 4):
                if a.mat[row][col] == 0:
                    a.emptyTilePosition = [row, col]
        result = []
        for i in a.mat:
            result.append(list(i))
        a.mat = result
        return a



    def solve(self):
        start = self.convertToTuple(self.mat)
        visited = []
        queue = []
        pred = {}
        queue.append(start)
        count = 1

        while len(queue) > 0:
            tmp = queue.pop()

            print(tmp)
            


            if tmp == self.goal:
                path = []
                while tmp != start:
                    path.append(pred[tmp][1])
                    tmp = pred[tmp][0]
                return path[::-1]
            if count == 2:
                count = 1
                self.limit = 1

            if self.limit <= 2:

                if tmp not in visited:
                    visited.append(tmp)
                    tmpboard = self.match(tmp)

                    tmpboard.moveUp()
                    if self.convertToTuple(tmpboard.mat) != tmp:
                        queue.append(self.convertToTuple(tmpboard.mat))
                        if self.convertToTuple(tmpboard.mat) not in pred.keys():
                            pred[self.convertToTuple(tmpboard.mat)]=[tmp, 'up']

                    

                    tmpboard = self.match(tmp)
                    tmpboard.moveDown()
                    if self.convertToTuple(tmpboard.mat) != tmp:
                        queue.append(self.convertToTuple(tmpboard.mat))
                        if self.convertToTuple(tmpboard.mat) not in pred.keys():
                            pred[self.convertToTuple(tmpboard.mat)]=[tmp, 'down']


                    tmpboard = self.match(tmp)
                    tmpboard.moveRight()
                    if self.convertToTuple(tmpboard.mat) != tmp:
                        queue.append(self.convertToTuple(tmpboard.mat))
                        if self.convertToTuple(tmpboard.mat) not in pred.keys():
                            pred[self.convertToTuple(tmpboard.mat)]=[tmp, 'right']


                    tmpboard = self.match(tmp)
                    tmpboard.moveLeft()
                    if self.convertToTuple(tmpboard.mat) != tmp:
                        queue.append(self.convertToTuple(tmpboard.mat))
                        if self.convertToTuple(tmpboard.mat) not in pred.keys():
                            pred[self.convertToTuple(tmpboard.mat)]=[tmp, 'left']
                
                self.limit += 1
            else:
                self.limit = self.limit - count
                count += 1

        raise Exception('There is no solution.')


    def applyLst(self, lst):
        for i in lst:
            if i == 'right':
                self.moveRight()
            if i == 'left':
                self.moveLeft()
            if i == 'down':
                self.moveDown()
            if i == 'up':
                self.moveUp()

if __name__ == "__main__":
    g1 = PuzzleGame()
    g1.isSolvable()
    lst = g1.solve()
    print(lst)
    g1.applyLst(lst)
    g1.showMatrix()