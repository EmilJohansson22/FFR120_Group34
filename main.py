import numpy as np
import random
import EnviromentClass

def main():
    test = EnviromentClass.Enviroment(10) #Has to be 10 as of now.
    #test.BuildEnviroment()
    test.DeterministicEnviroment()
    print(test.grid)








if __name__ == "__main__":
    main()
