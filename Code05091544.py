import sys
import math
import random

# Grab the pellets as fast as you can!

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

#Exploration de la grille pour lister les cases adjacentes à la case
# Atention au cases sur les bords gauches et droite. L'univers se replie

squares_adjacents = []
for i in range(len(squares_x)) :
    neighbours = [] 

    #Case en North
    ok = False
    x_adj = squares_x[i]
    y_adj = squares_y[i] - 1
    if y_adj < 0 :
       neighbours.append(-1)      
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

   #Case en North West
    ok = False
    x_adj = squares_x[i] + 1
    if x_adj == width :
        x_adj = 0
    y_adj = squares_y[i] - 1
    if (y_adj < 0) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

   #Case en West
    ok = False
    x_adj = squares_x[i] + 1
    if x_adj == width :
        x_adj = 0
    y_adj = squares_y[i]
    if (y_adj < 0) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

    #Case en  South West
    ok = False
    x_adj = squares_x[i] + 1
    if x_adj == width :
        x_adj = 0
    y_adj = squares_y[i] + 1

    if (y_adj == height) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

 #Case en  South
    ok = False
    x_adj = squares_x[i] 
    if x_adj == width :
        x_adj = 0
    y_adj = squares_y[i] + 1

    if (y_adj == height) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

#Case en  South Ovest
    ok = False
    x_adj = squares_x[i] - 1
    if x_adj == width :
        x_adj = 0
    y_adj = squares_y[i] + 1

    if (y_adj == height) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

#Case en  Ovest
    ok = False
    x_adj = squares_x[i] - 1
    if x_adj < 0 :
        x_adj = width
    y_adj = squares_y[i]

    if (y_adj == height) :
       neighbours.append(-1)       
    else :
        ok = False
        j = 0
        while not ok and j < len(squares_x):
            if  (x_adj == squares_x[j]) and  (y_adj == squares_y[j]) :
                ok = True
            else:
                j = j + 1
        if ok :
           neighbours.append(j) 
        else :
           neighbours.append(-1) 

    squares_adjacents.append(neighbours)

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
            print(" Nb cases à explorer = "+str(len(squares_not_explored)), file=sys.stderr)
        except:
            pass    

        if mine :
            mine_pacs.append(str(pac_id))
            pacs_x.append(x)
            pacs_y.append(y)
            pacs_ability.append(ability_cooldown)
            pacs_turns.append(speed_turns_left)

    # Recherche des index des cases de maes pacs
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

# Determiner si il y a un pac coincé 
#  x = x prec y = y prec et ordre MOVE
    i = 0
    blocked = []
    while i< len(mine_pacs) :
        blocked.append("")
        i = i +1

    if len(liste_cdes) > 0 : # au 1er round il n'y a pas de cde precedente envoyee

        i = 0
        print("  Nb old = "+ str(old_nb_mine) + " Nb New  = " + str(len(mine_pacs)), file=sys.stderr)
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
                print("  BLOCAGE ------------------------------", file=sys.stderr)
             
            i = i + 1

    print("Test 2", file=sys.stderr)

# Calcul des positions ou envoyer chaque pacs

    positions = [] 
    i = 0
    while i < len(mine_pacs) :
        if  i  < len(liste_10)  :
            j = int(liste_10[i])
            x = int(liste_x[j]) 
            y = int(liste_y[j])
        
        elif len(liste_1) > 0 :                
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
            print("CAS 03", file=sys.stderr)

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
        elif  pacs_ability[i]  > 0:
            commandes = commandes + "MOVE "+mine_pacs[i]+" "+positions[i]
            pacs_objectif.append(position[i])
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
