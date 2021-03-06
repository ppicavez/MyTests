import sys
import math
import random

# Grab the pellets as fast as you can!

def compare_strength (type1,type2) :
    result = 0
    if type1 == "ROCK" :
        if type2 == "SCISSORS" :
            result = 1
        elif type2 == "PAPER":
            result = 2  
    elif type1 == "SCISSORS" :
        if type2 == "ROCK" :
            result = 2
        elif type2 == "PAPER" :
            result = 1
    elif type1 == "PAPER" :
        if type2 == "SCISSORS" :
            result = 2
        elif type2 == "ROCK" :
            result = 1  
    #print( "Compare : " + type1 +" "+type2+" "+str(result), file=sys.stderr)
    return result    

##################################################################################

def increase_strength (type_pac):
    result = ""
    if type_pac == "SCISSORS" :
        result = "ROCK"
    elif type_pac == "PAPER" :
        result = "SCISSORS"
    elif type_pac == "ROCK" :
        result = "PAPER"    
    return result

########################################################################################

def compute_dist(x1,y1,x2,y2,s_x,s_y, width, d_attaque) :
    dist = 0
    delta_x = 0
    delta_y = 0
    if (x1 == x2) :
        dist = abs(y1 -y2)
        delta_y = 1
        if y1 >y2 :
            y1,y2 = y2,y1
    elif (y1 == y2) :
        dist = abs(x1 -x2)
        delta_x = 1
        if x1 >x2 :
            x1,x2 = x2,x1
        if dist == width :
            dist = 1
    else: 
        dist = 10000

    if (dist >1 ) and  (dist < d_attaque) :
        # Verifions qu il n'y a pas de mur entre les 2 coordonnées
        # Parcours des squares entre x1,y1 et x2,y2
        pb = False
        while not pb and (x1 < x2) and (y1 < y2) :

            # Recherche de la case (x1,y1) dans la liste des squares
            found = False
            i = 0
            while not found and (i < len(s_x)) :
                if (x1 == s_x[i])  and (y1 == s_y[i]):
                    found = True
                else :
                    i = i + 1
            pb = not found
            x1 = x1 + delta_x
            y1 = y1 + delta_y

        if pb:
            dist = 10000    
    return dist

########################################################################################

def compute_dist_pellets(x1,y1,x2,y2,s_x,s_y, width, d_attaque) :
    dist = 0
    #print("Coord : "+str(x1)+ " "+str(y1) + " "+str(x2)+ " "+str(y2), file=sys.stderr)

# On privilegie les pelets qui sont en line de mire 
# Meme x ou meme y
    print

    if (x1 == x2) :
        dist = abs(y1 - y2)
    elif y1 == y2 :
        dist = abs(x1 - x2)
        if dist == width :
            dist = 1
    else :
        #print ("Delta " , file=sys.stderr)
        dist = abs(x1 - x2)
        #print ("Dx " +str(dist), file=sys.stderr)
        if dist == width :
            dist = dist + 1
        else:
            dist =dist + abs(y1 - y2)
        #print ("Dy " +str(dist), file=sys.stderr)
    return dist

#############################################################################################

def all_affected(affectations):
    result = True
    for i in range(len(affectations)) :
        result = result and affectations[i]
    return result


###########################################################################################
############################################################################################


k_distance = 5 #Distance mini affrontement pac ennemy

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]

# On stocke dans squares les cases de la grille
squares_x = []
squares_y = []
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    for j in range(width) :
        if row[j] == " ":
            squares_x.append(j)
            squares_y.append(i)

nb_squares = len(squares_x)
squares_not_explored = [] #liste des index des cases de la grille pas encore explorees
                          # par aucun Pac : les miens et les ennemy
for i in range(len(squares_x)) :
    squares_not_explored.append(i)
nb_squares_not_explored = len(squares_not_explored)

liste_cdes = []
old_id = []
old_x  = []
old_y  = []     
old_nb_mine = 0 

# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    mine_pacs = []
    pacs_x = []
    pacs_y = []
    pacs_ability = []
    pacs_turns  = []
    pacs_type_id = []
    pacs_x_ennemy = []
    pacs_y_ennemy = []
    pacs_type_id_ennemy = []
    pacs_affectation = []
   
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)

        #On retire de la liste des cases non encore explorées celle ou se trouvent des pacs
        j = 0
        ok = False
        while not ok and j < len(squares_x):
            if (squares_x[j] == x) and (squares_y[j] == y):
                ok = True
            else :
                j = j+ 1
        try:        
            squares_not_explored.remove(j)
            nb_squares_not_explored = nb_squares_not_explored
        except:
            pass    

        if mine :
            mine_pacs.append(str(pac_id))
            pacs_x.append(x)
            pacs_y.append(y)
            pacs_ability.append(ability_cooldown)
            pacs_turns.append(speed_turns_left)
            pacs_type_id.append(type_id)
            pacs_affectation.append(False)

        else :
            pacs_x_ennemy.append(x)
            pacs_y_ennemy.append(y)
            pacs_type_id_ennemy.append(type_id)    

    nb_mine_pacs = len(mine_pacs)
    nb_ennemy_pacs = len(pacs_x_ennemy)
    # Recherche des index des cases de mes pacs
    pacs_square_index = []
    for i in range(nb_mine_pacs) :
        ok = False
        j = 0
        while not ok and j < nb_squares :
            if (pacs_x[i] == squares_x[j]) and (pacs_y[i] == squares_y[j]):
                ok = True
            else :
                j = j + 1     
        pacs_square_index.append(j)

    visible_pellet_count = int(input())  # all pellets in sight

    liste_x = []
    liste_y = []
    liste_value = []
    liste_10 =[]
    liste_1 =[]

