import numpy as np
import math


class Agent:
    def __init__(self,numberAgents, grid, rangeLength = 2):
        self.grid = grid    
        self.numberAgents = numberAgents
        
        self.x = np.zeros(numberAgents) #Each agent has a x and y coordinate in the grid
        self.y = np.zeros(numberAgents)

        self.status = []
        self.gridSize = np.size(self.grid[0])

        self.buildingLocations = np.where(self.grid == 2)
        #print(self.buildingLocations)
        self.occupied = np.full((self.gridSize, self.gridSize),-1)  #Lists if the grid-tile is occupied with the agents index, and if not the list has a -1 value in that place.
        self.rangeLength = rangeLength

        self.reachableCellCoverage = []
        self.eachTileRange = []
        self.FindAlLReachable()
        self.corners = []
        self.FindCorners()
        self.counterPlacement = []
        print(self.corners)
        
        

    def resetCounter(self):
        self.counterPlacement = []
    def FindCorners(self):
        buildingTiles = len(self.buildingLocations[0])
        for i in range(buildingTiles):
            x = self.buildingLocations[0][i]
            y = self.buildingLocations[1][i]
            c = 0
            xPlus = x+1
            yPlus = y+1
            xMin = x-1
            yMin = y-1
            if xPlus // self.gridSize == 0 and yPlus // self.gridSize == 0 and self.grid[xPlus,yPlus] != 2:
                c += 1
            if xMin // self.gridSize == 0 and yPlus // self.gridSize == 0 and self.grid[xMin,yPlus] != 2:
                c += 1
            if xPlus // self.gridSize == 0 and yMin // self.gridSize == 0 and self.grid[xPlus,yMin] != 2:
                c += 1
            if xMin // self.gridSize == 0 and yMin // self.gridSize == 0 and self.grid[xMin,yMin] != 2:
                c += 1
            if c == 3:
                #Corner found 
                self.corners.append((x,y))


    def FindAlLReachable(self):
        buildingTiles = len(self.buildingLocations[0])
        self.reachableCellCoverage = []
        tmpList = []
        for i in range(buildingTiles):
            if i % 50 == 0:
                print(i)
            x = [self.buildingLocations[0][i]]
            y = [self.buildingLocations[1][i]]
            xy = [(x,y)]

            for i in range(self.rangeLength):
                reach = i + 1
                neighbourhood = len(x)
                for iNeighbour in range(neighbourhood):
                    xTmp = int(x[iNeighbour])
                    yTmp = int(y[iNeighbour])
                    #kolla neighbours
                    if (xTmp+1,yTmp) not in xy and xTmp+1 < np.size(self.grid[0]) and self.grid[xTmp+1,yTmp] != 2 :
                        tmpList.append((xTmp+1,yTmp))
                        x.append(xTmp+1)
                        y.append(yTmp)
                        xy.append((xTmp+1,yTmp))
                    if (xTmp-1,yTmp) not in xy and self.grid[xTmp-1,yTmp] != 2 and xTmp-1 >= 0:
                        tmpList.append((xTmp-1,yTmp))
                        x.append(xTmp-1)
                        y.append(yTmp)
                        xy.append((xTmp-1,yTmp))
                    if (xTmp,yTmp-1) not in xy and self.grid[xTmp,yTmp-1] != 2 and yTmp-1 >= 0:
                        tmpList.append((xTmp,yTmp-1))
                        x.append(xTmp)
                        y.append(yTmp-1)
                        xy.append((xTmp,yTmp-1))
                    if (xTmp,yTmp+1) not in xy and yTmp+1 < np.size(self.grid[0]) and self.grid[xTmp,yTmp+1] != 2:
                        tmpList.append((xTmp,yTmp+1))
                        x.append(xTmp)
                        y.append(yTmp+1)
                        xy.append((xTmp,yTmp+1))
            self.eachTileRange.append(xy)
        #tmpList = list(zip(*tmpList))
        for (i1,i2) in tmpList:
            if (i1,i2) not in self.reachableCellCoverage:
                self.reachableCellCoverage.append((i1,i2))

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
        for agent in range(self.numberAgents):
            x = [self.x[agent]]
            y = [self.y[agent]]
            tmpList = []
            tmpList.append((x[0],y[0]))
            for i in range(self.rangeLength):
                reach = i + 1
                neighbourhood = len(x)
                for iNeighbour in range(neighbourhood):
                    #print("inehg ",iNeighbour )
                    xTmp = int(x[iNeighbour])
                    yTmp = int(y[iNeighbour])
                    #kolla neighbours
                    if (xTmp+1,yTmp) not in tmpList and xTmp+1 < np.size(self.grid[0]) and self.grid[xTmp+1,yTmp] != 2 :
                        tmpList.append((xTmp+1,yTmp))
                        x.append(xTmp+1)
                        y.append(yTmp)
                    if (xTmp-1,yTmp) not in tmpList and self.grid[xTmp-1,yTmp] != 2 and xTmp-1 >= 0:
                        tmpList.append((xTmp-1,yTmp))
                        x.append(xTmp-1)
                        y.append(yTmp)
                    if (xTmp,yTmp-1) not in tmpList and self.grid[xTmp,yTmp-1] != 2 and yTmp-1 >= 0:
                        tmpList.append((xTmp,yTmp-1))
                        x.append(xTmp)
                        y.append(yTmp-1)
                    if (xTmp,yTmp+1) not in tmpList and yTmp+1 < np.size(self.grid[0]) and self.grid[xTmp,yTmp+1] != 2:
                        tmpList.append((xTmp,yTmp+1))
                        x.append(xTmp)
                        y.append(yTmp+1)
            tmpList.pop(0)
            tmpList = list(zip(*tmpList))
            self.status.append(tmpList)

    def TmpAgentRange(self, xy):
        x = [xy[0]]
        y = [xy[0]]
        tmpList = []
        tmpList.append((x[0],y[0]))
        for i in range(3):
            reach = i + 1
            neighbourhood = len(x)
            for iNeighbour in range(neighbourhood):
                #print("inehg ",iNeighbour )
                xTmp = int(x[iNeighbour])
                yTmp = int(y[iNeighbour])
                #kolla neighbours
                if (xTmp+1,yTmp) not in tmpList and xTmp+1 < np.size(self.grid[0]) and self.grid[xTmp+1,yTmp] != 2 :
                    tmpList.append((xTmp+1,yTmp))
                    x.append(xTmp+1)
                    y.append(yTmp)
                if (xTmp-1,yTmp) not in tmpList and self.grid[xTmp-1,yTmp] != 2 and xTmp-1 >= 0:
                    tmpList.append((xTmp-1,yTmp))
                    x.append(xTmp-1)
                    y.append(yTmp)
                if (xTmp,yTmp-1) not in tmpList and self.grid[xTmp,yTmp-1] != 2 and yTmp-1 >= 0:
                    tmpList.append((xTmp,yTmp-1))
                    x.append(xTmp)
                    y.append(yTmp-1)
                if (xTmp,yTmp+1) not in tmpList and yTmp+1 < np.size(self.grid[0]) and self.grid[xTmp,yTmp+1] != 2:
                    tmpList.append((xTmp,yTmp+1))
                    x.append(xTmp)
                    y.append(yTmp+1)
        tmpList.pop(0)
        return tmpList

    def RemoveTmpagentRange(self):
        self.status = []
        ##TODO the origianl coordinate for the agent is not in agentRange - Status list
        for agent in range(self.numberAgents):
            xx = [self.x[agent]]
            yy = [self.y[agent]]

            tmpList = []
            for reach in range(self.rangeLength):
                xxTmp = []
                yyTmp = []
                neighbor = len(xx)
                for iNeigbour in range(neighbor):
                    tmpX = int(xx[iNeigbour])
                    tmpY = int(yy[iNeigbour])
                    if tmpX + 1 < np.size(self.grid[0]) and self.grid[tmpX+1,tmpY] != 2:
                        tmp1 = (tmpX+1,tmpY,reach+1) #TODO Third coorinate should decay with each step of reach. 
                        tmpList.append(tmp1)
                        xxTmp.append(tmpX+1)
                        yyTmp.append(tmpY)
                    if tmpX - 1 >= 0 and self.grid[tmpX-1,tmpY] != 2: 
                        tmp2 = (tmpX-1,tmpY,reach+1)
                        tmpList.append(tmp2)
                        xxTmp.append(tmpX-1)
                        yyTmp.append(tmpY)
                    if tmpY + 1 < np.size(self.grid[0]) and self.grid[tmpX,tmpY+1] != 2:
                        tmp3 = (tmpX,tmpY+1,reach+1)
                        tmpList.append(tmp3)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY+1)
                    if tmpY - 1 >= 0 and self.grid[tmpX,tmpY-1] != 2:
                        tmp4 = (tmpX,tmpY-1,reach+1)
                        tmpList.append(tmp4)
                        xxTmp.append(tmpX)
                        yyTmp.append(tmpY-1)
                xx = xxTmp
                yy = yyTmp
        
            tmpList = list(zip(*tmpList))
            self.status.append(tmpList)

    def Get_distance(self,data1, data2):
        points = zip(data1, data2)
        diffs_squared_distance = [pow(a - b, 2) for (a, b) in points]
        return math.sqrt(sum(diffs_squared_distance))

    def Get_shortest_distance(self,allOverlap,openCells):
        minDist = self.gridSize*2
        coordinates = allOverlap
        for cellPair in openCells:
            dist = self.Get_distance(allOverlap,cellPair)
            openCluster = self.TmpAgentRange(cellPair)
            if len(openCluster) >= 20:
                if dist < minDist:
                    minDist = dist
                    coordinates = cellPair
        if coordinates == (0,0):
            print('error: Get_Shortest_distance')
        return coordinates

    def MoveToOpenBuilding(self,agent):
        #Move agent to open building that is good for coverage...
        openCells,coveredCells = self.OpenReachable()


    def MoveOverlap2(self,agent,moveOverlap2):
        xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
        yAgent = int(self.y[agent]) #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something                
        
        moveOverlap2 = list(zip(*moveOverlap2))
        
        agentCoverage = len(self.status[agent][0])
        if agentCoverage > 0.65*2*self.rangeLength*(self.rangeLength+1):
            #Optimal position don't move it
            print("agent {} is optimally placed at position ({},{})".format(agent,xAgent,yAgent))
            return
        if not moveOverlap2:
            return
        else:
            self.MoveToOpenBuilding(agent)
        
    def MoveOverlap(self,agent, moveOverlap2): #Normal move
        xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
        yAgent = int(self.y[agent]) #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something                
        
        #moveOverlap2 = list(zip(*moveOverlap2))
        
        agentCoverage = len(self.status[agent][0])
        if agentCoverage > 0.7*2*self.rangeLength*(self.rangeLength+1):
            #Optimal position don't move it
            print("agent {} is optimally placed at position ({},{})".format(agent,xAgent,yAgent))
            return
        if not moveOverlap2:
            return
        else:
            openCells,coveredCells = self.OpenReachable()
            rangee = len(openCells)
            for i in range(rangee-1,0,-1):
                if openCells[i] in self.counterPlacement:
                    openCells.pop(i) 

            directionX = 0
            directionY = 0
            totalDistance = 0
            totalNumberVectors = 0
            for allOverlap in moveOverlap2:
                try:
                    #xMove = allOverlap[0]
                    #yMove = allOverlap[1]
                    xMove = self.x[allOverlap]
                    yMove = self.y[allOverlap]
                except:
                    print("All overlap")
                    print(allOverlap)
                    print(moveOverlap2)
                #coordinates =  self.Get_shortest_distance((xMove,yMove),openCells)
                distance = np.sqrt((xMove - xAgent)**2 + (yMove - yAgent)**2)
                if distance == -11:
                    self.MoveAgent2(agent)
                    return
                if distance < 9:
                    coordinates =  self.Get_shortest_distance((xAgent,yAgent),openCells)
                    self.counterPlacement.append(coordinates)
                    print("Dist")
                    totalNumberVectors += 1
                    # directionX += (xAgent-coordinates[0])
                    # directionY += (yAgent-coordinates[1])
                    newX = (coordinates[0])
                    newX = int(round(newX))
                    newY = (coordinates[1])
                    newY = int(round(newY))

                    print("New:", newX,newY)
                    print("old:", xAgent,yAgent)
                    break
                    #totalDistance  += distance
                else:
                    #self.GeneratePositions(updateOne = [agent]) #Randomly move the overlapping agent to a new position
                    continue #Skips this iteration and goes back to for allOverlap in cellOverloaded.
            
            if totalNumberVectors == 0:
                return
            if (xAgent,yAgent) == (newX,newY):
                return
            # if totalNumberVectors == 2:
            #     self.MoveAgent2(agent)
            #     return
            # directionX = directionX/totalNumberVectors
            # directionY = directionY/totalNumberVectors
            # scaleFactor = 1
            # newX = -(xAgent  - (directionX)*scaleFactor)
            # newX = int(round(newX))
            # newY = -(yAgent  - (directionY)*scaleFactor)
            # newY = int(round(newY))

            # newX = ((directionX)*scaleFactor) % self.gridSize
            # newX = int(round(newX))
            # newY = ((directionY)*scaleFactor) % self.gridSize
            # newY = int(round(newY))

            # if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.occupied[newX][newY] == -1: 
            #     self.occupied[xAgent][yAgent] = -1
            #     self.x[agent]  = newX
            #     self.y[agent]  = newY
            #     self.occupied[newX][newY] = agent

            # return
            if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.grid[newX][newY] == 2 and self.occupied[newX][newY] == -1: 
                self.occupied[xAgent][yAgent] = -1
                self.x[agent]  = newX
                self.y[agent]  = newY
                self.occupied[newX][newY] = agent
            else:
                tmpCorners = self.corners.copy()
                #distancesFromBuildings = np.sqrt((newX**2 - self.buildingLocations[0][:])**2 + (newY**2 - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
                while True:
                    distancesFromBuildings = self.Get_shortest_distance((newX,newY), tmpCorners)
                    # closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
                    # chosenBuilding = np.random.randint(len(closestBuildings))
                    #TmpnewX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
                    #TmpnewY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
                    TmpnewX = distancesFromBuildings[0]
                    TmpnewY = distancesFromBuildings[1]
                    #tmpCoverage = self.TmpAgentRange((TmpnewX,TmpnewY))
                    if self.occupied[TmpnewX][TmpnewY] == -1:
                        self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
                        self.x[agent] = TmpnewX
                        self.y[agent] = TmpnewY
                        self.occupied[TmpnewX][TmpnewY] = agent #Updates the building occupancy
                        #print("Found")
                        return
                    else:
                        #distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
                        try:
                            tmpCorners = [item for item in tmpCorners if item not in [distancesFromBuildings]]
                        except:
                            pass
                            #print("corners",tmpCorners)
                            #print("distance",distancesFromBuildings)
                        if len(tmpCorners) == 0:
                            break
                #distancesFromBuildings = np.sqrt((newX**2 - self.buildingLocations[0][:])**2 + (newY**2 - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
            while True:
                closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
                chosenBuilding = np.random.randint(len(closestBuildings))
                TmpnewX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
                TmpnewY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
                #tmpCoverage = self.TmpAgentRange((TmpnewX,TmpnewY))
                if self.occupied[TmpnewX][TmpnewY] == -1:
                    self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
                    self.x[agent] = TmpnewX
                    self.y[agent] = TmpnewY
                    self.occupied[TmpnewX][TmpnewY] = agent #Updates the building occupancy
                    #print("Found")
                    break
                else:
                    distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
                    if len(distancesFromBuildings) == 0:
                        break

            
    
    def Moveold(self,agent,oldCoordinates):
        xAgent = int(self.x[agent])
        yAgent = int(self.y[agent])
        self.occupied[xAgent,yAgent] = -1
        print(int(oldCoordinates[0]))
        self.x[Agent] = int(oldCoordinates[0])
        self.y[Agent] = int(oldCoordinates[1])
        self.occupied[int(oldCoordinates[0]),int(oldCoordinates[1])] = agent


    def MoveAgent2(self,agent): #Random Move
        xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
        yAgent = int(self.y[agent]) #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something                
        
        # openCells = self.OpenCells()
        # randLen = len(openCells)
        # r = np.random.randint(0,randLen-1)
        # coordinatePair = openCells[r]
        # newX = coordinatePair[0]
        # newY = coordinatePair[1]
        print("randomness")
        for (newX,newY) in self.corners:
            if self.occupied[newX,newY] == -1:
                self.x[agent]  = newX
                self.y[agent]  = newY
                self.occupied[newX][newY] = agent
                return

        # if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.grid[newX][newY] == 2 and self.occupied[newX][newY] == -1: 
        #     #self.occupied[xAgent][yAgent] = -1
        #     self.x[agent]  = newX
        #     self.y[agent]  = newY
        #     self.occupied[newX][newY] = agent
        # else:
        #     distancesFromBuildings = np.sqrt((newX - self.buildingLocations[0][:])**2 + (newY - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
        #     while True:
        #         closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
        #         chosenBuilding = np.random.randint(len(closestBuildings))
        #         newX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
        #         newY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
        #         if self.occupied[newX][newY] == -1:
        #             #self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
        #             self.x[agent] = newX
        #             self.y[agent] = newY
        #             self.occupied[newX][newY] = agent #Updates the building occupancy
        #             #print("Found")
        #             break
        #         else:
        #             distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration


    def MoveAgent(self,agent, cellOveloaded):
        xAgent = int(self.x[agent]) #Needs to be forced to an integer, otherwise the program does not identify 3.0 as 3 for some reason.
        yAgent = int(self.y[agent]) #move backwards from first agent found that has overlap Fix so it moves away from average of all overlapping agents or something                
        agentCoverage = len(self.status[agent][0])
        if agentCoverage > 0.65*2*self.rangeLength*(self.rangeLength+1):
            #Optimal position don't move it
            print("agent {} is optimally placed at position ({},{})".format(agent,xAgent,yAgent))
            return
        self.occupied[xAgent][yAgent] = agent

        if not cellOveloaded:
            return
        else:
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

            if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.occupied[newX][newY] == -1: 
                self.occupied[xAgent][yAgent] = -1
                self.x[agent]  = newX
                self.y[agent]  = newY
                self.occupied[newX][newY] = agent


            

            # if newX // self.gridSize == 0 and newY // self.gridSize == 0 and self.grid[newX][newY] == 2 and self.occupied[newX][newY] == -1: 
            #     self.occupied[xAgent][yAgent] = -1
            #     self.x[agent]  = newX
            #     self.y[agent]  = newY
            #     self.occupied[newX][newY] = agent
            # else:
            #     distancesFromBuildings = np.sqrt((newX - self.buildingLocations[0][:])**2 + (newY - self.buildingLocations[1][:])**2) #Lists the distances to the closest tile with a building on it compared to the suggest new point
            #     while True:
            #         closestBuildings = np.where((distancesFromBuildings == min(distancesFromBuildings)))
            #         chosenBuilding = np.random.randint(len(closestBuildings))
            #         newX = self.buildingLocations[0][closestBuildings[0][chosenBuilding]]
            #         newY = self.buildingLocations[1][closestBuildings[0][chosenBuilding]]
            #         if self.occupied[newX][newY] == -1:
            #             self.occupied[xAgent][yAgent] = -1 #Makes the old tile usuable for other agents
            #             self.x[agent] = newX
            #             self.y[agent] = newY
            #             self.occupied[newX][newY] = agent #Updates the building occupancy
            #             #print("Found")
            #             break
            #         else:
            #             distancesFromBuildings = np.delete(distancesFromBuildings,closestBuildings[0][chosenBuilding]) #Removes the tile from consideration
            #             if len(distancesFromBuildings) == 0:
            #                 break

    def CheckCoverage(self):
        maximumCoverage = self.gridSize**2 - len(self.buildingLocations[0])
        
        coveredCells = []
        for i in range(self.numberAgents):
            if len(self.status[i]) > 0:    
                xCoverage = self.status[i][0]
                yCoverage = self.status[i][1]
                coveregeLen = len(xCoverage)
                for j in range(coveregeLen):
                    xTmp = xCoverage[j]
                    yTmp = yCoverage[j]
                    if (xTmp,yTmp) not in coveredCells:
                        coveredCells.append((xTmp,yTmp))
            else:
                continue
        
            
        
        currentCoverage = len(coveredCells) / maximumCoverage
        return currentCoverage,coveredCells

    def OpenCells(self):
        coveredCells = []
        for i in range(self.numberAgents):
            if len(self.status[i]) > 0:    
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
                if (i,j) not in coveredCells and self.grid[i,j] != 2:
                    openCells.append((i,j))
        #Do a reachable open cells loop

        return openCells

    def OpenReachable(self):
        coveredCells = []
        for i in range(self.numberAgents):
            if len(self.status[i]) > 0:    
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
                if (i,j) not in coveredCells and (i,j) in self.reachableCellCoverage:
                    openCells.append((i,j))
        #Do a reachable open cells loop

        return openCells,coveredCells
        
            



