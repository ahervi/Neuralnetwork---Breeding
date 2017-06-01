# coding: utf-8

import random

class DNA():
    
    def __init__(self, taille):       
        self.data=[]
        for i in range(taille):
            self.data.append(random.random()*2-1)

    def crossover(self, ADN2, mutationcoeff):
        new_adn = DNA(len(self.data))
        for i in range(len(self.data)):
            if (i%2 == 0):
                newcoeff = self.data[i]
            else:
                newcoeff = ADN2.data[i]
        
            if (random.random() < mutationcoeff):
                #print("mutation au rang " + str(i))
            
                hasard = random.randint(0,1)
                changement = newcoeff*0.15

                if hasard == 0:
                    if (newcoeff + changement) > 1:
                        newcoeff = 1
                    else:
                        newcoeff += changement
                else:
                    if (newcoeff - changement) < -1:
                        newcoeff = -1
                    else:
                        newcoeff -= changement

            new_adn.data[i] = newcoeff 
        return(new_adn)

    def __str__(self):
        return str(len(self.data))

"""adn1 = DNA(5714020)
adn2 = DNA(5714020)
#print(adn1.data)
#print(adn2.data)
new_adn = adn1.crossover(adn2.data,0.3)
#print(new_adn.data)"""
