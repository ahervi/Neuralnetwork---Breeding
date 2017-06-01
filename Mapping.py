# coding: utf-8

from math import *
from collections import deque, namedtuple

DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)

def expo(x):
    return ((exp(-x)-exp(-32))/(exp(-1)-exp(-32)))

#renvoie un tableau de taille 34*34*4 correspondant aux inputs du rĂŠseau de neurones Ă  partir du board
#parcours de la grille dans le sens de la lecture
def mappingAvecMur(board, snake):
    BOARD_LENGTH=len(board)
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
    
    #mur supĂŠrieur
    for i in range(BOARD_LENGTH+2):
        input+=obstacle
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)
    
    for i in range(BOARD_LENGTH):        
        input += obstacle  #mur de gauche
        for j in range(BOARD_LENGTH):
            if board[i][j] == 0 :
                input += vide
            elif board[i][j] == 1:
                if [i,j] == head:
                    input += tete
                else:                    
                    input += obstacle
            elif board[i][j] == 2:
                input += pomme
        input += obstacle  #mur de droite
    
    #mur infĂŠrieur
    for i in range(BOARD_LENGTH+2):
        input+=obstacle
        
    return input 

def mappingSansMur(board, snake):
    BOARD_LENGTH=len(board)
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
    
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    for i in range(BOARD_LENGTH):        
        for j in range(BOARD_LENGTH):
            if board[i][j] == 0 :
                input += vide
            elif board[i][j] == 1:
                if [i,j] == head:
                    input += tete
                else:
                    input += obstacle
            elif board[i][j] == 2:
                input += pomme
        
    return input 

""" Creer une liste de 11 inputs entre 0 et 1 de la maniere suivante
    1:  distance(tete, pomme) selon l'axe des x
    2:  distance(tete, pomme) selon l'axe des y  
    3 a 5:  Si corps sur la gauche : [distance(tete,corps),0,0]
            Si pomme sur la gauche : [0,distance(tete,pomme),0]
            Si mur sur la gauche: [0,0,distance(tete,mur)]
    6 a 8: idem mais devant
    9 a 11: idem mais sur la droite
    distance(tete,X) est calcule de facon à ce que l'input vale 1 si la distance entre la tete et X 
    est nulle et 0 si elle est de BOARD_LENGTH pixel : distance(tete,X) = 1-(|X-tete|/BOARD_LENGTH)"""

def mappingBis(board, snake):
    BOARD_LENGTH=len(board)
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)
    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    
    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    if currentDirection == DIRECTIONS.Up or currentDirection == DIRECTIONS.Down:
        input.append(1-abs(xTete-X)/BOARD_LENGTH)  #deltaX
        input.append(1-abs(yTete-Y)/BOARD_LENGTH)  #deltaY     
    else :
        input.append(1-abs(yTete-X)/BOARD_LENGTH)  #deltaX
        input.append(1-abs(xTete-Y)/BOARD_LENGTH)  #deltaY  

        
    x=xTete
    y=yTete
    trouve = False
    
    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
    


        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        x=xTete
        trouve=False
                
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
         #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[0,0,distance]
        y=yTete
        trouve=False
    
    return input
        

