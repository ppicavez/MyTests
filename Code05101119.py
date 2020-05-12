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
    print( "Compare : " + type1 +" "+type2+" "+str(result), file=sys.stderr)
    return result    

def increase_strength (type_pac):
    result = ""
    if type_pac == "SCISSORS" :
        result = "ROCK"
    elif type_pac == "PAPER" :
        result = "SCISSORS"
    elif type_pac == "ROCK" :
        result = "PAPER"    
    return result


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

def all_pacs_affected(affectations):
    result = True
    for i in range(len(affectations)) :
        result = result and affectations[i]
    return result

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


squares_not_explored = [] #liste des index des cases de la grille pas encore explorees
                          # par aucun Pac : les miens et les ennemy
for i in range(len(squares_x)) :
    squares_not_explored.append(i)

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
        except:
            pass    

        if mine :
            mine_pacs.append(str(pac_id))
            pacs_x.append(x)
            pacs_y.append(y)
            pacs_ability.append(ability_cooldown)
            pacs_turns.append(speed_turns_left)
            pacs_type_id.append(type_id)

        else :
            pacs_x_ennemy.append(x)
            pacs_y_ennemy.append(y)
            pacs_type_id_ennemy.append(type_id)    

    # Recherche des index des cases de mes pacs
    pacs_square_index = []
    for i in range(len(mine_pacs)) :
        ok = False
        j = 0
        while not ok and j < len(squares_x) :
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
        else :
            liste_1.append(i)    

# Determiner si il y a des pac coincé 
#  x = x prec y = y prec et ordre MOVE
    i = 0
    blocked = []
    while i< len(mine_pacs) :
        blocked.append("")
        pacs_affectation.append(False)
        i = i +1

    if len(liste_cdes) > 0 : # au 1er round il n'y a pas de cde precedente envoyee

        i = 0
        
        while i< len(mine_pacs) :
            #recherche de l'identifant : il y a pu changer d'indice ds le tableau si 
            # un pac a été mangé au tour précédent
            j = 0
             
            index_ok = False
            while not index_ok and j<old_nb_mine  : 
                if old_id[j] == mine_pacs[i] :
                    index_ok = True
                else :    
                    j =  j + 1
            if index_ok and (liste_cdes[j] == 'M') and (old_x[j] ==pacs_x[i]) and (old_y[j] == pacs_y[i]) :
                # Calculer les positions de deblocage
                # Envoyer sur une case au hazard  de la grille
                j = random.randrange(len(squares_not_explored)) 
                j = squares_not_explored[j]
                x = squares_x[j]
                y = squares_y[j]    
                blocked[i] = str(x) + ' '+ str(y)
                pacs_affectation[i] = True
                print("  BLOCAGE ------------------------------", file=sys.stderr)
             
            i = i + 1

    # Gestion des pacs ennemy visibles
    pacs_action = []
    pacs_param = []
    for i in range(len(pacs_x)) :
        pacs_action.append("")
        pacs_param.append("")

    if (len(pacs_x_ennemy) > 0) and not all_pacs_affected(pacs_affectation) :
        
        for j in range(len(pacs_x)) : 
            print("Mine : "+mine_pacs[j] +" "+pacs_type_id[j], file=sys.stderr)   
            pacs_distance = []
            pacs_winner  = []
            pacs_type = []
            d_mini = 100

            for i in range(len(pacs_x_ennemy)) :
                d = compute_dist(pacs_x[j],pacs_y[j], pacs_x_ennemy[i],pacs_y_ennemy[i],
                    squares_x,squares_y, width, k_distance)

                winner = compare_strength(pacs_type_id[j],pacs_type_id_ennemy[i])

                if d < d_mini :
                   d_mini = d
                  
                pacs_distance.append(d)
                pacs_winner.append(winner)
                pacs_type.append(pacs_type_id_ennemy[i])

            # Parcours des pac ennemy les + proches
            print("D mini = "+str(d_mini), file=sys.stderr)
            nb_winner0 = 0
            nb_winner1 = 0
            nb_winner2 = 0
            if d_mini < k_distance :
                for k in range(len(pacs_distance)) :
                    if pacs_distance[k] == d_mini :
                        print("Winner = "+str(pacs_winner[k]), file=sys.stderr)
                        print("Type = "+str(pacs_type[k]), file=sys.stderr)
                        if pacs_winner[k] == 0:
                            nb_winner0 = nb_winner0 + 1
                        elif pacs_winner[k] == 1:
                            nb_winner1 = nb_winner1 + 1
                        elif pacs_winner[k] == 2:
                            nb_winner2 = nb_winner2 + 1

            # Si l'un des ennemy est eliminable on fait rien  ( A voir)
            if (d_mini < k_distance) and (nb_winner1 == 0) :
                #Les ennemy sont plus forts ou égaux       
                #on devient plus fort
                pacs_action[j] ='SWITCH'
                pacs_param[j] = increase_strength(pacs_type_id_ennemy[i])
                print("SWITCH", file=sys.stderr) 
                pacs_affectation[j] = True   

    
    # On regarde s'il reste des pacs à affecter

    # Calcul des positions ou envoyer chaque pacs
    positions = [] 
    
