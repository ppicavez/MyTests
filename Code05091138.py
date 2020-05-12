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

        if mine :
            mine_pacs.append(str(pac_id))
            pacs_x.append(x)
            pacs_y.append(y)
            pacs_ability.append(ability_cooldown)
            pacs_turns.append(speed_turns_left)

    visible_pellet_count = int(input())  # all pellets in sight

    liste_x = []
    liste_y = []
    liste_value = []
    liste_10 =[]
    liste_1 =[]

#Création liste des pellets à 10 p"oints

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
                # Envoyer sur une case adjacente libre de la grille
                # case (x  +-1, y +- 1) sana pac propres ni pac ennemey

                #case haut
                if pacs_y[i] - 1 >= 0 :
                   # occupée par un des mes autres pacs ?
                   m = 0
                   ok = False
                   while not ok and m < len[pacs_x]:
                       if  m != i and (pacs_x[m] = pacs_x[i]) and (pacs_y[m] = pacs_y[i] - 1) :
                          ok = True 
                       else :
                           m = m + 1

                   #occupées par un pac ennemy 


                   m = 0
                   ok = False
                   while not ok  and m < len(squares_x):
                       if (squares_x[m] = pacs_x[i]) and (squares_y[m] = pacs_y[i] - 1):
                           # c'est une case de la grille
                           


                       else:     
                            m = m + 1 

                blocked[i] = '!'
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
            j = random.randrange(len(squares_x))
            x = squares_x[j]
            y = squares_y[j]
            print("CAS 01", file=sys.stderr)

        position = str(x) + " " + str(y)

        #Vérifier doublons
        while  position in positions :
            j = random.randrange(len(squares_x))
            x = squares_x[j]
            y = squares_y[j]
            position = str(x) + " " + str(y)
            print("CAS 02", file=sys.stderr)




        positions.append(position)
        i = i + 1 

# Envoi ds la lgne de commmande d'un ordre par pac :  moves ou speed
    i = 0
    liste_cdes = []
    commandes = ""
    while i < len(mine_pacs) :
        if blocked[i] != "" :
          commandes = commandes + "MOVE "+mine_pacs[i]+" "+blocked[i]
           liste_cdes.append('M')  
        elif  pacs_ability[i]  > 0:
          commandes = commandes + "MOVE "+mine_pacs[i]+" "+positions[i]
          liste_cdes.append('M')
        else :
            commandes = commandes + "SPEED "+mine_pacs[i] 
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