# Crée 7 inputs :
# 4 inputs correspondants à la présence de la pomme dans les 4 carrés autour du snake
# 3 inputs correspondants à la distance tête snake <-> obstacle à G, devant et à D
def mappingCarre(board, snake):
    BOARD_LENGTH=len(board)
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    XRelatif = head[0]-X  #X Relatif
    YRelatif = head[1]-Y  #Y Relatif

    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    x=xTete
    y=yTete
    trouve = False

    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,0]
        elif (XRelatif<0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[distance,distance,0,0]
        elif (XRelatif<0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif>0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,0]
        elif (XRelatif>0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif<0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,distance]

        #Création des 3 inputs
    
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
                
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,0,distance]
        elif (XRelatif<0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[distance,0,0,distance]
        elif (XRelatif<0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif>0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,0,0]
        elif (XRelatif>0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif<0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,distance]

        #Création des 3 inputs

        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
        
    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,0]
        elif (XRelatif<0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[0,0,distance,distance]
        elif (XRelatif<0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif>0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,0]
        elif (XRelatif>0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif<0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,distance,0]

        #Création des 3 inputs

        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,distance,0,0]
        elif (XRelatif<0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[0,distance,distance,0]
        elif (XRelatif<0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif>0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif>0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[0,0,0,distance]
        elif (XRelatif>0 and YRelatif==0):
            distance = 1-(abs(XRelatif))/BOARD_LENGTH
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif<0):
            distance = 1-(abs(XRelatif)+abs(YRelatif))/BOARD_LENGTH
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif<0):
            distance = 1-(abs(YRelatif))/BOARD_LENGTH
            input+=[distance,distance,0,0]

        #Création des 3 inputs

         #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(y-yTete)/BOARD_LENGTH)
            input+=[distance]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/BOARD_LENGTH)
                input+=[distance]
        if not trouve:
            distance = 1-(abs(x-xTete)/BOARD_LENGTH)
            input+=[distance]
        x=xTete
        trouve=False
    
    return input
        

def mappingQLearning(board,snake):
    BOARD_LENGTH=len(board)
    currentDirection = snake.direction
    input = []
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    #Cherche les coordonnees de la pomme
    Xpomme=0
    Ypomme=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                Xpomme=i
                Ypomme=j
                stop=True
                break
        if stop:
             break
    
    XRelatif = head[0]-Xpomme  #X Relatif
    YRelatif = head[1]-Ypomme  #Y Relatif

    input.append(XRelatif)
    input.append(YRelatif)

    if currentDirection==DIRECTIONS.Left :
        if head[0]==0 or board[head[0]-1][head[1]] == 1:
            input.append(0)
        elif board[head[0]-1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[1]+1 ==  BOARD_LENGTH or board[head[0]][head[1]-1] == 1:
            input.append(0)
        elif board[head[0]][head[1]-1] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[1]-1 ==  0 or board[head[0]][head[1]+1] == 1:
            input.append(0)
        elif board[head[0]][head[1]+1] == 2:
            input.append(2)
        else:
            input.append(1)

        return input

    if currentDirection==DIRECTIONS.Right :
        if head[0]+1==BOARD_LENGTH or board[head[0]+1][head[1]] == 1:
            input.append(0)
        elif board[head[0]+1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[1] ==  0 or board[head[0]][head[1]-1] == 1:
            input.append(0)
        elif board[head[0]][head[1]+1] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[1]+1 ==  BOARD_LENGTH or board[head[0]][head[1]+1] == 1:
            input.append(0)
        elif board[head[0]][head[1]-1] == 2:
            input.append(2)
        else:
            input.append(1)

        return input

    if currentDirection==DIRECTIONS.Up :
        if head[1]==0 or board[head[0]][head[1]-1] == 1:
            input.append(0)
        elif board[head[0]][head[1]-1] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[0] ==  0 or board[head[0]-1][head[1]] == 1:
            input.append(0)
        elif board[head[0]-1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[0]+1 ==  BOARD_LENGTH or board[head[0]+1][head[1]] == 1:
            input.append(0)
        elif board[head[0]+1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        return input

    if currentDirection==DIRECTIONS.Down :
        if head[1]+1==BOARD_LENGTH or board[head[0]][head[1]+1] == 1:
            input.append(0)
        elif board[head[0]][head[1]+1] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[0]+1 ==  BOARD_LENGTH or board[head[0]+1][head[1]] == 1:
            input.append(0)
        elif board[head[0]+1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        if head[0] ==  0 or board[head[0]-1][head[1]] == 1:
            input.append(0)
        elif board[head[0]-1][head[1]] == 2:
            input.append(2)
        else:
            input.append(1)

        return input
        

def encoreUnMapping(board, snake):
    BOARD_LENGTH=len(board)
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    XRelatif = head[0]-X  #X Relatif
    YRelatif = head[1]-Y  #Y Relatif

    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    distance=1
    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,0,0,distance]

        #Création des 3 inputs
    
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
                
        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,0,distance,distance]

        #Création des 3 inputs

        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
                
        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
        
    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,distance,distance,0]

        #Création des 3 inputs

        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
            
        #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
        
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
            
        
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,distance,0,0]

        #Création des 3 inputs

         #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
        
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
    
    return input
    



def MappingExponentiel(board, snake):
    BOARD_LENGTH=len(board)
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    XRelatif = head[0]-X  #X Relatif
    YRelatif = head[1]-Y  #Y Relatif

    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    x=xTete
    y=yTete
    distance=1
    trouve = False
    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,0,0,distance]

        #Création des 3 inputs

        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False
                
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,0,distance,distance]

        #Création des 3 inputs

        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False

    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,distance,distance,0]

        #Création des 3 inputs

        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,distance,0,0]

        #Création des 3 inputs


         #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = expo(abs(y-yTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(y-yTete))
            input+=[dist]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = expo(abs(x-xTete))
                input+=[dist]
        if not trouve:
            dist = expo(abs(x-xTete))
            input+=[dist]
        x=xTete
        trouve=False
    
    return input
    
    
