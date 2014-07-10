"""
This method generate a maze, and stores it in a 2D "array"
"""
from random import randint, choice

from mazedef import is_wall, set_wall, get_direction_mod, in_range, change_direction, opposite_direction_of
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
            l.append(1)
        structure.append(l)

    maze = {
        "x" : x, 
        "y" : y,
        "structure" : structure,
    }

    starting_pos_x = randint(1, x-2)
    if not starting_pos_x % 2:
        starting_pos_x -= 1
    starting_pos_y = randint(1, y-2)
    if not starting_pos_y % 2:
        starting_pos_y -= 1
    pos = (starting_pos_x, starting_pos_y)
       
    moves = [] 
    moves.append(pos)
    
    while len(moves) > 0 :
        possible_directions = []
        pos_x, pos_y = pos
        if pos_x + 2 < x and is_wall(structure[pos_x + 2][pos_y]):
            possible_directions.append(EAST)
        if pos_x - 2 > 0 and is_wall(structure[pos_x - 2][pos_y]):
            possible_directions.append(WEST)
        if pos_y + 2 < y and is_wall(structure[pos_x][pos_y + 2]):
            possible_directions.append(SOUTH)
        if pos_y - 2 > 0 and is_wall(structure[pos_x][pos_y - 2]):
            possible_directions.append(NORTH)
        if(len(possible_directions)):
            direction = choice(possible_directions)
            direction_x, direction_y = get_direction_mod(direction)
            target_x, target_y = (pos_x + direction_x, pos_y + direction_y)
            set_wall(maze, target_x, target_y, False)
            target_x, target_y = (target_x + direction_x, target_y + direction_y)
            set_wall(maze, target_x, target_y, False)
            pos = (target_x, target_y)
            moves.append(pos)
        else:
            pos = moves.pop()
    
    random_x, random_y = get_random_passable_position(maze["x"], maze["y"])
    maze.update({ "start_x" : random_x, "start_y" : random_y })

    return maze

# get a random spot on the maze that is ALWAYS PASSABLE
def get_random_passable_position(x, y):
    random_x = randint(1, x-1)
    random_y = randint(1, y-1)
    if not random_x % 2 :
        random_x -= 1
    if not random_y % 2 :
        random_y -= 1

    return random_x, random_y

def get_random_variable_position(x, y):
    random_x = randint(1, x-2)
    random_y = randint(1, y-2)
    # if both are even or both are odd, then we randomly decrease one of them
    if not (random_x + random_y) % 2 :
        if random_x == 1 :
            random_y -= 1
        elif random_y == 1:
            random_x -= 1
        else:
            choice = randint(0, 1)
            if choice:
                random_x -= 1
            else:
                random_y -= 1

    return random_x, random_y

