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

#################################################################
def index_square(x,y,sx,sy,width) :
    result = -1
    found = False
    i_square = 0
    if x  == -1 :
        #print("Correction 1 ", file=sys.stderr)
        x = width - 1
    elif  x  == width -1 :
        #print("Correction 2 ", file=sys.stderr)
        x = 0    
    while not found and i_square < len(sx):
        if x == sx[i_square] and y == sy[i_square] :
            found = True
            result = i_square
        i_square = i_square + 1
    return result

########################################################################
def find_adjacentes(x,y,sx,sy,width) :
    result = []
    result.append(index_square(x,y - 1,sx,sy,width)) # H
    #Repliement sur axe des x
    if x +1 == width :
        x = 0
    elif x -1 == -1 :
        x = width - 1    
    result.append(index_square(x + 1,y,sx,sy,width)) #D
    result.append(index_square(x,y + 1,sx,sy,width)) #B    
    result.append(index_square(x -1 ,y,sx,sy,width)) #G
    # En diagonale
    result.append(index_square(x + 1,y - 1,sx,sy,width))
    result.append(index_square(x + 1,y - 1,sx,sy,width))
    result.append(index_square(x - 1,y - 1,sx,sy,width))
    result.append(index_square(x -1 ,y + 1,sx,sy,width))

    nb = 0
    for index in range(len(result)) :
        if result[index] != -1 :
            nb = nb + 1

    return result , nb
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


# Calculer les cases adjacentes de chaque case de la grille

adjacents_squares = []
nb_adjacent_square = []

for n_square in range(nb_squares):
    adjacentes, nb = find_adjacentes(squares_x[n_square],squares_y[n_square],
        squares_x,squares_y,width )
    adjacents_squares.append(adjacentes)
    nb_adjacent_square.append(nb)
    
    #print("Adj de  "+str(n_square)+ " coord = "+str(squares_x[n_square])+ ' '+
    #             "-"+str(squares_y[n_square]), file=sys.stderr)

    #for j in range(len(adjacentes)) :
    #    if adjacentes[j] >= 0 :
    #       #print(" Case = " + str(adjacentes[j]) + "  coord = "+str(squares_x[adjacentes[j]])+ ' '+
    #       "-"+str(squares_y[adjacentes[j]]), file=sys.stderr)   
    #print('-----------------------------------------------',file = sys.stderr)

#Calculer les longueur des segments dans les 4 directions
#Pour chaque case de la grille
adjacents_segment_length = []

for n_square in range(nb_squares):
    adjacentes= adjacents_squares[n_square]
    #print("Passage 1 ", file=sys.stderr)
    directions = []
    for i_dir in range(4):
        #print("Passage 22 ", file=sys.stderr)
        l_dir = 0
        current_square = adjacents_squares[n_square][2 * i_dir]
        while  current_square!= -1 :
            #print("Passage 333 ", file=sys.stderr)
            l_dir = l_dir + 1
            current_square = adjacents_squares[current_square][2 * i_dir]             
        directions.append(l_dir)
        #print("d =  " +str(l_dir), file=sys.stderr)
    adjacents_segment_length.append(directions)
hight_zone = []
low_zone = []

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

    pacs_id_ennemy = [] 
    pacs_x_ennemy = []
    pacs_y_ennemy = []
    pacs_type_id_ennemy = []
    pacs_ability_ennemy = []
    pacs_turns_ennemy  = []

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
            pacs_id_ennemy.append(str(pac_id))
            pacs_ability_ennemy.append(ability_cooldown)
            pacs_turns_ennemy.append(speed_turns_left)

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
    liste_no_square = []

#Création liste des pellets à 10 points

    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        liste_x.append(x)
        liste_y.append(y)
        liste_no_square.append(index_square(x,y,squares_x,squares_y,width))
        liste_value.append(value)
        if value == 10 :
            liste_10.append(i)
