# -*- coding: utf-8 -*-

import numpy as np
import math
from neuralNet import NeuralNet

""" Crée et initialise un réseau de neurones à 3 Hidden Layers
@param : coeff1 -> matrice des coefficients de la couche d'Input
		 coeff2 -> matrice des coefficients de la première Hidden Layer
		 coeff3 -> matrice des coefficients de la deuxième Hidden Layer
		 coeff4 -> matrice des coefficients de la troisième Hidden Layer
		 coeff5 -> matrice des coefficients de la couche d'Output
@return : un NeuralNet prêt à être utilisé
"""
def initialize():
	network = NeuralNet(4624,1156,12,3)
	network.addLayer(1156,300)
	network.addLayer(300,70)
	network.addLayer(70,12)
	return network



test=initialize()

tableauInputs = 4624*[1]

tableauOutputs = test.run(tableauInputs)


test.run(4624*[1])
test.display()
