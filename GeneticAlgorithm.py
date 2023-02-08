import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from game import game


# main class for genetic algorithm that that simulates games and creates new generations 
class GeneticAlgorithm:
    def __init__(self,populationSize,mutationRate,selectionRate,crossoverRate,numberOfWeights):       
        self.population = []
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.selectionRate = selectionRate
        self.crossoverRate = crossoverRate
        self.numberOfWeights = numberOfWeights
        self.populationFitness = [] 
        self.unseenPopulation = []
        self.nextGeneration = []

    # function to create the initial population
    def createPopulation(self):
        for i in range(self.populationSize):
            self.population.append(self.createIndividual())
    
    #create random individual  
    def createIndividual(self):
        return [random.randint(0,10) for i in range(self.numberOfWeights)]
    
    # get random individual from unseen population
    def getRandomIndividual(self):
        if len(self.unseenPopulation) == 0:
            return None
        index = random.randint(0,len(self.unseenPopulation)-1)
        individual = self.unseenPopulation[index]
        self.unseenPopulation.pop(index)
        return individual
         
    # simulate games and set fitness of each individual with the number of wins
    def simulate(self,numberOfGames):
        for i in range(numberOfGames):
            print('round: ',i+1)
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

    # play a game between two individuals and return the winner
    def play(self,ai1,ai2):
        g = game(6,7)
        winner = g.AIvsAI(ai1,ai2,'Genetic')
        del g
        return winner

    # select the best individuals to the next generation according to selection rate
    def selection(self):
        fitnessMappping = {}
        for i in range(self.populationSize):
            fitnessMappping[i] = self.populationFitness[i]
        fitnessMappping = sorted(fitnessMappping.items(), key=lambda x: x[1], reverse=True)
        for i in range(int(self.populationSize*self.selectionRate)):
            self.nextGeneration.append(self.population[fitnessMappping[i][0]])
        print('best of generation: ',self.population[fitnessMappping[i][0]])
    
    # crossover between two individuals and return the child
    def crossoverIndividuals(self,parent1,parent2):
        child = []
        for i in range(self.numberOfWeights):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    # make crossover children for next generation
    def crossover(self):
        for i in range(int(self.populationSize*self.crossoverRate)):
            parent1 = random.choice(self.nextGeneration)
            parent2 = random.choice(self.nextGeneration)
            child = self.crossoverIndividuals(parent1,parent2)
            self.nextGeneration.append(child)

    # mutate individuals in next generation
    def mutation(self):
        for i in range(int(int(self.populationSize*self.mutationRate))):
            individual = random.choice(self.nextGeneration)
            index = random.randint(0,self.numberOfWeights-1)
            individual[index] += random.randint(-2,2)
            self.nextGeneration.append(individual)

    # move population to next generation
    def oneGeneration(self):
        self.nextGeneration = []
        self.populationFitness = [0 for i in range(self.populationSize)]
        self.simulate(3)
        self.selection()
        self.crossover()
        self.mutation()
        self.population = self.nextGeneration.copy()

    # run the genetic algorithm for number of generations
    def run(self,numberOfGenerations,train='new'):
        if train == 'new':
            self.createPopulation()
        else:
            self.loadGeneration()
        for i in range(numberOfGenerations):
            print('gen: ',i+1)
            self.oneGeneration()
            self.saveGeneration()
        
    # save the current generation to csv file
    def saveGeneration(self):
        df = pd.DataFrame(self.population)
        df.to_csv('generation.csv',index=False)
    
    # load generation from csv file
    def loadGeneration(self):
        df = pd.read_csv('generation.csv')
        self.population = df.values.tolist()

    # return the best individual of the current generation according to fitness
    def bestIndividual(self):
        fitnessMappping = {}
        for i in range(self.populationSize):
            fitnessMappping[i] = self.populationFitness[i]
        fitnessMappping = sorted(fitnessMappping.items(), key=lambda x: x[1], reverse=True)
        bestIndividual = self.population[fitnessMappping[0][0]]
        return bestIndividual

# main function to run the genetic algorithm
def main(train='new'):
    ga = GeneticAlgorithm(populationSize=100,mutationRate=0.2,selectionRate=0.5,crossoverRate=0.3,numberOfWeights=7)
    ga.run(10,train)
    ga.saveGeneration()
    print(ga.bestIndividual())


if __name__ == '__main__':
    main('new')