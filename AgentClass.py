import numpy as np

#comment
#comment
class Agent:
    def __init__(self,numberAgents, grid):
        self.grid = grid    
        #Test
        self.numberAgents = numberAgents
        self.x = np.zeros(numberAgents) #Each agent has a x and y coordinate in the grid
        self.y = np.zeros(numberAgents)
        self.status = []

    def agentRange(self, rangeLength):
        self.status = []
        for agent in range(self.numberAgents):
            tmpX = self.x[agent]
            tmpY = self.y[agent]
            #Spread to neighbors but be careful of boundaries in grid "two step neighbor"
            for reach in range(rangeLength):
                #tmpX + 1,tmpY
                #Line for change
                #tmpX - 1,tmpY
                #tmpX,tmpY + 1
                #tmpX,tmpY + 1
                if tmpX + 1 < np.size(self.grid[0])-1:
                    tmp1 = (tmpX+1,tmpY)
                if tmpX - 1 > 0:
                    tmp2 = (tmpX-1,tmpY)
                if tmpY + 1 < np.size(self.grid[0])-1:
                    tmp3 = (tmpX,tmpY)
                if tmpY - 1 > 0:
                    tmp4 = (tmpX-1,tmpY)

        self.status.append(tmpArray)

    def GeneratePositions(grid, numberAgents):
        possibleLocations = np.where(grid == 2):
        for i in range(numberAgents):
            randomPos = np.random.randint(len(possibleLocations[0])+1)
            self.x[i] = possibleLocations[0][randomPos]
            self.y[i] = possibleLocations[1][randomPos]
     

