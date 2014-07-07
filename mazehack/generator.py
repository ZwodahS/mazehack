"""
This method generate a maze, and stores it in a 2D "array"
"""
from random import randint, choice

from mazedef import is_passable, get_time, is_curved, set_passable, get_direction_mod, in_range, change_direction, opposite_direction_of
from mazedef import NORTH, SOUTH, EAST, WEST

PROBABILITY_CHANGE_DIRECTION = 5 # base chance for changing direction
PROBABILITY_SPAWN = 5
"""
Modified from 
http://www.emanueleferonato.com/2008/12/08/perfect-maze-generation-tile-based-version-as3/
"""
def generate_maze(x, y, config={}):
    structure = []
    for i in range(x): 
        structure.append([0]*y)

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
        print(pos) 
        if pos_x + 2 < x and not is_passable(structure[pos_x + 2][pos_y]):
            possible_directions.append(EAST)
        if pos_x - 2 > 0 and not is_passable(structure[pos_x - 2][pos_y]):
            possible_directions.append(WEST)
        if pos_y + 2 < y and not is_passable(structure[pos_x][pos_y + 2]):
            possible_directions.append(SOUTH)
        if pos_y - 2 > 0 and not is_passable(structure[pos_x][pos_y - 2]):
            possible_directions.append(NORTH)
        print(possible_directions)
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
    return maze
