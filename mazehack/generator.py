"""
This method generate a maze, and stores it in a 2D "array"
"""
from random import randint, choice

from mazedef import is_passable, get_time, is_curved, set_passable, get_direction_mod, in_range, change_direction, opposite_direction_of
from mazedef import NORTH, SOUTH, EAST, WEST
"""
Modified from 
http://www.emanueleferonato.com/2008/12/08/perfect-maze-generation-tile-based-version-as3/
"""
def generate_maze(x, y, config={}):
    structure = []
    for i in range(x): 
        l = []
        for j in range(y):
            # l.append(randint(1, 5) << 1)
            l.append(6)
        structure.append(l)

    maze = {
        "x" : x, 
        "y" : y,
        "structure" : structure,
    }

    back = 0
    move = 0
    starting_pos_x = randint(0, x-1)
    if not starting_pos_x % 2:
        starting_pos_x -= 1
    starting_pos_y = randint(0, y-1)
    if not starting_pos_y % 2:
        starting_pos_y -= 1
    pos = (1, 1)
       
    moves = [] 
    moves.append(pos)
    
    while len(moves) > 0 :
        possible_directions = []
        pos_x, pos_y = pos
        if pos_x + 2 < x and not is_passable(structure[pos_x + 2][pos_y]):
            possible_directions.append(EAST)
        if pos_x - 2 > 0 and not is_passable(structure[pos_x - 2][pos_y]):
            possible_directions.append(WEST)
        if pos_y + 2 < y and not is_passable(structure[pos_x][pos_y + 2]):
            possible_directions.append(SOUTH)
        if pos_y - 2 > 0 and not is_passable(structure[pos_x][pos_y - 2]):
            possible_directions.append(NORTH)
        if(len(possible_directions)):
            direction = choice(possible_directions)
            direction_x, direction_y = get_direction_mod(direction)
            target_x, target_y = (pos_x + direction_x, pos_y + direction_y)
            set_passable(structure, target_x, target_y, True)
            target_x, target_y = (target_x + direction_x, target_y + direction_y)
            set_passable(structure, target_x, target_y, True)
            pos = (target_x, target_y)
            moves.append(pos)
        else:
            pos = moves.pop()

    if "holes" in config:
        value = config["holes"]
        for i in range(0, value):
            random_x = randint(1, x -2)
            random_y = randint(1, y -2)
            set_passable(maze["structure"], random_x, random_y, True)
    while True:
        random_x = randint(1, x -1)
        random_y = randint(1, y -1)
        if is_passable(structure[random_x][random_y]) :
            maze.update({ "start_x" : random_x, "start_y" : random_y })
            break

    return maze