#On s'occupe des groses pastilles d'abord
#    for i in range(len(pacs_x)) :
 #       positions.add('')

#    for n in range(len(liste_10)) :
#        # associer le pac le plus proche qui n'est ni bloqué ni en cours de transformation
#        found = False



    i = 0
    while i < len(mine_pacs) :
         # Associer  les premiers pack avec la grosse pastille la plus proche

        if  i  < len(liste_10)  :
            j = int(liste_10[i])
            x = int(liste_x[j]) 
            y = int(liste_y[j])
        
        elif len(liste_1) > 0 : 
            # Associer  le pac avec les pastille qu'il a dans sa ligne de mire



            k = random.randrange(len(liste_1))
            j =int(liste_1[k]) 
            #recherche si il y a un pellet à coté
            found = False
            n = 0
            while not found and n < len(liste_1):
                # Calcule distance entre pellet j et pac i
                index = liste_1[n]
                if (abs(liste_x[index] -pacs_x[i]) <2 ) and (abs(liste_y[index] -pacs_y[i]) <2):
                    j = n
                    x = int(liste_x[j]) 
                    y = int(liste_y[j])
                    found = True
                n = n + 1
        else:
            # pas de pastille visible,
            j = random.randrange(len(squares_not_explored)) 
            j = squares_not_explored[j]
            x = squares_x[j]
            y = squares_y[j]

        position = str(x) + " " + str(y)

        #Vérifier doublons
        #while  position in positions :
        #    j = random.randrange(len(squares_not_explored)) 
        #    j = squares_not_explored[j]
        #    x = squares_x[j]
        #    y = squares_y[j]
        #    position = str(x) + " " + str(y)
        #   print("CAS 04", file=sys.stderr)

        positions.append(position)
        i = i + 1 

# Envoi ds la lgne de commmande d'un ordre par pac :  move de déblocage ou move normal  ou speed
    i = 0
    liste_cdes = []
    pacs_objectif = []

    commandes = ""
    while i < len(mine_pacs) :
        if blocked[i] != "" :
            commandes = commandes + "MOVE "+mine_pacs[i]+" "+ blocked[i]
            pacs_objectif.append('')
            liste_cdes.append('M')
        elif pacs_action[i] != "" : 
            commandes = commandes + pacs_action[i] + " " + mine_pacs[i] + " " + pacs_param[i]
            pacs_objectif.append(positions[i])
            liste_cdes.append(pacs_action[i][0])

        elif  pacs_ability[i]  > 0:
            commandes = commandes + "MOVE "+mine_pacs[i]+" "+positions[i]
            pacs_objectif.append(positions[i])
            liste_cdes.append('M')
        else :
            commandes = commandes + "SPEED "+mine_pacs[i]
            pacs_objectif.append('') 
            liste_cdes.append('S')
        if i < len(mine_pacs) - 1 :
            commandes= commandes +"|"
        i = i + 1

# envoi sur la sortie de la ligne de commandes
    print(commandes)
    
#Sauvgardes des infos des pacs avant  application des commandes du tour
    old_nb_mine = len(mine_pacs)
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
