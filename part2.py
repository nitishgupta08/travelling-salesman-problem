## Solving the Travelling Salesman Problem using
## simulated annealing
import random
import math
import matplotlib.pyplot as plt

class SimulatedAnnealingTSP:

    def __init__(self):
        self.cities = list()
                
    def simulatedAnnealing(self):
        
        # Read input from files and append them to
        # the cities list
        f = open('input.txt','r')
        n = int(f.readline())
        # N = list(range(1,21))
        cord = f.read().split('\n')
        xcord = []
        for i in cord[0].split():
            xcord.append(float(i))
        ycord = []
        for i in cord[1].split():
            ycord.append(float(i))
        cordn = []
        cordn.append(xcord)
        cordn.append(ycord)
            
        for i in range(len(cordn[0])):
            self.cities.append((cordn[0][i],cordn[1][i]))
   
        # Tempreature and cooling ratefor annealing    
        temprature = 1000
        coolingRate = 0.01
        iterations = 0 
        maxIterations = 10000

        # Generate a random Path
        randomPath = self.randomPath(n) 
        currentPath = randomPath.copy()
        bestPath = randomPath.copy()
        minCost = self.heuristic(bestPath) 
        
       
        while temprature > 0.0001 or iterations < maxIterations:
            
            # Swapping any of the two positions in the new path to
            # generate a new path
            newPath = currentPath.copy()
    
            position1 = round((len(newPath) - 1) * random.random())
            position2 = round((len(newPath) - 1) * random.random())
            newPath[position1],newPath[position2] = newPath[position2],newPath[position1]
            
            # Compute heurestic value of current and new Path
            currentEnergy = self.heuristic(currentPath)
            newEnergy = self.heuristic(newPath)
 
            # Checks for acceptance 
            if self.acceptanceProbability(currentEnergy, newEnergy, temprature) > random.random():
                currentPath = newPath.copy()

            # Checks if the new path is more optimal than
            # the old one
            if self.heuristic(currentPath) < minCost:
                minCost = self.heuristic(currentPath)
                bestPath = currentPath.copy()

            temprature *= (1 - coolingRate)
            iterations += 1
            
            if iterations in range(1,maxIterations,500):
                self.updateGraph(currentPath,currentEnergy,iterations)
        
        if minCost < currentEnergy:
            self.updateGraph(bestPath,minCost,iterations)

        return (bestPath,minCost)
        
   
    # Determine the probability and accept
    # the path with higher probability
    def acceptanceProbability(self, curr, new, T):
        if new < curr: 
            return 1
        return math.exp(-abs(curr - new)/T)
        
    # Euclidean distance between two points         
    def distance(self, x, y):
        xCord = abs(x[0] - y[0])
        yCord = abs(x[1] - y[1])
        return math.sqrt((xCord*xCord) + (yCord*yCord))

    # Calculates cost of a path
    def heuristic(self, path):
        cost = 0
        for i in range(len(path)):
            city1 = path[i]
            if i + 1 < len(path):
                city2 = path[i + 1]
            else:
                city2 = path[0]
            cost += self.distance(city1, city2)
        return cost

    # # This will generate a random path
    # for simulated annealing
    def randomPath(self,n):
        cities = list(range(n))
        path = []                                                 
        for i in range(n):
            city = cities[random.randint(0, len(cities) - 1)]
            path.append(self.cities[city])
            cities.remove(city)
        return path
      
    # The graph is updated after every iteration
    def updateGraph(self,path,cost,iteration):
        plt.cla()
        print(f"Iteration number: {iteration} and Cost: {cost:.3f}")
        xCords = list()
        yCords = list()
        copyPath = path.copy()
        copyPath.append(path[0])
        for coords in copyPath:
            xCords.append(coords[0])
            yCords.append(coords[1])
        plt.scatter(xCords, yCords,color='m')
        plt.plot(xCords,yCords,color='m')
        title = f'Iteration number: {iteration}'
        title = title + '           ' + f'Cost: {cost:.3f}'
        plt.title(title)
        plt.pause(0.1)
        


tsp = SimulatedAnnealingTSP()
results = tsp.simulatedAnnealing()


