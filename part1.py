## Solving the Travelling Salesman Problem using the
## steepest accent variation of hill climbing algorithm
import random
import math
import matplotlib.pyplot as plt


# Given all the co-ordinates of the cities 
# we will first generate a Matrix that represents
# distance between any two cities
def generateMatrix(xcord,ycord,n):
    tsp = []
    for i in range(n):
        row = []
        for j in range(n):
            if j == i:
                row.append(0)
            elif j < i:
                row.append(tsp[j][i])
            else:
                distance = math.sqrt((xcord[i]-xcord[j])**2 + (ycord[i]-ycord[j])**2)
                row.append(distance)
        tsp.append(row)
    return tsp
                
        
# The idea is to generate a random path
# and then optimise it
def randomPath(n):
    cities = list(range(n))
    path = []                                                 
    for i in range(n):
        city = cities[random.randint(0, len(cities) - 1)]
        path.append(city)
        cities.remove(city)
    return path


# Cost of every path calculated using the
# TSP matrix
def heuristic(tsp,path):
    cost = 0
    for i in range(len(path)):
        cost += tsp[path[i-1]][path[i]]  
    return cost


# Get varients of the random path 
# to find the path with the best reward
# In this case path with least cost
def generateVarients(path):
    varients = []
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            varient = path.copy()
            varient[i] = path[j]
            varient[j] = path[i]
            varients.append(varient)
    return varients


# Get the varient with minimum cost
def getBestVarient(tsp, varients):
    # set 0th index to best past and then
    # compare it remaining varients
    minPathCost = heuristic(tsp, varients[0])
    bestVarient = varients[0]
    for varient in varients:
        varientPathCost = heuristic(tsp, varient)
        if varientPathCost < minPathCost:
            minPathCost = varientPathCost
            bestVarient = varient
    return bestVarient, minPathCost


# The graph is updated after every iteration
def updateGraph(path,cost,iteration):
    plt.cla()
    plt.scatter(xcord,ycord,color='m')
    x = []
    y = []
    for i in path:
        x.append(xcord[i])
        y.append(ycord[i])
    x.append(xcord[path[0]])
    y.append(ycord[path[0]])
    if iteration == 0:
        title = 'Final Solution'
    else:
        title = f'Iteration number: {iteration}'
    title = title + '           ' + f'Cost: {cost:.3f}'
    plt.title(title)
    plt.plot(x,y,color='m')
    plt.pause(0.001)
        

# This solution is not optimal, as number of nodes increase
# the while loop may get stuck at local maximum or a plateu
# and may not even return a path.
def hillClimbing(tsp,n):
    currentPath = randomPath(n)
    currentPathCost = heuristic(tsp, currentPath)
    updateGraph(currentPath,currentPathCost,1)
    print(f'Path: {currentPath},Cost: {currentPathCost:.3f}, Iteration: {1}')
    varients = generateVarients(currentPath)
    bestVarient, minPathCost = getBestVarient(tsp, varients)
    i = 1
    data = []
    # Continue this till we find the best vairent
    while minPathCost < currentPathCost:
        currentPath = bestVarient
        currentPathCost = minPathCost        
        varients = generateVarients(currentPath)
        bestVarient, minPathCost = getBestVarient(tsp, varients)
        updateGraph(bestVarient,minPathCost,i)
        i += 1
        print(f'Path: {bestVarient},Cost: {minPathCost:.3f}, Iteration: {i}')
        data.append((bestVarient,minPathCost))
    updateGraph(currentPath,currentPathCost,0)
    print(f'Path: {data[-2][0]},Cost: {data[-2][1]:.3f},"FINAL SOLUTION"')
    return currentPath, currentPathCost


##### Executing the program with a sample input from text file #####

# read input from file
f = open('input.txt','r')
n = int(f.readline())
N = list(range(1,21))
cord = f.read().split('\n')
xcord = []
for i in cord[0].split():
    xcord.append(float(i))
ycord = []
for i in cord[1].split():
    ycord.append(float(i))
    
# Creating a scatter plot with
# all the coordinates  in input file
plt.show()
plt.scatter(xcord,ycord,color='m')
    
tsp = generateMatrix(xcord,ycord,n)
bestpath, mincost = hillClimbing(tsp,n)
plt.show()


