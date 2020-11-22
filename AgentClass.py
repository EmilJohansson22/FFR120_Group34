import numpy as np

#comment
#comment
class Agent:
    def __init__(self,numberAgents, grid):
        self.grid = grid    
        self.numberAgents = numberAgents
        self.x = np.zeros(numberAgents) #Each agent has a x and y coordinate in the grid
        self.y = np.zeros(numberAgents)
        self.status = []

    def agentRange(self, rangeLength):
        self.status = []
        ##TODO the origianl coordinate for the agent is not in agentRange - Status list
        for agent in range(self.numberAgents):
            xx = [self.x[agent]]
            yy = [self.y[agent]]
            #Spread to neighbors but be careful of boundaries in grid "two step neighbor"
            tmpList = []
            for reach in range(rangeLength):
                xxTmp = []
                yyTmp = []
                neighbor = len(xx)
                for iNeigbour in range(neighbor):
                    tmpX = xx[iNeigbour]
                    tmpY = yy[iNeigbour]
                    if tmpX + 1 < np.size(self.grid[0]):
                        tmp1 = (tmpX+1,tmpY,1/(reach+1))
                        tmpList.append(tmp1)
                        xxTmp.append(tmpX+1)
                        yyTmp.append(tmpY)
                    if tmpX - 1 > 0:
                        tmp2 = (tmpX-1,tmpY,1/(reach+1))
                        tmpList.append(tmp2)
                        xxTmp.append(tmpX-1)
                        yyTmp.append(tmpY)
                    if tmpY + 1 < np.size(self.grid[0]):
                        tmp3 = (tmpX,tmpY,1/(reach+1))
                        tmpList.append(tmp3)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY+1)
                    if tmpY - 1 > 0:
                        tmp4 = (tmpX-1,tmpY,1/(reach+1))
                        tmpList.append(tmp4)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY-1)
                xx = xxTmp
                yy = yyTmp
        
            tmpList = list(zip(*tmpList))
            self.status.append(tmpList)

    def MoveAgent(self,agent, cellOveloaded):
        #Direction between cell overloaded and 
        numberOverlaps = len(cellOveloaded)
        x = self.x[agent]
        y = self.y[agent]
        status = self.status[agent]
        if cellOveloaded:
            return
        else:
            for i in range(numberOverlaps):#TODO several overlaps some kind averae where the new agent should move
                xStatus = status[0][i]
                yStatus = status[1][i]
                xDir = (x- xStatus) /np.sqrt((x- xStatus)**2 + (y- yStatus)**2)
                yDir = (y- yStatus)/np.sqrt((x- xStatus)**2 + (y- yStatus)**2)
        
        print('move agent')
        #TODO make sure the updated position is on the grid cell with a buidling.
