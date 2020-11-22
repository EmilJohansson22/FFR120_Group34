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
    agents = AgentClass.Agent(2,test.grid)
    agents.x[1] = 2
    agents.y[1] = 2
    agents.agentRange(2)
    #print(agents.status)
    print("A0\n",agents.status[0]) #Gets agent 0 status with x, y and some decay value...
    print("A1\n",agents.status[1]) #Gets agent 0 status with x, y and some decay value...

    #I do a change
    


if __name__ == "__main__":
    main()
