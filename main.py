import numpy as np
import random
import EnviromentClass
import AgentClass
import time as timer
from tkinter import *
from tkinter import ttk


def main():

    res = 500   # Animation resolution
    tk = Tk()  
    tk.geometry( str(int(res*1.1)) + 'x'  +  str(int(res*1.3)) )
    tk.configure(background='white')

    canvas = Canvas(tk, bd=2)            # Generate animation window 
    tk.attributes('-topmost', 0)
    canvas.place(x=res/20, y=res/20, height= res, width= res)
    gridSize = 10 #Has to be 10 as of now.


    test = EnviromentClass.Enviroment(gridSize) 
    test.PlaceBuildings(1)
    print(test.grid)
    #test.DeterministicEnviroment()
    
    #Build Grid
    gridPlot = []
    ccolor = ['black','gray','red']
    for i in range(gridSize):     # Generate animated particles in Canvas 
        for j in range(gridSize):     # Generate animated particles in Canvas 
            if test.grid[i,j] == test.building:
                gridPlot.append( canvas.create_rectangle( (i)*res/gridSize,                                           
                                                    (j)*res/gridSize,                           
                                                    (i+1)*res/gridSize,                               
                                                    (j+1)*res/gridSize,                               
                                                    outline=ccolor[0], fill=ccolor[0]) )
            else:
                gridPlot.append( canvas.create_rectangle( (i)*res/gridSize,                                           
                                                    (j)*res/gridSize,                           
                                                    (i+1)*res/gridSize,                               
                                                    (j+1)*res/gridSize,                               
                                                    outline=ccolor[1], ))



    totalAgents = 10
    agents = AgentClass.Agent(totalAgents,test.grid,rangeLength=4)


    agents.GeneratePositions()
    agents.agentRange()
    currentCoverage,coveragePosition = agents.CheckCoverage()

    print("CoveragePosition \n ", coveragePosition)
    print("Starting coverage with random initialized positions: ", currentCoverage)
    # print(agents.status)
    # print("A0\n",agents.status[0]) #Gets agent 0 status with x, y and some decay value...
    # print("A1\n",agents.status[1]) #Gets agent 0 status with x, y and some decay value...

    # tmpList = list(zip(*agents.status))
    # print("x\n", tmpList[0])

    agentPlot = []
    for j in range(totalAgents):     # Generate animated particles in Canvas 
        xx = agents.x[j]
        yy = agents.y[j]
        agentPlot.append(canvas.create_oval((xx)*res/gridSize,                                           
                                            (yy)*res/gridSize,                           
                                            (xx+1)*res/gridSize,                               
                                            (yy+1)*res/gridSize,                               
                                            outline=ccolor[2], fill=ccolor[2]) )

    coveragePlot = []
    for i in range(gridSize):     # Generate animated particles in Canvas 
        for j in range(gridSize):     # Generate animated particles in Canvas 
            if (i,j) in coveragePosition:
                coveragePlot.append( canvas.create_rectangle( (i)*res/gridSize,                                           
                                                    (j)*res/gridSize,                           
                                                    (i+1)*res/gridSize,                               
                                                    (j+1)*res/gridSize,                               
                                                    outline='orange', fill='orange' ))

    print("coveragePlot : ", coveragePlot)
    tk.update()    
    timer.sleep(1)
    bestCoverage = currentCoverage
    threshold = 1
    #Test a couple of runs
    #TODO When two agents are on the same spot an error occurs
    for iteration in range(50):
        print("iteration: ", iteration)
        for agent in range(totalAgents): ##TODO make the list a permutation of each agent
            #print("Agent number\n",agent)
            agents.agentRange()
            xOld = agents.x[agent]
            yOld = agents.y[agent]

            if len(agents.status[agent]) == 0:
                randomMove =True
            elif len(agents.status[agent][0]) < 8: #TODO Change threshold
                randomMove = True
            else:
                randomMove = False

            if randomMove:
                print('random move')
                agents.MoveAgent2(agent)
                agents.agentRange()
                #canvas.move(agentPlot[agent], (agents.x[agent]-xOld) *res/gridSize, (agents.y[agent]-yOld)*res/gridSize)

                #currentCoverage,coveragePosition = agents.CheckCoverage()
                #print("Coverage after {} iterations at agent {}:  ".format(i,agent), currentCoverage)
                # for c in coveragePlot:
                #     canvas.delete(c)
                # coveragePlot = []
                # for iGenerate in range(gridSize):     # Generate animated particles in Canvas 
                #     for jGenerate in range(gridSize):     # Generate animated particles in Canvas 
                #         if (iGenerate,jGenerate) in coveragePosition:
                #             coveragePlot.append( canvas.create_rectangle( (iGenerate)*res/gridSize,                                           
                #                                                 (jGenerate)*res/gridSize,                           
                #                                                 (iGenerate+1)*res/gridSize,                               
                #                                                 (jGenerate+1)*res/gridSize,                               
                #                                                 outline='orange', fill='orange' ))

                #tk.update()
                
            currentStatus = agents.status[agent]
            if not currentStatus:
                continue
            xStatus = currentStatus[0]

            yStatus = currentStatus[1]
            decayStatus = currentStatus[2]
            currentLen = len(xStatus)
            
            cellOverloaded = []
            for agent2 in range(totalAgents):
                if agent2 != agent:
                    compareStatus = agents.status[agent2]
                    if not compareStatus:
                        continue
                    else:
                        compareX = compareStatus[0]

                        compareY = compareStatus[1]
                        compareDecay = compareStatus[2]
                        compareLen = len(compareX)
                        agentFound = False
                        for i in range(currentLen):
                            if agentFound:
                                break
                            for j in range(compareLen):
                                if xStatus[i] == compareX[j] and yStatus[i] == compareY[j] and compareDecay[j] + decayStatus[i] > threshold:
                                    #The agent is not placed optimally
                                    cellOverloaded.append(agent2)
                                    agentFound = True
            
            agents.MoveAgent(agent, cellOverloaded)
            canvas.move(agentPlot[agent], (agents.x[agent]-xOld) *res/gridSize, (agents.y[agent]-yOld)*res/gridSize)

            currentCoverage,coveragePosition = agents.CheckCoverage()
            #print("Coverage after {} iterations at agent {}:  ".format(i,agent), currentCoverage)
            for c in coveragePlot:
                canvas.delete(c)
            coveragePlot = []
            for iGenerate in range(gridSize):     # Generate animated particles in Canvas 
                for jGenerate in range(gridSize):     # Generate animated particles in Canvas 
                    if (iGenerate,jGenerate) in coveragePosition:
                        coveragePlot.append( canvas.create_rectangle( (iGenerate)*res/gridSize,                                           
                                                            (jGenerate)*res/gridSize,                           
                                                            (iGenerate+1)*res/gridSize,                               
                                                            (jGenerate+1)*res/gridSize,                               
                                                            outline='orange', fill='orange' ))

            tk.update()
            if currentCoverage > bestCoverage:
                bestCoverage = currentCoverage
                bestX = agents.x.copy()
                bestY = agents.y.copy()
            #timer.sleep(1)

    
    #print(agents.occupied)
    
    agents.x = bestX
    agents.y = bestY
    agents.agentRange()

    canvas.move(agentPlot[agent], (agents.x[agent]-xOld) *res/gridSize, (agents.y[agent]-yOld)*res/gridSize)

    currentCoverage,coveragePosition = agents.CheckCoverage()
    #print("Coverage after {} iterations at agent {}:  ".format(i,agent), currentCoverage)
    for c in coveragePlot:
        canvas.delete(c)
    coveragePlot = []
    for iGenerate in range(gridSize):     # Generate animated particles in Canvas 
        for jGenerate in range(gridSize):     # Generate animated particles in Canvas 
            if (iGenerate,jGenerate) in coveragePosition:
                coveragePlot.append( canvas.create_rectangle( (iGenerate)*res/gridSize,                                           
                                                    (jGenerate)*res/gridSize,                           
                                                    (iGenerate+1)*res/gridSize,                               
                                                    (jGenerate+1)*res/gridSize,                               
                                                    outline='orange', fill='orange' ))

    tk.update()

    #print("All x",agents.x)        
    #print("All y",agents.y)        

    #Cell overloaded contains coordinates from xStatus,yStatus in which the agent overlaps with another agent.
    #Move the opposite direction of coordinates in cellOverloaded
    print('Done')
    Tk.mainloop(canvas)
            
                    
    


if __name__ == "__main__":
    main()
    
