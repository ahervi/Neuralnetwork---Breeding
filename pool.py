# coding: utf-8

from individu import Individu
from collections import deque
import random
import sys

class Pool():

    """Population de (n) snakes a tester et a croiser
    
    Attributes:
        n (int): Taille de la population
        population (deque): ensemble des N individus de la populations
    """

    def __init__(self, n):
        self.n = n
        self.population = deque()
        for i in range(n):
            self.population.append(Individu())
        self.mutationcoeff = (10/self.getFitnessMoy())
        self.trained = 0
        self.generation = 0
        self.min = 0
        self.moy = 0
        self.max = 0
        

    def breeding(self):
        #remplissage initial de la pool par entraînement des N premiers snakes
        self.trained+=1

        # actualisation du numero de la generation
        if (self.trained % self.n == 0) :
            self.generation += 1
        
        if self.trained < self.n+1:
            return self.population[self.trained-1]
        else:
            # Creation du tableau de croisement
            tab = []
            fitnessMax = self.getFitnessMax()[0]
            self.mutationcoeff = 0.1
            for individu in self.population:
                nb_apparition = int((individu.getFitness() * 100) / fitnessMax)
                for i in range(nb_apparition):
                    tab.append(individu)

            # Choix des deux parents
            index1 = random.randint(0,len(tab)-1)
            index2 = random.randint(0,len(tab)-1)
            
            while(index1 == index2): # eviter d'avoir le meme index
                index2 = random.randint(0,len(tab)-1)
            
            parent1 = tab[index1]
            parent2 = tab[index2]

            # Remplacer l'individu avec le fitness le plus faible par un enfant
            index_pire_indiv = self.getFitnessMin()[1]
            dna_enfant = parent1.dna.crossover(parent2.dna, self.mutationcoeff)
            enfant = Individu(dna_enfant)
            self.population[index_pire_indiv] = enfant

            return enfant
        

    def updateStatistics(self):
        self.min = self.getFitnessMin()[0]
        self.moy = self.getFitnessMoy()
        self.max = self.getFitnessMax()[0]

    
    def getFitnessMax(self):
        fitnessMax = 0
        indexMax = 0
        for i,individu in enumerate(self.population):
            if individu.getFitness() > fitnessMax:
                fitnessMax = individu.getFitness()
                indexMax = i
        return [fitnessMax,indexMax]

    def getFitnessMin(self):
        fitnessMin = sys.maxsize
        indexMin = 0
        for i,individu in enumerate(self.population):
            if individu.getFitness() < fitnessMin:
                fitnessMin = individu.getFitness()
                indexMin = i

        return [fitnessMin,indexMin]

    def getFitnessMoy(self):
        somme = 0
        for individu in self.population:
            somme += individu.getFitness()
        return somme/self.n

    def __str__(self):
        string = ""
        for i in range(self.n):
            string+=(str(self.trained)+" : "+str(self.population[i])+"\n")
        return string

    
"""
#Tests

# Test de la creation du tableau dans breeding
a = Pool(2)
a.population[0].size = 11
print(a.getFitnessMax())
print(a.breeding())
"""
