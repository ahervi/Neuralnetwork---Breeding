# coding: utf-8

from collections import deque, namedtuple
from pool import *
from timeit import default_timer as timer
import random
import pygame
import select
from individu import Individu
from Mapping import *
import csv
import sys
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

speed=500000
BOARD_LENGTH = 32
OFFSET = int(BOARD_LENGTH/2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
POOL_SIZE = 100
IHM = False


DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)




def rand_color():
    return (random.randrange(254)|64, random.randrange(254)|64, random.randrange(254)|64)

class Snake(object):
    """Description:
    
    Attributes:
        color (triplet (int,int,int)): couleur du snake
        deque (deque (double-ended queue, à la fois une pile et une file)): corps du snake
        direction (int dans [0,3]): direction du snake (cf variable globale DIRECTIONS)
        indexDirection (int): ???
        nextDir (deque): pile des directions (FIFO) 
        tailmax (int): taille du snake
        individu (individu): instance d'individu associée à l'instance de Snake
    """
    def __init__(self, direction=DIRECTIONS.Right, point=(OFFSET, OFFSET, (20,120,80)), color=(20,120,80)):
        self.tailmax = 4
        self.direction = direction 
        self.deque = deque()
        self.deque.append(point)
        self.color = color
        self.nextDir = deque()
        self.indexDirection = 2
        self.individu = Individu()
    
    def __str__(self):
        return str(self.tailmax)

    def get_color(self):
        return (20,120,80)
    
    def setIndividu(self, individuPool):
        self.individu = individuPool

    def trad_direction(self, nv_dir):
        """Traduit la direction demandée (relative, 0:gauche, 1: en face 2:droite) 
        en direction absolue (N S W E)
        Merci Agathe!
        
        Args:
            nv_dir (DIRECTION): direction relative
        
        Returns:
            DIRECTION: absolue
        """
        if (self.direction == DIRECTIONS.Up):
            if nv_dir == 0:
                return DIRECTIONS.Left
            if nv_dir == 1:
                return DIRECTIONS.Up
            else:
                return DIRECTIONS.Right

        elif (self.direction == DIRECTIONS.Right):
            if nv_dir == 0:
                return DIRECTIONS.Up
            if nv_dir == 1:
                return DIRECTIONS.Right
            else:
                return DIRECTIONS.Down

        elif (self.direction == DIRECTIONS.Down):
            if nv_dir == 0:
                return DIRECTIONS.Right
            if nv_dir == 1:
                return DIRECTIONS.Down
            else:
                return DIRECTIONS.Left

        elif (self.direction == DIRECTIONS.Left):
            if nv_dir == 0:
                return DIRECTIONS.Down
            if nv_dir == 1:
                return DIRECTIONS.Left
            else:
                return DIRECTIONS.Up


    def populate_nextDir(self, direction):
        """Ajoute la prochaine direction que doit prendre le snake sur une pile (d'où le appendLeft)
        
        Args:
            direction (???): A DEFINIR

        Returns:
            void: ajoute en haut de pile la direction choisie
        """

        self.nextDir.appendleft(direction)
        self.indexDirection+=1

#______________________________________ SCRIPT DU JEU __________________________________


def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
            spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False

def make_board():
    return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]
    

def update_board(screen, snakes, food, pool):
    if IHM:
        rect = pygame.Rect(0, 0, OFFSET, OFFSET)
    
        spots = [[] for i in range(BOARD_LENGTH)]
        num1 = 0
        num2 = 0
        for row in spots:
            for i in range(BOARD_LENGTH):
                row.append(0)
                temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
                pygame.draw.rect(screen, BLACK, temprect)
                num2 += 1
            num1 += 1
        spots[food[0]][food[1]] = 2
        temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
        pygame.draw.rect(screen, rand_color(), temprect)
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
                temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
                pygame.draw.rect(screen, coord[2], temprect)

        # Faire l'affichage des statistiques de la pool
        font = pygame.font.Font(None, 15)
        message_generation = font.render("Generation : " + str(pool.generation), True, WHITE)
        message_maxFitness = font.render("Fitness Max : " + str(pool.getFitnessMax()[0]), True, WHITE)
        message_avgFitness = font.render("Fitness Moyen : " + str(pool.getFitnessMoy()), True, WHITE)
        screen.blit(message_generation, (10, 20)) 
        screen.blit(message_maxFitness, (10, 35))  
        screen.blit(message_avgFitness, (10, 50)) 

        return spots
    else:
        spots=make_board()
        spots[food[0]][food[1]] = 2
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
        return spots

def get_color(s):
    if s == "bk":
        return BLACK
    elif s == "wh":
        return WHITE
    elif s == "rd":
        return RED
    elif s == "bl":
        return BLUE
    elif s == "fo":
        return rand_color()
    else:
        print("WHAT", s)
        return BLUE

# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

    screen.fill(BLACK)
    screen.blit(menu_message1, (32, 32)) 
    screen.blit(menu_message2, (32, 64))
    pygame.display.update()
    while True: 
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1
        if done:
            break
    if done:
        pygame.quit()
        return 0

def quit(screen,pool):
    return False

def move(snake):
    if len(snake.nextDir) != 0:
        next_dir = snake.nextDir.pop()
    else:
        next_dir = snake.direction
    head = snake.deque.pop()
    snake.deque.append(head)
    next_move = head
    if (next_dir == DIRECTIONS.Up):
        if snake.direction != DIRECTIONS.Down:
            next_move =  (head[0] - 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] + 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Down):
        if snake.direction != DIRECTIONS.Up:
            next_move =  (head[0] + 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] - 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Left):
        if snake.direction != DIRECTIONS.Right:
            next_move =  (head[0], head[1] - 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] + 1, snake.get_color())
    elif (next_dir == DIRECTIONS.Right):
        if snake.direction != DIRECTIONS.Left:
            next_move =  (head[0], head[1] + 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] - 1, snake.get_color())
    return next_move

