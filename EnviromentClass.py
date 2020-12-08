import numpy as np
import random
#Enviroment Class. 
class Enviroment:
    def __init__(self,gridSize):
        self.gridSize = gridSize
        self.road = 1
        self.building = 2
        self.empty = 0
        self.inside = -1
        self.grid = np.zeros((gridSize,gridSize))
        self.overlapGrid = np.zeros((gridSize,gridSize)) #A seperate grid which keeps track of the locations where buildings cant be placed, since they would overlap with other buildings
        self.buildingSize = 2 #This determines the wall thickness
        self.interiorSize = 3 #Determines how large the interior of each building is, in this case 3x3. Has to be an odd number, otherwise there is not a clear center
        self.roadSize = 1

    def BuildEnviroment(self):
        #TODO Check what is road and what is building to make a good approximation
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                r = random.random()
                if r < 0.5:
                    self.grid[i,j] = self.building
                else:
                    self.grid[i,j] = self.road


    def DeterministicEnviroment(self):
        #Fix different cells start with 9
        v1 = [0,1,2,3,6,7,8,9]
        v2 = [3,6]
        self.grid[:,:] = self.road
        for i in range(self.gridSize):
            if i in v1:
                self.grid[i,v2] = self.building
            if i in v2:
                self.grid[i,v1] = self.building


    def PlaceBuildings(self,numberOfBuildings): #Each building takes a lot of space, about a 7x7 square on the grid.
        for i in range(numberOfBuildings):
            while True:
                randX = np.random.randint(self.buildingSize+self.interiorSize - 1,self.gridSize-self.buildingSize-self.interiorSize+1,1)
                randY = np.random.randint(self.buildingSize+self.interiorSize - 1,self.gridSize-self.buildingSize-self.interiorSize+1,1)
                if self.overlapGrid[randX,randY] == 0:
                    for j in range(self.buildingSize*2 + self.interiorSize):
                        for k in range(self.buildingSize*2 + self.interiorSize):
                            if self.grid[randX - self.buildingSize + j - 1,randY - self.buildingSize+k-1] == 0 or self.grid[randX - self.buildingSize + j - 1,randY - self.buildingSize+k-1] == 2:
                                self.grid[randX - self.buildingSize + j - 1,randY - self.buildingSize+k-1] = self.building

                    for j in range(self.interiorSize):
                        for k in range(self.interiorSize):
                            self.grid[randX + j - 1,randY + k - 1] = self.inside

                    for j in range(self.buildingSize*2 + self.interiorSize + 2):
                        for k in range(self.buildingSize*2 + self.interiorSize + 2):
                            if self.grid[randX - self.buildingSize + j - 2,randY - self.buildingSize+k-2] == 0:
                                self.grid[randX - self.buildingSize + j - 2,randY - self.buildingSize+k-2] = self.road

                    for j in range(self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)*2):
                        for k in range(self.buildingSize*4 + 1*self.interiorSize + 2*self.roadSize + (self.interiorSize-1)*2): #hardcoded for the case where the interior is 3x3
                            currentX = int(randX - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (j-1))
                            currentY = int(randY - 2*self.buildingSize - self.roadSize - 2*(self.interiorSize-1)/2 + (k-1))
                            if  self.gridSize -1 < currentX:
                                continue
                            elif currentX < -self.gridSize + 1:
                                continue
                            elif currentY > self.gridSize - 1:
                                continue
                            elif -self.gridSize + 1 > currentY:
                                continue
                            else:
                                self.overlapGrid[currentX,currentY] = 1
                    break


