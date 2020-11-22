import numpy as np
import random
import EnviromentClass
import AgentClass

def main():
    test = EnviromentClass.Enviroment(10) #Has to be 10 as of now.
    #test.BuildEnviroment()
    test.DeterministicEnviroment()
    #print(test.grid)
    #print(test)
    totalAgents = 2
    agents = AgentClass.Agent(totalAgents,test.grid)
    agents.x[1] = 2
    agents.y[1] = 2
    agents.agentRange(2)
    # print(agents.status)
    # print("A0\n",agents.status[0]) #Gets agent 0 status with x, y and some decay value...
    # print("A1\n",agents.status[1]) #Gets agent 0 status with x, y and some decay value...

    # tmpList = list(zip(*agents.status))
    # print("x\n", tmpList[0])
    threshold = 1
    for agent in range(totalAgents): ##TODO make the list a permutation of each agent
        currentStatus = agents.status[agent]
        xStatus = currentStatus[0]
        yStatus = currentStatus[1]
        decayStatus = currentStatus[2]
        currentLen = len(xStatus)
        cellOverloaded = []
        for agent2 in range(totalAgents):
            if agent2 != agent:
                compareStatus = agents.status[agent2]
                compareX = compareStatus[0]
                compareY = compareStatus[1]
                compareDecay = compareStatus[2]
                compareLen = len(compareX)
                for i in range(currentLen):
                    for j in range(compareLen):
                        if xStatus[i] == compareX[j] and yStatus[i] == compareY[j] and compareDecay[j] + decayStatus[i] > threshold:
                            #The agent is not placed optimally
                            cellOverloaded.append(i)

        #Cell overloaded contains coordinates from xStatus,yStatus in which the agent overlaps with another agent.
        #Move the opposite direction of coordinates in cellOverloaded

            
            
                    
        


        

    #I do a change
    


if __name__ == "__main__":
    main()
