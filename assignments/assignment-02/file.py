import numpy as np
import random
import operator
import pandas as pd


class Fitness:
    def __init__(self, route, data):
        self.route = route
        self.data  = data
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        pathDistance = 0
        for i in range(len(self.route)):
            if i == 0 or i == (len(self.route)-1):
                continue
            else:
                j = self.route[i-1]
                k = self.route[i]
                pathDistance += self.data[j][k]
        self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness



def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route



def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))

    return population



def rankRoutes(population, data):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i], data).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

# The fitness of each individual relative to the population is used to assign a probability of selection. Think of this as the fitness-weighted probability of being selected.

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults



def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool



def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children



def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual



def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop



def nextGeneration(currentGen, eliteSize, mutationRate, data):
    popRanked = rankRoutes(currentGen, data)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, data):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop, data)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, data)
    
    print("Final distance: " + str(1 / rankRoutes(pop, data)[0][1]))
    bestRouteIndex = rankRoutes(pop, data)[0][0]

    bestRoute = pop[bestRouteIndex]
    return bestRoute


if __name__ == "__main__":

    with open("input.txt") as f:
        numbers = "0123456789"
        finalList = []
        lines = f.readlines()
        for i in range(len(lines)):
            lst = []
            corp = lines[i].split(" ")
            for j in corp:
                if len(j)> 0 and j[0] in numbers:
                    lst.append(int(j))
            finalList.append(lst)  
    cityList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    data = finalList
    final = geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500, data=data)
    
    distance_total = 0
    for i in range(len(cityList)):
        if i == 0 or i == (len(cityList)-1):
            continue
        else:
            j = final[i-1]
            k = final[i]
            distance_total += data[j][k]
    # print(final)
    print("Route Will be following:")
    for i in final:
        print("City "+str(i+1))