#            print("Big "+ str(i)+"  = "+str(x)+ " "+str(y), file=sys.stderr)
        else :
            liste_1.append(i)
#            print("Small "+ str(i)+"  = "+str(x)+ " "+str(y), file=sys.stderr)    
    nb_big_pellet = len(liste_10)
    nb_small_pellet = len(liste_1)

    # Attribuer les pellets aux pacs
    
    liste_adj = []
    for n_pac in range(nb_mine_pacs):
        squares_H = []
        squares_D = []
        squares_B = []
        squares_G = []
        adjs = []
        adjs.append(squares_H)
        adjs.append(squares_B)
        adjs.append(squares_B)
        adjs.append(squares_G)
        liste_adj.append(adjs)

        found = False    
#        recherche des distance maxi ds chaque direction des pac
        #print(" Passsage 1", file=sys.stderr
        i_square = pacs_square_index[n_pac]
        for i_dir in range(4) :
            l = adjacents_segment_length[n_pac][i_dir]
            if l > 0 :
                i_pellet = 0
                while i_pellet < nb_small_pellet :
                    square_pellet = liste_1[i_pellet]

                    if pacs_x[n_pac] == liste_x[square_pellet] or pacs_x[n_pac] == liste_x[square_pellet] :
                        # Le pac et le pellet sont sur une meme ligne ou une meme colonne
                        
                        print(" Pellet "+str(i_pellet), file=sys.stderr)
                        print(" Case Pellet "+str(square_pellet), file=sys.stderr)
                        found = False

                        if i_dir == 0  and  pacs_x[n_pac] == liste_x[square_pellet]: #Haut
                            # On recherche si le pellet est ds le segment haut du pac
                            i_segment = 0
                            while not found and i_segment < l :
                                y = pacs_y[n_pac] - 1
                                if y == liste_y[square_pellet] :
                                    found = True
                                    liste_adj[n_pac][0].append(square_pellet)
                                    print(" En haut du pac", file=sys.stderr)
                                else :
                                    i_segment = i_segment + 1

                        elif i_dir == 1  and  not found and pacs_y[n_pac] == liste_y[square_pellet]: #Haut
                            # On recherche si le pellet est ds le segment droite du pac
                            i_segment = 0
                            while not found and i_segment < l :
                                x = pacs_x[n_pac] + 1
                                if x == liste_x[square_pellet] :
                                    found = True
                                    liste_adj[n_pac][1].append(square_pellet)
                                    print(" A droite du pac", file=sys.stderr)
                                else :
                                    i_segment = i_segment + 1
                        elif i_dir == 2  and  not found and pacs_x[n_pac] == liste_x[square_pellet]: #Haut
                            # On recherche si le pellet est ds le segment Bas du pac
                            i_segment = 0
                            while not found and i_segment < l :
                                y = pacs_y[n_pac] + 1
                                if y == liste_y[square_pellet] :
                                    found = True
                                    liste_adj[n_pac][2].append(square_pellet)
                                    print(" A droite du pac", file=sys.stderr)
                                else :
                                    i_segment = i_segment + 1
                        elif i_dir == 3  and  not found and pacs_y[n_pac] == liste_y[square_pellet]: #Haut
                            # On recherche si le pellet est ds le segment gauche du pac
                            i_segment = 0
                            while not found and i_segment < l :
                                x = pacs_x[n_pac] - 1
                                if x == liste_x[square_pellet] :
                                    found = True
                                    liste_adj[n_pac][3].append(square_pellet)
                                    print(" A droite du pac", file=sys.stderr)
                                else :
                                    i_segment = i_segment + 1
                    i_pellet = i_pellet + 1


 # La liste des pellets visible de chaque pac pour chacune des 4 directions
 # Nous renseigne sur les palets diparus dans chaque direction et maj
 # la liste des cases non explored squares_not_explored
  #  print(" Boucle ", file=sys.stderr)
    for n_pac in range(nb_mine_pacs) :
 #       print(" Boucle 1", file=sys.stderr)
        for i_direct in range(4) :
