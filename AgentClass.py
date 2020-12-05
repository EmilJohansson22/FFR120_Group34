import numpy as np


class Agent:
    def __init__(self,numberAgents, grid, rangeLength = 2):
        self.grid = grid    
        self.numberAgents = numberAgents
        
        self.x = np.zeros(numberAgents) #Each agent has a x and y coordinate in the grid
        self.y = np.zeros(numberAgents)

        self.status = []
        self.gridSize = np.size(self.grid[0])

        self.buildingLocations = np.where(self.grid == 2)

        self.occupied = np.full((self.gridSize, self.gridSize),-1)  #Lists if the grid-tile is occupied with the agents index, and if not the list has a -1 value in that place.
        self.rangeLength = rangeLength

    def GeneratePositions(self, updateOne = []):
        if updateOne:
            print('only one agent random position update')
            for i in updateOne:
                possibleLocations = np.where(self.grid == 2)
                randomPos = np.random.randint(len(possibleLocations[0]))
                x = possibleLocations[0][randomPos]
                y = possibleLocations[1][randomPos]
                while self.occupied[x][y] != -1: #TODO Does not work
                    randomPos = np.random.randint(len(possibleLocations[0]))
                    x = possibleLocations[0][randomPos]
                    y = possibleLocations[1][randomPos]
                self.x[i] = x 
                self.y[i] = y
                self.occupied[x][y] = i #Shows which agent is occupying which tile
            return
        
        
        possibleLocations = np.where(self.grid == 2)
        for i in range(self.numberAgents):
            randomPos = np.random.randint(len(possibleLocations[0]))
            self.x[i] = possibleLocations[0][randomPos]
            self.y[i] = possibleLocations[1][randomPos]
            self.occupied[possibleLocations[0][randomPos]][possibleLocations[1][randomPos]] = i #Shows which agent is occupying which tile
    
    def agentRange(self):
        self.status = []
        ##TODO the origianl coordinate for the agent is not in agentRange - Status list
        for agent in range(self.numberAgents):
            xx = [self.x[agent]]
            yy = [self.y[agent]]
            #Spread to neighbors but be careful of boundaries in grid "two step neighbor"
            tmpList = []
            for reach in range(self.rangeLength):
                xxTmp = []
                yyTmp = []
                neighbor = len(xx)
                for iNeigbour in range(neighbor):
                    tmpX = int(xx[iNeigbour])
                    tmpY = int(yy[iNeigbour])
                    if tmpX + 1 < np.size(self.grid[0]) and self.grid[tmpX+1,tmpY] != 2:
                        tmp1 = (tmpX+1,tmpY,1) #TODO Third coorinate should decay with each step of reach. 
                        tmpList.append(tmp1)
                        xxTmp.append(tmpX+1)
                        yyTmp.append(tmpY)
                    if tmpX - 1 >= 0 and self.grid[tmpX-1,tmpY] != 2: 
                        tmp2 = (tmpX-1,tmpY,1)
                        tmpList.append(tmp2)
                        xxTmp.append(tmpX-1)
                        yyTmp.append(tmpY)
                    if tmpY + 1 < np.size(self.grid[0]) and self.grid[tmpX,tmpY+1] != 2:
                        tmp3 = (tmpX,tmpY+1,1)
                        tmpList.append(tmp3)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY+1)
                    if tmpY - 1 >= 0 and self.grid[tmpX,tmpY-1] != 2:
                        tmp4 = (tmpX,tmpY-1,1)
                        tmpList.append(tmp4)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY-1)
                xx = xxTmp
                yy = yyTmp
        
            tmpList = list(zip(*tmpList))
            self.status.append(tmpList)

    def MoveAgent(self,agent, cellOveloaded):

        if not cellOveloaded:
            return
        else:
            xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
            yAgent = int(self.y[agent]) #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something                
            
            directionX = 0
            directionY = 0
            totalDistance = 0
            for allOverlap in cellOveloaded:
            #for abc in range(1):
            #    allOverlap = cellOveloaded[0]
                xMove = self.x[allOverlap]
                yMove = self.y[allOverlap]
                distance = np.sqrt((xMove - xAgent)**2 + (yMove - yAgent)**2)
                if distance != 0:
                    directionX += (xMove - xAgent) / distance #Unit vector
                    directionY += (yMove - yAgent) / distance
                    #totalDistance  += distance
                else:
                    #self.GeneratePositions(updateOne = [agent]) #Randomly move the overlapping agent to a new position
                    continue #Skips this iteration and goes back to for allOverlap in cellOverloaded.
        
            totalDistance = np.sqrt(directionX**2 + directionY**2)
            if totalDistance == 0:
                totalDistance = 1
            directionX = directionX/totalDistance
            directionY = directionY/totalDistance
            scaleFactor = 1
            newX = (xAgent  - (directionX)*scaleFactor)
            newX = int(round(newX))
            newY = (yAgent  - (directionY)*scaleFactor)
            newY = int(round(newY))

            #Testing with moving towards no coverage...
            # openCells = self.OpenCells()
            # randLen = len(openCells)
            # r = np.random.randint(0,randLen-1)
            # coordinatePair = openCells[r]
            # newX = coordinatePair[0]
            # newY = coordinatePair[1]
            


            # if newX //self.gridSize == 0 and newY // self.gridSize == 0 and self.occupied[newX][newY] == -1: 
            #     self.occupied[xAgent][yAgent] = -1
            #     self.x[agent]  = newX
            #     self.y[agent]  = newY
            #     self.occupied[newX][newY] = agent
            # else:
            #     #self.GeneratePositions(updateOne = [agent]) #Randomly move the overlapping agent to a new position
            #     pass #Skips this iteration and goes back to for allOverlap in cellOverloaded.
                

        
        

            if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.grid[newX][newY] == 2 and self.occupied[newX][newY] == -1: 
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
                        #print("Found")
                        break
                    else:
                        distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
                        #print(distancesFromBuildings)
                        #print("Removing")
                    # distancesFromBuildings = np.sqrt((newX - self.buildingLocations[0][:])**2 + (newY - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
                    # while True: #TODO This function seems to remove a bunch of distances and throw error when distancesFromBuilding is empty
                    #     print("Closest buidling list", distancesFromBuildings)
                    #     closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
                    #     chosenBuilding = np.random.randint(len(closestBuildings))
                    #     newX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
                    #     newY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
                    #     tmpabc = True
                    #     #if tmpabc:
                    #     if self.occupied[newX][newY] == -1:
                    #         self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
                    #         self.x[agent] = newX
                    #         self.y[agent] = newY
                    #         self.occupied[newX][newY] = agent #Updates the building occupancy
                    #         print("Found")
                    #         break
                    #     else:
                    #         distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
                    #         #print("Removing")
                

    def CheckCoverage(self):
        maximumCoverage = self.gridSize**2 - len(self.buildingLocations[0])
        
        coveredCells = []
        for i in range(self.numberAgents):
            xCoverage = self.status[i][0]
            yCoverage = self.status[i][1]
            coveregeLen = len(xCoverage)
            for j in range(coveregeLen):
                xTmp = xCoverage[j]
                yTmp = yCoverage[j]
                if (xTmp,yTmp) not in coveredCells:
                    coveredCells.append((xTmp,yTmp))
        
        currentCoverage = len(coveredCells) / maximumCoverage
        return currentCoverage,coveredCells

    def OpenCells(self):
        coveredCells = []
        for i in range(self.numberAgents):
            xCoverage = self.status[i][0]
            yCoverage = self.status[i][1]
            coveregeLen = len(xCoverage)
            for j in range(coveregeLen):
                xTmp = xCoverage[j]
                yTmp = yCoverage[j]
                if (xTmp,yTmp) not in coveredCells:
                    coveredCells.append((xTmp,yTmp))
        
        openCells = []
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if (i,j) not in coveredCells:
                    openCells.append((i,j))

        return openCells
        
            



