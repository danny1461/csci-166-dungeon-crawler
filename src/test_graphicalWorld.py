from tkinter import *
master = Tk()


Width = 50 # width of each block in grid
(x, y) = (20, 20) # AxB grid parameters
actions = ["up", "down", "left", "right"] #movement actions

board = Canvas(master, width=x*Width, height=y*Width) #display parameters
restart = False

#hard coded dungeon1 map values
player = (2, 17)
monster = (5, 2)
traps = [(7, 8), (7, 11), (10, 8), (10, 11)]
walkable = [(1, 4), (1, 5), (1, 6), (1, 7), (1, 10), (2, 4), (2, 5), (2, 6), (2, 7), (2, 10), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 10), (3, 15), (3, 16), (3, 17), (3, 18), (4, 1), (4, 4), (4, 5), (4, 9), (4, 10), (4, 11), (4, 15), (4, 16), (4, 17), (4, 18), (5, 1), (5, 4), (5, 5), (5, 8), (5, 9), (5, 10), (5, 11), (5, 15), (5, 16), (5, 17), (5, 18), (6, 1), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 15), (6, 16), (6, 17), (6, 18), (7, 1), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 18), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 18), (9, 2), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (10, 2), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 16), (11, 2), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (11, 12), (11, 16), (12, 2), (12, 8), (12, 9), (12, 10), (12, 11), (12, 16), (13, 2), (13, 5), (13, 6), (13, 9), (13, 10), (13, 16), (14, 2), (14, 5), (14, 6), (14, 16), (15, 2), (15, 5), (15, 6), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15), (15, 16), (16, 1), (16, 2), (16, 3), (16, 6), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 11), (17, 12), (17, 13), (18, 1), (18, 2), (18, 3), (18, 11), (18, 12), (18, 13)]
walls = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (1, 0), (1, 1), (1, 2), (1, 3), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (2, 0), (2, 1), (2, 2), (2, 3), (2, 8), (2, 9), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (3, 0), (3, 8), (3, 9), (3, 11), (3, 12), (3, 13), (3, 14), (3, 19), (4, 0), (4, 2), (4, 3), (4, 6), (4, 7), (4, 8), (4, 12), (4, 13), (4, 14), (4, 19), (5, 0), (5, 2), (5, 3), (5, 6), (5, 7), (5, 12), (5, 13), (5, 14), (5, 19), (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 13), (6, 14), (6, 19), (7, 0), (7, 2), (7, 3), (7, 4), (7, 5), (7, 14), (7, 15), (7, 16), (7, 17), (7, 19), (8, 0), (8, 15), (8, 16), (8, 17), (8, 19), (9, 0), (9, 1), (9, 3), (9, 4), (9, 19), (10, 0), (10, 1), (10, 3), (10, 4), (10, 5), (10, 14), (10, 15), (10, 17), (10, 18), (10, 19), (11, 0), (11, 1), (11, 3), (11, 4), (11, 5), (11, 6), (11, 13), (11, 14), (11, 15), (11, 17), (11, 18), (11, 19), (12, 0), (12, 1), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 12), (12, 13), (12, 14), (12, 15), (12, 17), (12, 18), (12, 19), (13, 0), (13, 1), (13, 3), (13, 4), (13, 7), (13, 8), (13, 11), (13, 12), (13, 13), (13, 14), (13, 15), (13, 17), (13, 18), (13, 19), (14, 0), (14, 1), (14, 3), (14, 4), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (14, 17), (14, 18), (14, 19), (15, 0), (15, 1), (15, 3), (15, 4), (15, 7), (15, 8), (15, 9), (15, 10), (15, 17), (15, 18), (15, 19), (16, 0), (16, 4), (16, 5), (16, 7), (16, 8), (16, 9), (16, 10), (16, 17), (16, 18), (16, 19), (17, 0), (17, 9), (17, 10), (17, 14), (17, 15), (17, 16), (17, 17), (17, 18), (17, 19), (18, 0), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (19, 16), (19, 17), (19, 18), (19, 19)]

def render_grid(): 
    global Width, x, walls, walkable, y
    for (j,i) in walkable:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
    for (j,i) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
    for (j,i) in traps:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="green", width=1)
render_grid()


#register what move player should do
def try_move_player(dx, dy):
    global player, x, y, me, restart
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    if((new_x,new_y) == monster):
        print("gotcha monster")
    if ((new_y,new_x) in traps):
        print("player took trap dmg")
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_y, new_x) in walls) :
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)

#register what move player should do
def try_move_monster(dx, dy):
    global monster, x, y, enemy, restart
    if restart == True:
        restart_game()
    new_x = monster[0] + dx
    new_y = monster[1] + dy
    if((new_x,new_y) == player):
        print("gotcha player")
    if ((new_y,new_x) in traps):
        print("monster took trap dmg")
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_y, new_x) in walls) :
        board.coords(enemy, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        monster = (new_x, new_y)



def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)

#reset items , call when a certain condition is met
def restart_game():
    global player, score, me, restart
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

#displaying monster and agent onto grid 
me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="yellow", width=1, tag="me")

enemy = board.create_rectangle(monster[0]*Width+Width*2/10, monster[1]*Width+Width*2/10,
                            monster[0]*Width+Width*8/10, monster[1]*Width+Width*8/10, fill="red", width=1, tag="me")

board.grid(row=0, column=0)

def start_game():
    master.mainloop()