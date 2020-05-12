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
    visible_pellet_count = int(input())  # all pellets in sight

    liste_x = []
    liste_y = []
    liste_value = []
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        liste_x.append(x)
        liste_y.append(y)
        liste_value.append(value)

    print("Nb of Pelet" +str(len(liste_x)), file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # MOVE <pacId> <x> <y>
    #print("MOVE 0 15 15")

    again = True
    x = int(liste_x[0])
    y = int(liste_y[0])
    i = 1
    while again and i <visible_pellet_count :
        if int(liste_value[i]) > 1 :
            again = False
        else :
            i = i + 1

    if again :
        i = random.randrange(visible_pac_count)

    x = int(liste_x[i]) 
    y = int(liste_y[i])
    
    position = str(x) + " " + str(y) 
    print("MOVE 0 "+position)
    
