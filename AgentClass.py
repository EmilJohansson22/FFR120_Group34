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
        self.gridSize = np.size(self.grid[0])
        self.buildingLocations = np.where(self.grid == 2)
        self.occupied = np.full((self.gridSize, self.gridSize),-1)  #Lists if the grid-tile is occupied with the agents index, and if not the list has a -1 value in that place.
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
                        tmp1 = (tmpX+1,tmpY,1) #TODO Third coorinate should decay with each step of reach. 
                        tmpList.append(tmp1)
                        xxTmp.append(tmpX+1)
                        yyTmp.append(tmpY)
                    if tmpX - 1 > 0:
                        tmp2 = (tmpX-1,tmpY,1)
                        tmpList.append(tmp2)
                        xxTmp.append(tmpX-1)
                        yyTmp.append(tmpY)
                    if tmpY + 1 < np.size(self.grid[0]):
                        tmp3 = (tmpX,tmpY,1)
                        tmpList.append(tmp3)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY+1)
                    if tmpY - 1 > 0:
                        tmp4 = (tmpX-1,tmpY,1)
                        tmpList.append(tmp4)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY-1)
                xx = xxTmp
                yy = yyTmp
        
            tmpList = list(zip(*tmpList))
            self.status.append(tmpList)

    def MoveAgent(self,agent, cellOveloaded):
        ## TODO Make sure the agent moves to a "building " cell
        if not cellOveloaded:
            return
        else:
            xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
            yAgent = int(self.y[agent])
            #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something
            xMove = self.x[cellOveloaded[0]]
            yMove = self.y[cellOveloaded[0]] # For some reason xMove and yMove are equal to xAgent and yAgent alot of the time
            directionX = (xMove - xAgent) / np.sqrt((xMove - xAgent)**2 + (yMove - yAgent)**2)
            directionY = (yMove - yAgent) / np.sqrt((xMove - xAgent)**2 + (yMove - yAgent)**2) 
            if np.isnan(directionX) or np.isnan(directionY):
                SystemExit("The direction evaluates as NaN")
            newX = round(xAgent  - round(directionX))
            newY = round(xAgent  - round(directionY))
            
            if newX <= self.gridSize-1 and newY <= self.gridSize-1 and self.grid[newX][newY] == 2 and self.occupied[newX][newY] == -1:
                self.occupied[xAgent][yAgent] = -1
                self.x[agent]  = newX
                self.y[agent]  = newY
                self.occupied[newX][newY] = agent
            else:
                distancesFromBuildings = np.sqrt((newX - self.buildingLocations[0][:])**2 + (newY - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
                while True:
                    closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
                    chosenBuilding = np.random.randint(len(closestBuildings))
                    newX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
                    newY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
                    if self.occupied[newX][newY] == -1:
                        self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
                        self.x[agent] = newX
                        self.y[agent] = newY
                        self.occupied[newX][newY] = agent #Updates the building occupancy
                        print("Found")
                        break
                    else:
                        distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
                        print("Removing")
                






        #     numberOverlaps = len(cellOveloaded)
        #     x = self.x[agent]
        #     y = self.y[agent]
        #     currentStatus = self.status[agent]
        #     xStatus = currentStatus[0]
        #     yStatus = currentStatus[1]
        #     print("Agent x before: ",x)
        #     print("Cell overloaded: ", cellOveloaded)
        #     status = self.status[agent]

    
        #     print("length of status: ", len(xStatus))
        #     for i in cellOveloaded:#TODO several overlaps some kind averae where the new agent should move
        #         xx = xStatus[i] #Overlapping x coordinate
        #         yy = xStatus[i] #ovelapping y coordinate
        #         xDir = (x- xx) /np.sqrt((x- xx)**2 + (y- yy)**2) #Normalized direction of overlap move agent away from overlap
        #         yDir = (y- yy)/np.sqrt((x- xx)**2 + (y- yy)**2)
            
        #     #Check boundary
        #     if not self.x[agent] == 0 or not self.x[agent] == self.gridSize:
        #         self.x[agent] = self.x[agent] - round(xDir)
        #     if not self.y[agent] == 0 or not self.y[agent] == self.gridSize:
        #         self.y[agent] =  self.y[agent] - round(yDir)
        #     print("agent x after: ", self.x[agent])
        
        #     print('move agent')
        # #TODO make sure the updated position is on the grid cell with a buidling.

    def GeneratePositions(self, grid):
        possibleLocations = np.where(grid == 2)
        for i in range(self.numberAgents):
            randomPos = np.random.randint(len(possibleLocations[0]))
            self.x[i] = possibleLocations[0][randomPos]
            self.y[i] = possibleLocations[1][randomPos]
            self.occupied[possibleLocations[0][randomPos]][possibleLocations[1][randomPos]] = i #Shows which agent is occupying which tile