#            print(" Boucle 11", file=sys.stderr)
            l = adjacents_segment_length[n_pac][i_direct]
            if l > 0 :
                liste =liste_adj[n_pac][i_direct]
 #               print(" l = "+str(l), file=sys.stderr)
 #               print("Pac : " +str(n_pac)+" Dir : "+str(i_direct)+" nb vus = " +str(len(liste)), file=sys.stderr)





 #-----------------------------------------------------------------------
 #----------------------------------------------------------------------       

    
    positions = [] 
    for i in range(nb_mine_pacs) :
        positions.append('')

#Analyse des pacs ennemy dans le champ de vision
#Associer à mes pacs les pacs ennemy visibles

    
    pacs_mutant = []
    for n_pac in range(nb_mine_pacs) :
        pacs_mutant.append('')

    for n_pac in range(nb_mine_pacs) :
        print(" ability  de " + str(n_pac)+ " = " +str(pacs_ability[n_pac]), file=sys.stderr)
        if pacs_ability[n_pac] == 0:
            for n_pac_ennemy in range(nb_ennemy_pacs) :
                win = -1
                print(" Passage = ", file=sys.stderr)
                print(" Cord :"+str( pacs_x[n_pac]) + ' '+ str( pacs_y[n_pac]), file=sys.stderr)
                print(" Cord :"+str( pacs_x_ennemy[n_pac_ennemy]) + ' '+ str( pacs_y_ennemy[n_pac_ennemy]), file=sys.stderr)
                if pacs_x[n_pac] == pacs_x_ennemy[n_pac_ennemy]  or pacs_y[n_pac] == pacs_y_ennemy[n_pac_ennemy]:
                    win = compare_strength(pacs_type_id[n_pac],
                        pacs_type_id_ennemy[n_pac_ennemy])
                    print(" Win = " +str(win), file=sys.stderr)
        
                mutation = False        
                if  win > 0 :
                    pacs_mutant[n_pac] = increase_strength(pacs_type_id[n_pac])
                    mutation = True 
                if  win == 2:
                    pacs_mutant[n_pac] = increase_strength(pacs_mutant[n_pac])
                    mutation = True 

                if mutation:
                    pacs_affectation[n_pac] = True   

