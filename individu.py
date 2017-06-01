# coding: utf-8

from dna import DNA
from neuralNet import NeuralNet

HEALTH_MAX = 32*4
DECAY_RATE = 1
APPLE_REWARD = 100

class Individu:

    def __init__ (self, dna = "null"):
        self.size = 0
        self.casesParcourues = 0
        self.health = HEALTH_MAX
        
        # creation reseau de neuronne de l'individu
        self.reseau = NeuralNet(7,5,5,3)
        
        # creation ADN
        if (dna == "null"):
            self.dna = DNA(self.reseau.sizeTotale())
        else:
            self.dna = dna

        # remplissage des coeff du reseau de neuronne
        self.reseau.load(self.dna.data)

    def getFitness(self):
        return int(APPLE_REWARD * self.size + self.health*APPLE_REWARD/HEALTH_MAX)

    def decay(self):
        self.casesParcourues+=1
        if self.health>1:
            self.health-=DECAY_RATE
            return False
        else:
            return True

    def eat(self):
        self.size+=1
        self.health = HEALTH_MAX

    def __str__(self):
        return str(self.size)+" / "+str(self.health)+" | "+str(self.dna)

"""indi = Individu()
#print(indi.dna.data)
print(len(indi.dna.data))"""
