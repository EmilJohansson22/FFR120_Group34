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
    agents.agentRange(2)
    print(agents.status)


if __name__ == "__main__":
    main()
