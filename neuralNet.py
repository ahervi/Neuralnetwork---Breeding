# -*- coding: utf-8 -*-

import numpy as np
import math
from layer import Layer


def sigmoid(x):
		return 1 / (1 + math.exp(-0.2*x))


class NeuralNet(object):

	"""NeuralNet est un réseau de neurones, c'est aussi un tableau
	de couches de neurones (layer)
	@param: nbInput1  -> nombre d'input de la couche d'input
			nbOutput1 -> nombre d'outputs de la couche d'input
			nbInput2  -> nombre d'input de la couche d'output
			nbOutput2 -> nombre d'outputs de la couche d'output
	@return: instance de Layer
	"""
	def __init__(self, nbInput1, nbOutput1, nbInput2, nbOutput2):
		inp=Layer(nbInput1, nbOutput1, None, "Input")
		self.layers = [inp,Layer(nbInput2, nbOutput2, inp, "Output")]


	"""Ajoute une layer en avant derniere position
	@param:  nbInput -> nombre d'input de la couche à rajouter
			 nOutput -> nombre d'output de la couche à rajouter
	@return: Void
	"""
	def addLayer(self,nbInput, nbOutput):
		n=len(self.layers)
		add=Layer(nbInput, nbOutput, self.layers[n-2])
		self.layers[n-1].prev=add
		self.layers.insert((n-1),add)


	"""Affiche recursivement les layer en partant des inputs et en remontant
	Necessite un toString des layer 
	@param: //

	@return: Void
	"""
	def display(self):
		def disp(lay):
			if lay.prev==None :
				print (lay.toString())
			else :
				disp(lay.prev)
				print (lay.toString())
		n=len(self.layers)
		disp(self.layers[n-1])


	""" Execute le réseau de neurones avec un tableau d'inputs en entrée
	@param : inp -> tableau des inputs

	@return : tableau des outputs ainsi calculé
	"""
	def run(self,inp):
		n=len(self.layers)

		#Premiere couche
		raw_coeff = np.dot(self.layers[0].coeff,inp)
		for i in range(len(raw_coeff)):
			self.layers[0].output[i] = raw_coeff[i]

		#Pour les autres
		for i in range(1,n):
			self.layers[i].calc()

		#self.layers[n-1].output=[sigmoid(x) for x in self.layers[n-1].output]
		return self.layers[n-1].output


		""" Donne la somme des tailles des matrices coeff des couches du réseau
		et permet d'obtenir la taille requise de l'ADN
		@param : //
		@ return : taille cumulée des matrices coeff
		"""
	def sizeTotale(self) :
		n=len(self.layers)
		size = 0
		for i in range(0,n):
			size+=self.layers[i].size
		return size


	""" Permet de charger les matrices de coeff avec un tableau data d'ADN en entrée
	@param : double[] data
	@return : Void
	"""
	def load(self,data) :
		k=0 	#Permet de parcourir data
		for layer in self.layers :
			for i in range(len(layer.coeff)):
				for j in range(len(layer.coeff[0])):
					layer.coeff[i][j]=data[k]
					k+=1


