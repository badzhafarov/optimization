# genetic algorithm for knapsack problem

import random
import collections
import numpy as np
import matplotlib.pyplot as plt


maxWeight = 10000
iterations = 50
maxIndividuals = 45
sizeOfPack = 30 # 9
weights = list(range(2, sizeOfPack*2 + 2, 2)) # 2,20,2

probabilityOfMutation = 0.1

balanceForCrossover = 0.35 # probability [0;1] if random > probability => using crossover
                          #                   if random < probability => using modifiedCrossover1 and modifiedCrossover2

balanceForModifiedCrossover = 0.15 # probability [0;1] if random > probability => using modifiedCrossover1
                                   #                   if random < probability => using modifiedCrossover2

ordinate = []
statics = collections.Counter()


def graph(ordinate_):
    plt.plot(range(1, len(ordinate_) + 1), ordinate_, marker='o')
    plt.title('Knapsack problem')
    plt.xlabel('Iteration')
    plt.ylabel('Worth')
    plt.savefig('knapsack.png', dpi=300)
    plt.xlim(0.5, len(ordinate_) + 1)
    plt.show()

def crossover(a, b):
    statics['crossover']+=1
    solution = []
    solution.extend(a[:int(len(a)/2)])
    solution.extend(b[int(len(a)/2):])
    if random.random() < probabilityOfMutation:
        statics['mutation_in_crossover'] += 1
        statics['mutation'] += 1
        solution[random.randint(0, sizeOfPack-1)] = 1
    return solution

def modifiedCrossover1(a, b, probability1, probability2):
    statics['modifiedCrossover1'] += 1
    if (probability1 + probability2) > 0:
        localProbability1 = probability1 / (probability1 + probability2)
        solution = []
        i = 0
        while len(solution) < len(a):
            r = random.random()
            if r > localProbability1:
                solution.append(b[i])
            else:
                solution.append(a[i])
            i += 1
    else:
        solution = randomSolution()
    return solution

def modifiedCrossover2(a, b, probability1, probability2):
    statics['modifiedCrossover2'] += 1
    if (probability1 + probability2) > 0:
        localProbability1 = probability1 / (probability1 + probability2)
        solution = []
        solution.extend(a[:int(len(a) * localProbability1)])
        solution.extend(a[int(len(a) * localProbability1):])
    else:
        solution = randomSolution()
    return solution




def randomSolution():
    solution = np.zeros((sizeOfPack,))
    numberOfBits = random.randint(0, sizeOfPack - 1)
    i = 0
    while i < numberOfBits:
        positionOfBit = random.randint(0, sizeOfPack - 1)
        solution[positionOfBit] = 1
        i += 1
    return solution

def changeBit(value):
    statics['mutation_in_selection'] += 1
    statics['mutation'] += 1
    positionOfBit = random.randint(0, sizeOfPack - 1)
    value[positionOfBit] = int(not bool(value[positionOfBit]))
    return value


class Individuals:
    def __init__(self, n):
        self.list = []
        i = 0
        while i < n:
            self.list.append(np.zeros((sizeOfPack,), dtype=np.int))
            i += 1
    def initialization(self):
        self.localMax = 0
        for i in self.list:
            self.localSum = 0
            self.f = 0
            while self.f == 0:
                r = int(random.uniform(0, sizeOfPack))
                if i[r] == 0:
                    if (weights[r]+self.localSum <= maxWeight):
                        i[r] = 1
                        self.localSum += weights[r]
                    else:
                        self.f = 1
            if np.dot(i, worth) > self.localMax:
                self.localMax = np.dot(i, worth)
                self.best = i
        self.fitness() #
        ordinate.append(np.dot(self.best, worth))

    def foolishInitialization(self):
        self.localMax = 0
        for i in self.list:
            r = int(random.uniform(0, sizeOfPack))
            i[r] = 1
            if np.dot(i, worth) > self.localMax:
                self.localMax = np.dot(i, worth)
                self.best = i
        self.fitness()
        ordinate.append(np.dot(self.best, worth))

    def fitness(self):
        self.valueOfFitness = []

        for i in self.list:
            if np.dot(i, weights) > maxWeight:
                self.valueOfFitness.append(0)
            else:
                self.valueOfFitness.append(np.dot(i,worth))

        self.localSum = sum(self.valueOfFitness)
        self.valueOfFitness = [i/self.localSum for i in self.valueOfFitness]

    def fitnessSingle(self, value):

        if np.dot(value, weights) > maxWeight:
            return 0
        else:
            return np.dot(value, worth)

    def mutation(self, value):
        probability1_ = random.random()
        probability2_ = random.random()
        if probability1_ < probability2_:
            return changeBit(value)
        if probability1_ < probabilityOfMutation:
            return changeBit(value)
        if probability1_ < probabilityOfMutation*probabilityOfMutation:
            return changeBit(value)


    def getBest(self):
        self.indexOfBest = self.valueOfFitness.index(max(self.valueOfFitness))
        self.best = self.list[self.indexOfBest]
        ordinate.append(np.dot(self.best,worth))

    def getOldIndividuals(self):
        for i in self.list:
            self.setOfNewIndividuals[self.fitnessSingle(i)] = i

    def selection(self):
        keys = list(self.setOfNewIndividuals.keys())
        keys.sort()
        keys.reverse()
        i = 0
        j = 0
        while i+j < maxIndividuals - 2:
            if len(keys) > i:
                k = keys[i]
                self.list[i] = self.setOfNewIndividuals[keys[i]]
                probability_ = random.random()
                if probability_ < probabilityOfMutation:
                    copy = self.setOfNewIndividuals[keys[i]]
                    self.mutation(copy)
                    self.list[i] = self.setOfNewIndividuals[keys[i]]
                i += 1
            else:
                self.mutation(self.setOfNewIndividuals[keys[j]])
                self.list[i] = self.setOfNewIndividuals[keys[j]]
                j+=1
        self.list[maxIndividuals - 1] = self.best


    def new(self):
        i = 0
        self.localCopy = self.list
        self.setOfNewIndividuals = {}
        self.getOldIndividuals()


        while i < maxIndividuals * 2:
            a = random.randint(0, maxIndividuals-1)
            b = random.randint(0, maxIndividuals-1)
            if random.random() > balanceForCrossover:
                self.candidate = crossover(self.localCopy[a], self.localCopy[b])
            elif random.random() > balanceForModifiedCrossover:
                self.candidate = modifiedCrossover1(self.localCopy[a], self.localCopy[b],
                                           self.valueOfFitness[a], self.valueOfFitness[b])
            else:
                self.candidate = modifiedCrossover2(self.localCopy[a], self.localCopy[b],
                                           self.valueOfFitness[a], self.valueOfFitness[b])
            if self.fitnessSingle(self.candidate)>0:
                self.setOfNewIndividuals[self.fitnessSingle(self.candidate)] = self.candidate
                i += 1
        self.selection()


def start():
    i = 0
    b = Individuals(maxIndividuals)
    b.foolishInitialization()
    while  i < iterations - 1:
        b.new()
        b.fitness()
        b.getBest()
        i += 1
    #print(ordinate)



worth = random.sample(list(np.linspace(0, np.pi, num=1000)), sizeOfPack)
worth = [int(100*np.sin(i)) for i in worth]
print(weights)
print(worth)

start()

print('Best solution', ordinate[-1])
print(statics)

graph(ordinate)