def MappingHybride(board, snake):
    BOARD_LENGTH=len(board)
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(BOARD_LENGTH): 
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    XRelatif = head[0]-X  #X Relatif
    YRelatif = head[1]-Y  #Y Relatif

    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    x=xTete
    y=yTete
    distance=1
    trouve = False
    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,0,0,distance]

        #Création des 3 inputs

        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False
                
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False

        #Input Mur
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
                
        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,0,distance]
        elif (XRelatif<0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,distance,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,0,distance,distance]

        #Création des 3 inputs

        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False
        
        #InputMur
        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
                
        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)

    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,0,distance,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,0,distance,distance]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif==0 and YRelatif>0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[distance,0,0,0]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,distance,0,0]
        elif (XRelatif>0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[0,distance,distance,0]

        #Création des 3 inputs

        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False
            
        #InputMur
        #A droite
        if yTete==BOARD_LENGTH-1 or board[xTete][yTete+1]==1:
            input.append(1)
        else:
            input.append(0)
            
        #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
        
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
        #Création des 4 inputs
        if (XRelatif<0 and YRelatif<0):
            input+=[0,distance,0,0]
        elif (XRelatif<0 and YRelatif==0):
            input+=[0,distance,distance,0]
        elif (XRelatif<0 and YRelatif>0):
            input+=[0,0,distance,0]
        elif (XRelatif==0 and YRelatif>0):
            input+=[0,0,distance,distance]
        elif (XRelatif>0 and YRelatif>0):
            input+=[0,0,0,distance]
        elif (XRelatif>0 and YRelatif==0):
            input+=[distance,0,0,distance]
        elif (XRelatif>0 and YRelatif<0):
            input+=[distance,0,0,0]
        elif (XRelatif==0 and YRelatif<0):
            input+=[distance,distance,0,0]

        #Création des 3 inputs


         #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                dist = (1-(abs(y-yTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(y-yTete))/BOARD_LENGTH)
            input+=[dist]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                dist = (1-(abs(x-xTete))/BOARD_LENGTH)
                input+=[dist]
        if not trouve:
            dist = (1-(abs(x-xTete))/BOARD_LENGTH)
            input+=[dist]
        x=xTete
        trouve=False

        #InputMur
        #En bas
        if xTete==BOARD_LENGTH-1 or board[xTete+1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
        
        #A gauche
        if yTete==0 or board[xTete][yTete-1]==1:
            input.append(1)
        else:
            input.append(0)
        
        #En haut
        if xTete==0 or board[xTete-1][yTete]==1:
            input.append(1)
        else:
            input.append(0)
    
    return input
