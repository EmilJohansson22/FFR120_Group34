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
        self.buildingSize = 2  # This determines the wall thickness
        self.interiorSize = 3  # Determines how large the interior of each building is, in this case 3x3. Has to be an odd number, otherwise there is not a clear center
        self.roadSize = 1
        self.GenerateBuildNodes()
        self.grid = np.zeros((self.gridSize, self.gridSize))
        # A seperate grid which keeps track of the locations where buildings cant be placed, since they would overlap with other buildings
        self.overlapGrid = np.zeros((self.gridSize, self.gridSize))

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

    def GenerateBuildNodes(self): # This function generates positions where the buildings can be placed.
        buildingSpace = self.roadSize*2 + self.buildingSize*2 + self.interiorSize
        nmrOfBuildNodes = self.gridSize/buildingSpace
        l = 0
        if isinstance(nmrOfBuildNodes,int):
            self.buildingGrid = np.ones(nmrOfBuildNodes)
        else:
            k = self.gridSize % buildingSpace
            roundedUpGridSize = self.gridSize + buildingSpace - k
            print("The gridsize was increased from", self.gridSize, "to", roundedUpGridSize)
            self.gridSize = roundedUpGridSize 
            nmrOfBuildNodes = int(self.gridSize/buildingSpace)
            self.buildingGrid = np.ones((nmrOfBuildNodes, nmrOfBuildNodes))
        for i in range(nmrOfBuildNodes):
            for j in range(nmrOfBuildNodes):
                self.buildingGrid[i][j] = l
                l += 1


    def PlaceBuildings_version2(self,numberOfBuildings):
        cutOff = 700
        for i in range(numberOfBuildings):
            numberOfTries = 0
            buildingTypes = ["Square", "Double"] #add rolling for building type here
            while True:
                    numberOfTries = numberOfTries + 1
                    possNodes = np.where(np.isfinite(self.buildingGrid))
                    length = len(possNodes[0][:])
                    randIndex = np.random.randint(length)
                    compRow = possNodes[0][randIndex]
                    compCol = possNodes[1][randIndex]
                    [buildingX,buildingY] = self.FindBuildingCenter(compRow,compCol)
                    buildType = random.choice(buildingTypes)

                    if buildType == "Square":
                        self.PlaceSquareBuilding_version2(cutOff,i,buildingX,buildingY)
                        print('Building:',i, "placed at X=",buildingX,"Y=",buildingY)
                        self.buildingGrid[possNodes[0][randIndex]][possNodes[1][randIndex]] = np.nan
                        break
                    elif buildType == "Double":
                        [neighbours, possibleDirections] = self.FindNeighbours(compRow, compCol)
                        if len(possibleDirections) >= 1:
                            self.PlaceDouble(cutOff, i, buildingX, buildingY, possibleDirections, compCol, compRow)
                            print('Building:',i, "placed at X=",buildingX,"Y=",buildingY)
                            self.buildingGrid[possNodes[0][randIndex]][possNodes[1][randIndex]] = np.nan
                    elif numberOfTries == cutOff:
                        print("Could not place building")
                        break

    def FindBuildingCenter(self, compRow, compCol):
        buildingX = (self.buildingSize + (self.interiorSize - 1)) + compCol*(self.buildingSize*2 + self.interiorSize + self.roadSize)
        buildingY = (self.buildingSize + (self.interiorSize - 1)) + compRow*(self.buildingSize*2 + self.interiorSize + self.roadSize)
        return [int(buildingX), int(buildingY)]

    def PlaceSquareBuilding_version2(self,cutOff, i,randX,randY):
        numberOfIterations = 0
        while True:
            numberOfIterations = numberOfIterations + 1
            if  numberOfIterations < cutOff:
                for j in range(self.buildingSize*2 + self.interiorSize):
                    for k in range(self.buildingSize*2 + self.interiorSize):
                        #if self.grid[randX - self.buildingSize + j - int((self.interiorSize-1)/2), randY - self.buildingSize + k - int((self.interiorSize-1)/2)] == 0:
                            self.grid[randX - self.buildingSize + j - int((self.interiorSize-1)/2),
                                      randY - self.buildingSize+k - int((self.interiorSize-1)/2)] = self.building

                for j in range(self.interiorSize):
                    for k in range(self.interiorSize):
                        self.grid[randX + j - 1, randY + k - 1] = self.inside

                for j in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                    for k in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                        if self.grid[randX - self.buildingSize + j - 2, randY - self.buildingSize+k-2] == 0 :
                            self.grid[randX - self.buildingSize + j - 2,
                                      randY - self.buildingSize+k-2] = self.road
                break
            elif numberOfIterations >= cutOff:
                print('Could not place building:', i)
                break

    def FindNeighbours(self,compRow, compCol):
        possibleDirections = ["up", "right", "down", "left"]
        length = len(self.buildingGrid)
        neighbours = []
        index = self.buildingGrid[compRow][compCol]
        if compCol == 0 or np.isnan(self.buildingGrid[compRow][compCol - 1]):
            possibleDirections.remove('left')
        if compRow == 0 or np.isnan(self.buildingGrid[compRow-1][compCol]):
            possibleDirections.remove('up')
        if compCol == len(self.buildingGrid) - 1 or np.isnan(self.buildingGrid[compRow][compCol + 1]):
            possibleDirections.remove('right')
        if compRow == len(self.buildingGrid) - 1 or np.isnan(self.buildingGrid[compRow+1][compCol]):
            possibleDirections.remove('down')

        for direction in possibleDirections:
            if direction == "up":
                neighbours.append(index - length)
            elif direction == "right":
                neighbours.append(index + 1)
            elif direction == "down":
                neighbours.append(index + length)
            elif direction == "left":
                neighbours.append(index - 1)
                
        return [neighbours, possibleDirections]

    def PlaceDouble(self, cutOff, i, buildingX, buildingY, possibleDirections, compCol, compRow):
        numberOfIterations = 0
        while True:
            chosenDirection = random.choice(possibleDirections)

            if chosenDirection == "up":
                for j in range(self.buildingSize*2 + self.interiorSize):
                    for k in range(self.buildingSize*4 + self.interiorSize*2 + self.roadSize):
                        #if self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2), buildingY - 3*self.buildingSize + k - int((self.interiorSize-1)/2) - self.interiorSize - self.roadSize] == 0:
                            self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2),
                                      buildingY - 3*self.buildingSize + k - int((self.interiorSize-1)/2) - self.interiorSize - self.roadSize] = self.building
                
                for j in range(self.interiorSize):
                    for k in range(self.interiorSize*2 + 2*self.buildingSize + self.roadSize):
                        self.grid[buildingX + j - int((self.interiorSize-1)/2),
                                  buildingY + k - int((self.interiorSize-1)/2) - 2*self.buildingSize - self.roadSize - self.interiorSize] = self.inside

                for j in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                    for k in range(self.buildingSize*4 + self.interiorSize*2 + 3*self.roadSize):
                        if self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize,
                                    buildingY - 3*self.buildingSize + k - int((self.interiorSize-1)/2) - self.interiorSize - 2*self.roadSize] == 0:
                            self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize,
                                      buildingY - 3*self.buildingSize + k - int((self.interiorSize-1)/2) - self.interiorSize - 2*self.roadSize] = self.road
                connectedCol = compCol 
                connectedRow = compRow - 1
                self.buildingGrid[connectedRow][connectedCol] = np.nan
                break


            if chosenDirection == "down":
                for j in range(self.buildingSize*2 + self.interiorSize):
                    for k in range(self.buildingSize*4 + self.interiorSize*2 + self.roadSize):
                       # if self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2), buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] == 0:
                            self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2),
                                      buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] = self.building
                
                for j in range(self.interiorSize):
                    for k in range(self.interiorSize*2 + 2*self.buildingSize + self.roadSize):
                        self.grid[buildingX + j - int((self.interiorSize-1)/2),
                                  buildingY + k - int((self.interiorSize-1)/2)] = self.inside

                for j in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                    for k in range(self.buildingSize*4 + self.interiorSize*2 + 3*self.roadSize):
                        if self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize, buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] == 0 :
                            self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize,
                                      buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] = self.road
                connectedCol = compCol 
                connectedRow = compRow + 1
                self.buildingGrid[connectedRow][connectedCol] = np.nan
                break



            if chosenDirection == "right":
                for k in range(self.buildingSize*2 + self.interiorSize):
                    for j in range(self.buildingSize*4 + self.interiorSize*2 + self.roadSize):
                        #if self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2), buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] == 0:
                            self.grid[buildingX - self.buildingSize + j - int((self.interiorSize-1)/2),
                                      buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] = self.building
                
                for k in range(self.interiorSize):
                    for j in range(self.interiorSize*2 + 2*self.buildingSize + self.roadSize):
                        self.grid[buildingX + j - int((self.interiorSize-1)/2),
                                  buildingY + k - int((self.interiorSize-1)/2)] = self.inside

                for k in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                    for j in range(self.buildingSize*4 + self.interiorSize*2 + 3*self.roadSize):
                        if self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize, buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] == 0:
                            self.grid[buildingX + j - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize,
                                      buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] = self.road
                connectedCol = compCol + 1
                connectedRow = compRow
                self.buildingGrid[connectedRow][connectedCol] = np.nan
                break

            if chosenDirection == "left":
                for k in range(self.buildingSize*2 + self.interiorSize):
                    for j in range(self.buildingSize*4 + self.interiorSize*2 + self.roadSize):
                        if self.grid[buildingX - 3*self.buildingSize + j - int((self.interiorSize-1)/2) - self.interiorSize - self.roadSize, buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] == 0:
                            self.grid[buildingX - 3*self.buildingSize + j - int((self.interiorSize-1)/2) - self.interiorSize - self.roadSize,
                                      buildingY - self.buildingSize + k - int((self.interiorSize-1)/2)] = self.building
                
                for k in range(self.interiorSize):
                    for j in range(self.interiorSize*2 + 2*self.buildingSize + self.roadSize):
                        self.grid[buildingX + j - int((self.interiorSize-1)/2)- 2*self.buildingSize - self.roadSize - self.interiorSize,
                                  buildingY + k - int((self.interiorSize-1)/2)] = self.inside

                for k in range(self.buildingSize*2 + self.interiorSize + 2*self.roadSize):
                    for j in range(self.buildingSize*4 + self.interiorSize*2 + 3*self.roadSize):
                        if self.grid[buildingX - 3*self.buildingSize + j - int((self.interiorSize-1)/2) - self.interiorSize - 2*self.roadSize, buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] == 0 :
                            self.grid[buildingX - 3*self.buildingSize + j - int((self.interiorSize-1)/2) - self.interiorSize - 2*self.roadSize,
                                      buildingY + k - int((self.interiorSize-1)/2) - self.roadSize - self.buildingSize] = self.road        
                connectedCol = compCol - 1
                connectedRow = compRow
                self.buildingGrid[connectedRow][connectedCol] = np.nan
                break