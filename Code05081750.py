import sys
import math
import random

# Grab the pellets as fast as you can!

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall

# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    mine_pacs = []
    encore=plus = True
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
        if mine :
            mine_pacs.append(str(pac_id))
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
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

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # MOVE <pacId> <x> <y>
    #print("MOVE 0 15 15")


    positions = [] 
    i = 0
    while i < len(mine_pacs) :
        if  i  < len(liste_10)  :
            j = int(liste_10[i])
        else :
            k = random.randrange(len(liste_1))
            j =int(liste_1[k]) 
            

        x = int(liste_x[j]) 
        y = int(liste_y[j])
        position = str(x) + " " + str(y)
        positions.append(position)
        print("Position  : " +position, file=sys.stderr)
        i = i + 1 

# Envoi de la lgne de commmande
    i = 0
    commandes = ""
    while i < len(mine_pacs) :
        commandes = commandes + "MOVE "+mine_pacs[i]+" "+positions[i]
        if i < len(mine_pacs) - 1 :
            commandes= commandes +"|"
        i = i + 1

    print(commandes)
    print("Ma commande  : " + commandes, file=sys.stderr)