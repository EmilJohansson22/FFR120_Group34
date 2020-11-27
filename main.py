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
    #test.BuildEnviroment()
    test.DeterministicEnviroment()

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



    #print(test.grid)
    #print(test)
    totalAgents = 5
    agents = AgentClass.Agent(totalAgents,test.grid,rangeLength=3)
    #agents.x[0] = 5
    #agents.y[0] = 5
    #agents.x[1] = 6
    #agents.y[1] = 6
    #agents.x[2] = 3
    #agents.y[2] = 3
    agents.GeneratePositions()
    agents.agentRange()
    # print(agents.status)
    # print("A0\n",agents.status[0]) #Gets agent 0 status with x, y and some decay value...
    # print("A1\n",agents.status[1]) #Gets agent 0 status with x, y and some decay value...

    # tmpList = list(zip(*agents.status))
    # print("x\n", tmpList[0])

    agentPlot = []
    for j in range(totalAgents):     # Generate animated particles in Canvas 
        xx = agents.x[j]
        yy = agents.y[j]
        agentPlot.append( canvas.create_oval((xx)*res/gridSize,                                           
                                            (yy)*res/gridSize,                           
                                            (xx+1)*res/gridSize,                               
                                            (yy+1)*res/gridSize,                               
                                            outline=ccolor[2], fill=ccolor[2]) )

    
    
    tk.update()    
    timer.sleep(1)
    
    threshold = 1
    #Test a couple of runs

    #TODO When two agents are on the same spot an error occurs
    for i in range(20):
        print("iteration: ", i)
        for agent in range(totalAgents): ##TODO make the list a permutation of each agent
            print("Agent number\n",agent)
            agents.agentRange()
            xOld = agents.x[agent]
            yOld = agents.y[agent]
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
            tk.update()
            #timer.sleep(3)
    print(agents.occupied)
    tk.update()
    print("All x",agents.x)        
    print("All y",agents.y)        

        #Cell overloaded contains coordinates from xStatus,yStatus in which the agent overlaps with another agent.
        #Move the opposite direction of coordinates in cellOverloaded
    print('Done')
    Tk.mainloop(canvas)
            
                    
        


        

    #I do a change
    


if __name__ == "__main__":
    main()
    
