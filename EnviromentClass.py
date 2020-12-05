import numpy as np
import random
#Enviroment Class. 
class Enviroment:
    def __init__(self,gridSize):
        self.gridSize = gridSize
        self.road = 1
        self.building = 2
        self.empty = 0
        self.grid = np.zeros((gridSize,gridSize))
    
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
        #Fix different cells start with 10
        v1 = [0,1,2,3,6,7,8,9]
        v2 = [3,6]
        
        self.grid[:,:] = self.road

        for i in range(self.gridSize):
            if i in v1:
                self.grid[i,v2] = self.building
            if i in v2:
                self.grid[i,v1] = self.building
    
    def NewEnviroment(self):
        #This is the new enviroment
        pass

            