#Analyse des colisions entre mes pacs

    blocked = []
    #print(" Passage ", file=sys.stderr)
    for n_pac in range(nb_mine_pacs) :
        blocked.append(False)

    nb_blocked = 0
    blocked_1 = -1
    blocked_2 = -1
    if len(liste_cdes) > 0:
    #Ce n'est pas le premier tour    m
        for n_pac in range(nb_mine_pacs) :
            if pacs_x[n_pac] == old_x[n_pac]  and pacs_y[n_pac] == old_y[n_pac] :
                if not old_speeded[n_pac] and old_pacs_mutant[n_pac] == '' :
                    blocked[n_pac] = True
                    if blocked_1 == -1:
                        blocked_1 = n_pac
                    else :
                        blocked_2 = n_pac    
                    nb_blocked = nb_blocked + 1

        print(" Nb bloqué " +str(nb_blocked), file=sys.stderr)
        #for k in range(len(adjacents_squares)) :
        #            print(" Adj = " +str(len(adjacents_squares[k])), file=sys.stderr)



        if nb_blocked > 1:
            #On a les 2 index des pacs qui se bloquent

            #No de la case du pac
            i_square_1 = index_square(pacs_x[blocked_1],pacs_y[blocked_1],squares_x,squares_y,width) 
            adj_1 = adjacents_squares[i_square_1]
    
            i_square_2 = index_square(pacs_x[blocked_2],pacs_y[blocked_2],squares_x,squares_y,width) 
            adj_2 = adjacents_squares[i_square_2]
 
            print(" Pack " +str(blocked_1), file=sys.stderr)
            print(" Coord " +str(pacs_x[blocked_1]) + " " + str(pacs_y[blocked_1]), file=sys.stderr)

            for k in range(8) :
                if adj_1[k] > -1 :
                    print(" Adj = " +str(adj_1[k]), file=sys.stderr)
                    print(" x = " +str(squares_x[adj_1[k]]), file=sys.stderr)
                    print(" y = " +str(squares_y[adj_1[k]]), file=sys.stderr)


            print(" -------------------------------------------" , file=sys.stderr)
            for k in range(8) :
                if adj_2[k] > -1 :
                    print(" Adj = " +str(adj_2[k]), file=sys.stderr)
                    print(" x = " +str(squares_x[adj_2[k]]), file=sys.stderr)
                    print(" y = " +str(squares_y[adj_2[k]]), file=sys.stderr)

            #Recherche de la case de conflit
            found = False
            n_square = 0
            while not found and n_square < 8 :
                if adj_1[n_square] > 0 and  adj_1[n_square] in adj_2:
                    found = True
                else:
                    n_square = n_square +1 

            if found :
                print(" Trouve 1 = ", file=sys.stderr)
                n_square_fight = adj_1[n_square]
            else:
                found = i_square_1 in adj_2
                print(" Trouve 2 = ", file=sys.stderr)
                if found :
                    n_square_fight = i_square_1 
                else :
                    found = i_square_2 in adj_1
                    print(" Trouve 3 = ", file=sys.stderr)
                    if found :
                        n_square_fight = i_square_2  

                                      
            if found :
                print(" Case fight = " +str(n_square_fight), file=sys.stderr)
                print(" x = " +str(squares_x[n_square_fight]), file=sys.stderr)
                print(" y = " +str(squares_y[n_square_fight]), file=sys.stderr)

            #Pour resoudre le conflit 
            # Le pac qui a le moins de case adjacente continue  sur
            # la case de conflit
            if nb_adjacent_square[i_square_1] > nb_adjacent_square[i_square_2] :
                i_square_1,i_square_2 = i_square_2,i_square_1
                blocked_1,blocked_2 = blocked_2,blocked_1
                adj_1,adj_2 = adj_2,adj_1

            x = squares_x[i_square_1]
            y = squares_y[i_square_1]

            pacs_affectation[blocked_1] = True   
            position = str(x) + " " + str(y)
            positions[blocked_1] = position
            print("afectation DEBLOC 1 No" +str(blocked_1) + " " + position +" " , file=sys.stderr)

            #L'autre pack doit choisir une autre case :
            # La première case de fuite différente de la case de conflit
            # Il faudrait verifier si elle est libre

            found = False
            i_square_2 = 0
            while not found and i_square_2 < 8:
                if  adj_2[i_square_2] != -1 and adj_2[i_square_2] != i_square_1:
                    found = True
                else :
                    i_square_2 = i_square_2 + 1

            if found :
                x = squares_x[i_square_2]
                y = squares_y[i_square_2]
                pacs_affectation[blocked_2] = True   
                position = str(x) + " " + str(y)
                positions[blocked_2] = position
                print("afectation DEBLOC 2 No" +str(blocked_2) + " " + position +" " , file=sys.stderr)

#------Acceleration des pacs
    speeded = [] 
    for i in range(nb_mine_pacs) :
        speeded.append(False)

    if not all_affected(pacs_affectation) :
        #print("  PASSAGE -", file=sys.stderr)
        for n_pacs in range(nb_mine_pacs):
            #print("Ability " + str(pacs_ability[n_pacs])  , file=sys.stderr)
            if not pacs_affectation[n_pacs] and pacs_ability[n_pacs] == 0 :
                speeded[n_pacs] = True
                pacs_affectation[n_pacs] = True
                print("Speed sur " + str(n_pacs)  , file=sys.stderr)

