import World
import threading
import time
import random

import os
from sys import argv

os.chdir(os.path.dirname(argv[0]))

from Cli import commandLineArgs
from GridWorld import GridWorld

walls = []
walkable = []
player = []
monster = []
traps = []

mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
#world = GridWorld(fromFile = mapPath, logging = commandLineArgs.logging)
with open(mapPath) as f:
    map = f.readlines()

for i in range(len(map)):
    for j in range(len(map[i])):
        if (map[i][j] == 'W'):
            walls.append((i,j))
        if (map[i][j] == ' '):
            walkable.append((i,j))
        if (map[i][j] == 'M'):
            monster.append((i,j))
        if (map[i][j] == 'A'):
            player.append((i,j))
        if (map[i][j] == 'S'):
            traps.append((i,j))    
            
#print (player)
#print (traps)
#print (monster)
#print (walls)
#print (map[8][19])

#World.render_grid(walls, walkable)

#print (map[3][3])

actions = World.actions

def do_action_player(action):
    if action == actions[0]:
        World.try_move_player(0, -1)
    elif action == actions[1]:
        World.try_move_player(0, 1)
    elif action == actions[2]:
        World.try_move_player(-1, 0)
    elif action == actions[3]:
        World.try_move_player(1, 0)
    else:
        return

def do_action_monster(action):
    if action == actions[0]:
        World.try_move_monster(0, -1)
    elif action == actions[1]:
        World.try_move_monster(0, 1)
    elif action == actions[2]:
        World.try_move_monster(-1, 0)
    elif action == actions[3]:
        World.try_move_monster(1, 0)
    else:
        return


def run():
    time.sleep(1)
    t = 1
    counter = 1
    while True:
        #Taking turns each action between monster and agent
       
        #Take a random action 
        if ((counter % 2) == 0):
            do_action_player(random.choice(actions)) 
        if ((counter % 2) != 0):
            do_action_monster(random.choice(actions))
        #print(counter)
        counter +=1
        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # MODIFY THIS TO SPEED UP OR SLOW DOWN GAME
        time.sleep(0.01)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()