#Création liste des pellets à 10 points

    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        liste_x.append(x)
        liste_y.append(y)
        liste_value.append(value)
        if value == 10 :
            liste_10.append(i)
            print("Big "+ str(i)+"  = "+str(x)+ " "+str(y), file=sys.stderr)
        else :
            liste_1.append(i)    
    nb_big_pellet = len(liste_10)
    nb_small_pellet = len(liste_1)

   # for i in range(nb_big_pellet) :
   #     j = liste_10[i]
   #     print("Big "+str(i)+ " "+str(j), file=sys.stderr)
   #     print("x = "+str(liste_x[j])+ " y = "+str(liste_y[j]), file=sys.stderr)
    
    # Calcul des positions ou envoyer chaque pacs pas encore affecté 
    positions = [] 
    for i in range(nb_mine_pacs) :
        positions.append('')

    big_affectations = []
    for n in range(nb_big_pellet) :
        big_affectations.append(False)

    small_affectations = []
    for n in range(nb_small_pellet) :
        small_affectations.append(False)

    matrice_d = []

    # Calculer matrice  des distances (pac X big pellet) 
    for i in range(nb_mine_pacs) :
        row = []
        for j in range(nb_big_pellet):
            row.append(10000)
        matrice_d.append(row)

    #Afecter d"abord les big pellets au pacs sans emploi
    while not all_affected(big_affectations)  and not all_affected(pacs_affectation):
        d_mini = 10000   
    
        for i in range(nb_mine_pacs) :
            if  not pacs_affectation[i] :
                for j in range(nb_big_pellet):
                    if  not big_affectations[j] :
                        index_pellet = int(liste_10[j])
                        d = compute_dist_pellets(pacs_x[i],pacs_y[i],
                            liste_x[index_pellet],liste_y[index_pellet],
                            width,squares_x,squares_y,1000)

                        if d < d_mini :
                            d_mini = d
                            i_pac_mini = i
                            j_pellet_mini = j
                            index_pellet_mini = index_pellet

         #La plus petite represente l'allocation optimale du big pelet avec  
        x = int(liste_x[index_pellet_mini]) 
        y = int(liste_y[index_pellet_mini])
        pacs_affectation[i_pac_mini] = True
        big_affectations[j_pellet_mini] = True    
        position = str(x) + " " + str(y)
        positions[i_pac_mini] = position
        print("afectation BIG Pac No" +str(i_pac_mini) + " " + position +" " , file=sys.stderr)
                
    #Affecter les pastilles visibles les plus proches
    if not all_affected(small_affectations)  and not all_affected(pacs_affectation):
        for n_pellet in range(nb_small_pellet) :
            d_mini = 10000
            if not small_affectations[n_pellet]:
                index_pellet = int(liste_1[n_pellet])
                # Tant que il reste des pacs à affecter
                n_pac = 0
                while n_pac <  nb_mine_pacs:
                    if not pacs_affectation[n_pac] :
                        d = compute_dist_pellets(pacs_x[n_pac],pacs_y[n_pac],
                            liste_x[index_pellet],liste_y[index_pellet],
                            width,squares_x,squares_y,1000)
                        #print("d = "+str(d) , file=sys.stderr)
                        if d < d_mini:
                            d_mini = d
                            index_mini = n_pac
                    n_pac = n_pac + 1

                if d_mini < 10000 : # affectation réussie
                    x = int(liste_x[index_pellet]) 
                    y = int(liste_y[index_pellet])
                    pacs_affectation[index_mini] = True
                    small_affectations[n_pellet] = True    
                    position = str(x) + " " + str(y)
                    positions[index_mini] = position
                    print("afectation SMALL  Pac No" +str(i_pac_mini) + " " + position +" " , file=sys.stderr)
                
    # Tant que il reste des pacs à affecter
    n_pac = 0
    while  not all_affected(pacs_affectation) and n_pac <  nb_mine_pacs:
        
            #Recherche dans les pastilles restantes de la grille              
            #On affecte soit la pastille la plus proche
            #Soit une pastille pour répartir les pacs pour couvrir le plus de terrain possible 
        
        while not pacs_affectation[n_pac] :
            d_mini = 10000
            index_mini = 0
            for n_pellet in range(len(squares_not_explored)):
                 #print(" n pellet = "+str(n_pellet) +"/"+str(len(squares_not_explored)), file=sys.stderr)
                 index_pellet = int(squares_not_explored[n_pellet])
                 d = compute_dist_pellets(pacs_x[n_pac],pacs_y[n_pac],
                    squares_x[index_pellet],squares_y[index_pellet],
                    width,squares_x,squares_y,1000)
                 if d <d_mini:
                    d_mini = d
                    index_mini = index_pellet

            x = int(squares_x[index_mini]) 
            y = int(squares_y[index_mini])
            pacs_affectation[n_pac] = True
            position = str(x) + " " + str(y)
            positions[n_pac] = position
            print("afectation restante" +str(i_pac_mini) + " " + position +" " , file=sys.stderr)

        n_pac = n_pac + 1
            
# Envoi ds la ligne de commmande d'un ordre par pac :  move de déblocage ou move normal  ou speed
    i = 0
    liste_cdes = []
    pacs_objectif = []

    commandes = ""
    while i < nb_mine_pacs :
        if  positions[i] != '':
            commandes = commandes + "MOVE "+mine_pacs[i]+" "+positions[i]
            #print(" Choix " + positions[i], file=sys.stderr)
            pacs_objectif.append(positions[i])
            liste_cdes.append('M')
            commandes= commandes +"|"
        i = i + 1

# envoi sur la sortie de la ligne de commandes
    print(commandes)
    
#Sauvgardes des infos des pacs avant  application des commandes du tour
    old_nb_mine = nb_mine_pacs
    i  = 0
    old_id = []
    old_x  = []
    old_y  = []  
    while i < old_nb_mine :
        old_id.append(mine_pacs[i])
        old_x.append(pacs_x[i])
        old_y.append(pacs_y[i])
        i = i+ 1        

   # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # MOVE <pacId> <x> <y>
    #print("MOVE 0 15 15")
