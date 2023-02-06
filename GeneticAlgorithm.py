import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from game import game

class GeneticAlgorithm:
    def __init__(self,populationSize,mutationRate,selectionRate,crossoverRate,numberOfWeights):       
        self.population = []
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.selectionRate = selectionRate
        self.crossoverRate = crossoverRate
        self.numberOfWeights = numberOfWeights
        self.populationFitness = [] #number of wins for each individual
        self.unseenPopulation = []
        self.nextGeneration = []

    def createPopulation(self):
        for i in range(self.populationSize):
            self.population.append(self.createIndividual())
    
    def createIndividual(self):
        return [random.randint(0,10) for i in range(self.numberOfWeights)]
    
    def getRandomIndividual(self):
        if len(self.unseenPopulation) == 0:
            return None
        index = random.randint(0,len(self.unseenPopulation)-1)
        individual = self.unseenPopulation[index]
        self.unseenPopulation.pop(index)
        return individual
         

    def simulate(self,numberOfGames):
        for _ in range(numberOfGames):
            self.unseenPopulation = self.population.copy()
            while len(self.unseenPopulation) != 0:
                ai1 = self.getRandomIndividual()
                ai2 = self.getRandomIndividual()

                winner = self.play(ai1,ai2)
                if winner == 1:
                    self.populationFitness[self.population.index(ai1)] += 1
                elif winner == 2:
                    self.populationFitness[self.population.index(ai2)] += 1
                else:
                    self.populationFitness[self.population.index(ai1)] += 0.5
                    self.populationFitness[self.population.index(ai2)] += 0.5

    def play(self,ai1,ai2):
        g = game(6,7)
        winner = g.AIvsAI(ai1,ai2,'Genetic')
        del g
        return winner

    def selection(self):
        fitnessMappping = {}
        for i in range(self.populationSize):
            fitnessMappping[i] = self.populationFitness[i]
        fitnessMappping = sorted(fitnessMappping.items(), key=lambda x: x[1], reverse=True)
        for i in range(self.populationSize*self.selectionRate):
            self.nextGeneration.append(self.population[fitnessMappping[i][0]])
        
    def crossoverIndividuals(self,parent1,parent2):
        child = []
        for i in range(self.numberOfWeights):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def crossover(self):
        for i in range(self.populationSize*self.crossoverRate):
            parent1 = random.choice(self.nextGeneration)
            parent2 = random.choice(self.nextGeneration)
            child = self.crossoverIndividuals(parent1,parent2)
            self.nextGeneration.append(child)

    def mutation(self):
        for i in range(self.populationSize*self.mutationRate):
            individual = random.choice(self.nextGeneration)
            index = random.randint(0,self.numberOfWeights-1)
            individual[index] += random.randint(-2,2)
            self.nextGeneration.append(individual)

    def oneGeneration(self):
        self.nextGeneration = []
        self.populationFitness = [0 for i in range(self.populationSize)]
        self.simulate(4)
        self.selection()
        self.crossover()
        self.mutation()
        self.population = self.nextGeneration.copy()
        print(max(self.populationFitness))

    def run(self,numberOfGenerations):
        self.createPopulation()
        for i in range(numberOfGenerations):
            self.oneGeneration()
        
        self.saveGeneration()
    
    def saveGeneration(self):
        df = pd.DataFrame(self.population)
        df.to_csv('generation.csv',index=False)
    
    def loadGeneration(self):
        df = pd.read_csv('generation.csv')
        self.population = df.values.tolist()
    def bestIndividual(self):
        fitnessMappping = {}
        for i in range(self.populationSize):
            fitnessMappping[i] = self.populationFitness[i]
        fitnessMappping = sorted(fitnessMappping.items(), key=lambda x: x[1], reverse=True)
        bestIndividual = self.population[fitnessMappping[0][0]]
        return bestIndividual

def main():
    ga = GeneticAlgorithm(populationSize=100,mutationRate=0.2,selectionRate=0.5,crossoverRate=0.3,numberOfWeights=42)
    ga.run(100)
    ga.saveGeneration()
    print(ga.bestIndividual())