###################################################################################

    # Calcul des positions ou envoyer chaque pacs pas encore affecté 
    big_affectations = []
    for n in range(nb_big_pellet) :
        big_affectations.append(False)

    small_affectations = []
    for n in range(nb_small_pellet) :
        small_affectations.append(False)


    #Afecter d"abord les big pellets au pacs sans emploi
    while not all_affected(big_affectations)  and not all_affected(pacs_affectation):
        d_mini = 10000   
    
        for i in range(nb_mine_pacs) :
            if  not pacs_affectation[i] :
                for j in range(nb_big_pellet):
                    if  not big_affectations[j] :
                        index_pellet = int(liste_10[j])
                        d = compute_dist(pacs_x[i],pacs_y[i],
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
                
    #Affecter a chaque pac un pellet dans ces listes de pellet adjacente
    if not all_affected(pacs_affectation):
        for i_pac in range(nb_mine_pacs):
            # recherche de la direction ds laquelle il voit le plus de pellet
            if not pacs_affectation[i_pac] :
                print("Test pac No" +str(i_pac) , file=sys.stderr)
                nb_maxi_seen_pellet = 0
                dir_max = 0
                for i_dir in range(4):
                    n_len = len(liste_adj[i_pac][i_dir])
                    if n_len > nb_maxi_seen_pellet :
                        nb_maxi_seen_pellet = n_len
                        dir_max =i_dir

                if nb_maxi_seen_pellet > 0:

                    #On va vers le premier de la liste (donc le plus près) la plus longue
                    x =  squares_x[liste_adj[i_pac][dir_max][0]]
                    y =  squares_y[liste_adj[i_pac][dir_max][0]]
                    pacs_affectation[i_pac] = True    
                    position = str(x) + " " + str(y)
                    positions[i_pac] = position
                    print("afectation visibles  Pac No" +str(i_pac) + " " + position  , file=sys.stderr)
            
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
                 d = compute_dist(pacs_x[n_pac],pacs_y[n_pac],
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
            print("afectation restantes " +str(n_pac) + " " + position +" " , file=sys.stderr)
            
        n_pac = n_pac + 1
            
# Envoi ds la ligne de commmande d'un ordre par pac :  move de déblocage ou move normal  ou speed
    n_pac = 0
    liste_cdes = []
    pacs_objectif = []

    commandes = ""
    while n_pac < nb_mine_pacs :
        if  positions[n_pac] != '':
            commandes = commandes + "MOVE "+mine_pacs[n_pac]+" "+positions[n_pac]
            #print(" Choix " + positions[i], file=sys.stderr)
            pacs_objectif.append(positions[n_pac])
            liste_cdes.append('M')
            
        elif speeded[n_pac] :
            commandes = commandes + "SPEED "+mine_pacs[n_pac]
            liste_cdes.append('SP') 
        elif pacs_mutant[n_pac] != '':
            commandes = commandes + "SWITCH "+mine_pacs[n_pac]+" "+ pacs_mutant[n_pac]
            liste_cdes.append('SP') 

        if  n_pac < nb_mine_pacs -1:
            commandes= commandes +"|"
        n_pac = n_pac + 1

# envoi sur la sortie de la ligne de commandes
    print(commandes)
    
#Sauvgardes des infos des pacs avant  application des commandes du tour
    old_nb_mine = nb_mine_pacs
    i  = 0
    old_id = []
    old_x  = []
    old_y  = []  
    old_speeded = []
    old_pacs_mutant = []

    while i < old_nb_mine :
        old_id.append(mine_pacs[i])
        old_x.append(pacs_x[i])
        old_y.append(pacs_y[i])
        old_speeded.append(speeded[i])
        old_pacs_mutant.append(pacs_mutant[i])
        i = i+ 1        

   # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # MOVE <pacId> <x> <y>
    #print("MOVE 0 15 15")
