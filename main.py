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

#Agent Class


def main():
    test = Enviroment(10)
    test.BuildEnviroment()
    print(test.grid)








if __name__ == "__main__":
    main()