def is_food(board, point):
    return board[point[0]][point[1]] == 2


# Return false to quit program, true to go to
# gameover screen
def play(screen, pool): 
    clock = pygame.time.Clock()
    spots = make_board()
    indexDirection = 0

    #______________________________________ SCRIPT DU BREEDING _____________________________

    snake = Snake()
    snake.setIndividu(pool.breeding())

    #______________________________________ /SCRIPT DU BREEDING ____________________________
    # PUTAING C BO LA SIMPLICITÉ


    # Board set up
    spots[0][0] = 1
    food = find_food(spots)

    while True:
        clock.tick(speed)
        # Event processing
        done = False
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
                break
        if done:
            return False

        #____________________________ DECISION-MAKING _____________________________

        inp = encoreUnMapping(spots, snake)
        snake.populate_nextDir(snake.trad_direction(network_nextDir(snake.individu,inp)))

        #____________________________ /DECISION-MAKING _____________________________

        

        # Game logic
        next_head = move(snake)
        if snake.individu.decay():
            #print("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = 0  \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| MORT NATURELLE \t\t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            logging.debug("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = 0  \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| MORT NATURELLE \t\t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            return snake.tailmax
        
        if (end_condition(spots, next_head)):
            #print("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = "+str(snake.individu.health)+" \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| AFFREUX ACCIDENT \t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            logging.debug("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = "+str(snake.individu.health)+" \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| AFFREUX ACCIDENT \t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            return snake.tailmax
        
        
        
        
        if is_food(spots, next_head):
            snake.tailmax += 1
            snake.individu.eat()
            food = find_food(spots)
        pool.updateStatistics()
        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        screen.fill(BLACK)  # makes screen black

        spots = update_board(screen, [snake], food, pool)

        pygame.display.update()
        # à décommenter pour afficher le Snake 
        # MAIS environ 75% plus lent sur mappingBis 5000 itérations

def network_nextDir(indiv,inp):
    output=indiv.reseau.run(inp)
    def maxIndice(liste):
        indice=0
        max=liste[0]
        for i in range(1,len(liste)):
            if liste[i]>max :
                indice=i
                max = liste[i]
        return indice
    return maxIndice(output)

def sauvegarder(pool, fileName):
    with open(fileName,"w") as file:
        writer = csv.writer(file)
        for i in range(pool.n):
            writer.writerow([pool.population[i].dna.data])
            writer.writerow([pool.population[i].size])
            writer.writerow([pool.population[i].getFitness()])
        file.close()

def sauvegarder_statistiques(pool, fileName, numSnake, fitnessAvg, fitnessMax):
    with open(fileName,"w") as file:
        writer = csv.writer(file)
    
        writer.writerow([numSnake])
        writer.writerow([fitnessAvg])
        writer.writerow([fitnessMax])
        file.close()

def graphique_fitness(numSnake, avgFitness, maxFitness):
    plt.plot(numSnake, avgFitness, label="Fitness moyen")
    plt.plot(numSnake, maxFitness, label="Fitness max")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel('Fitness')
    plt.xlabel("Nombre de snakes")
    plt.show()

def charger(fileName):
    i=0
    pool=Pool(POOL_SIZE)
    pool.trained=POOL_SIZE
    cr = csv.reader(open(fileName,"rU"))
    for row in cr:       
        if len(row)==1:
            pool.population[i].size=int(row[0])
            i+=1
        elif len(row)>1:
            pool.population[i] = Individu()
            for j in range(pool.population[i].reseau.sizeTotale()):
                pool.population[i].dna.data[j]=float(row[j])

    return pool
    
                

def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    message2 = "Press enter to play again, esc to quit."
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, BLACK)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, BLACK)

    overlay = pygame.Surface((BOARD_LENGTH * OFFSET, BOARD_LENGTH * OFFSET))
    overlay.fill((84, 84, 84))
    overlay.set_alpha(150)
    screen.blit(overlay, (0,0))

    screen.blit(game_over_message1, (35, 35))
    screen.blit(game_over_message2, (65, 65))
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, WHITE)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, WHITE)
    screen.blit(game_over_message1, (32, 32))
    screen.blit(game_over_message2, (62, 62))
   
    pygame.display.update()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True
#______________________________________ /SCRIPT DU JEU ________________________________



def main():
    pool = Pool(POOL_SIZE)
    #pool = charger('out.csv')
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
        BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen,pygame.Color(255,255,255,255),pygame.Rect(50,50,10,10))
    first = True
    playing = True
    i=0
    start = timer()
    numSnake = []
    avgFitness = []
    maxFitness = []

    while playing:
        
        i+=1
        if first or pick == 3:
            pick = 1

        options = {0 : quit,
                1 : play}
        now = options[pick](screen,pool)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 1
            #playing = game_over(screen, eaten)
            first = False
        
        numSnake.append(i)
        avgFitness.append(pool.getFitnessMoy())
        maxFitness.append(pool.getFitnessMax()[0])
   
        if pool.trained == 2000:
            graphique_fitness(numSnake, avgFitness, maxFitness)
    
    #sauvegarder(pool,'mappingBis_5.csv')
    #sauvegarder_statistiques(pool,'statistique_mappingBis_5.csv', numSnake, avgFitness, maxFitness)
    end = timer()
    time = end-start
    print(str(time))
    print(str(time/i)+" ms par Snake")
    pygame.quit()

if __name__ == "__main__":
    main()
