import numpy as np
import random
# Enviroment Class.
# TODO: Implement the node based grid, where the building blocks can only be placed in predefined 'nodes', based on the gridsize.

class Enviroment:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.road = 1
        self.building = 2
        self.empty = 0
        self.inside = -1
        self.grid = np.zeros((gridSize, gridSize))
        # A seperate grid which keeps track of the locations where buildings cant be placed, since they would overlap with other buildings
        self.overlapGrid = np.zeros((gridSize, gridSize))
        self.buildingSize = 2  # This determines the wall thickness
        self.interiorSize = 3  # Determines how large the interior of each building is, in this case 3x3. Has to be an odd number, otherwise there is not a clear center
        self.roadSize = 1

    def BuildEnviroment(self):
        # TODO Check what is road and what is building to make a good approximation
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                r = random.random()
                if r < 0.5:
                    self.grid[i, j] = self.building
                else:
                    self.grid[i, j] = self.road

    def DeterministicEnviroment(self):
        # Fix different cells start with 9
        v1 = [0, 1, 2, 3, 6, 7, 8, 9]
        v2 = [3, 6]
        self.grid[:, :] = self.road
        for i in range(self.gridSize):
            if i in v1:
                self.grid[i, v2] = self.building
            if i in v2:
                self.grid[i, v1] = self.building

    # Each building takes a lot of space, about a 7x7 square on the grid.
    def PlaceBuildings(self, numberOfBuildings):
        cutOff = 700
        for i in range(numberOfBuildings):
            numberOfTries = 0
            if i == 0:
                randX = int((self.gridSize/2-1))
                randY = int((self.gridSize/2-1))
                self.PlaceSquareBuilding(cutOff,i,randX,randY)
                print('Building:',i, "placed at X=",randX,"Y=",randY)
            else:
                buildType = "square"
                locationsArray = np.where(self.overlapGrid == 1)
                while True:
                    numberOfTries = numberOfTries + 1
                    self.obstruction = 0 # This is a check for the system
                    newBuildIndex = np.random.randint(len(locationsArray[0][:]))
                    randX = locationsArray[0][newBuildIndex]
                    randY = locationsArray[1][newBuildIndex]
                    self.BuildingCheck("square",randX,randY)
                    if self.obstruction == 0:
                        if buildType == "square":
                            self.PlaceSquareBuilding(cutOff,i,randX,randY)
                            print('Building:',i, "placed at X=",randX,"Y=",randY)
                            break
                    elif numberOfTries == cutOff:
                        print("Could not place building")
                        break


    def PlaceSquareBuilding(self,cutOff, i,randX,randY):
        numberOfIterations = 0
        while True:
            numberOfIterations = numberOfIterations + 1
            if (self.overlapGrid[randX, randY] == 1 and numberOfIterations < cutOff) or (i == 0):
                for j in range(self.buildingSize*2 + self.interiorSize):
                    for k in range(self.buildingSize*2 + self.interiorSize):
                        if self.grid[randX - self.buildingSize + j - 1, randY - self.buildingSize+k-1] == 0 or self.grid[randX - self.buildingSize + j - 1, randY - self.buildingSize+k-1] == 2:
                            self.grid[randX - self.buildingSize + j - 1,
                                      randY - self.buildingSize+k-1] = self.building

                for j in range(self.interiorSize):
                    for k in range(self.interiorSize):
                        self.grid[randX + j - 1, randY + k - 1] = self.inside

                for j in range(self.buildingSize*2 + self.interiorSize + 2):
                    for k in range(self.buildingSize*2 + self.interiorSize + 2):
                        if randX - self.buildingSize + j - 2<=self.gridSize-1 and randY - self.buildingSize+k-2 <= self.gridSize -1 and self.grid[randX - self.buildingSize + j - 2, randY - self.buildingSize+k-2] == 0 :
                            self.grid[randX - self.buildingSize + j - 2,
                                      randY - self.buildingSize+k-2] = self.road
                for j in range(int(self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)/2*2)):
                    # hardcoded for the case where the interior is 3x3
                    for k in range(int(self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)/2*2)):
                        currentX = int(
                            randX - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (j))
                        currentY = int(
                            randY - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (k))
                        if self.gridSize - 1 < currentX:
                            continue
                        elif currentX < 0 + 1:
                            continue
                        elif currentY > self.gridSize - 1:
                            continue
                        elif 0 + 1 > currentY:
                            continue
                        else:
                            self.overlapGrid[currentX, currentY] = -1

                for j in range(int(2+self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)/2*4)):
                    # hardcoded for the case where the interior is 3x3
                    for k in range(int(2+self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)/2*4)):
                        currentX = int(
                            randX - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (j-1))
                        currentY = int(
                            randY - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (k-1))
                        if self.gridSize - 4 < currentX:
                            continue
                        elif currentX < 4:
                            continue
                        elif currentY > self.gridSize - 4:
                            continue
                        elif 4 > currentY:
                            continue
                        elif self.overlapGrid[currentX, currentY] != -1:
                            self.overlapGrid[currentX, currentY] = 1
                break
            elif numberOfIterations >= cutOff:
                print('Could not place building:', i)
                break

    def BuildingCheck(self,buildType,coordX,coordY):
        if buildType == "square":
            for j in range(self.buildingSize*2 + self.interiorSize + 2):
                for k in range(self.buildingSize*2 + self.interiorSize + 2):
                    if coordX - self.buildingSize + j - 2 < self.gridSize -1 and coordY - self.buildingSize+k-2 < self.gridSize-1:
                        if self.grid[coordX - self.buildingSize + j - 2, coordY - self.buildingSize+k-2] != 0:
                            self.obstruction = 1
                            break
                        elif coordX - self.buildingSize + j - 2 >= self.gridSize -1 or coordX - self.buildingSize + j - 2 <= 1:
                            self.obstruction = 1
                            break
                        elif coordY - self.buildingSize + j - 2 >= self.gridSize -1 or coordY - self.buildingSize + j - 2 <= 1:
                            self.obstruction = 1
                            break
                    break    

    # def PlaceLongBuilding(self, cutOff, coordX, coordY):