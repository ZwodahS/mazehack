from random import randint
""" Constants for direction """
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

""" Constants for direction respective to direction"""
FRONT = 0
BACK = 1
RIGHT = 2
LEFT = 3
BELOW = 4
"""
origin is top left
"""
"""
This file contains all the definition used to interpret a int value to see if it passable
or the speed or what kind of "thing" it contains.
"""
"""
right most bit's index is 0
set the bit at index of the original_value to a value
"""
def set_bit(original_value, index, value):
    mask = 1 << index  # create mask
    original_value &= ~mask         # extract everything except the index
    if value:              # if value is 1, then we need to set it to 1
        original_value |= mask
    return original_value
"""
Each int value will be used in the following way
The last bit, will store a bool value storing if it is passable.
The next 3 bit, stores the time value
    max value is 16, 
    return 2^(x-1)

    valid value are 1, 2, 3, 4, 5 == 1, 2, 4, 8, 16

    Time are done in this way for players to able to "deduce" things

The next bit stores if it is a curve value
    Curve is only allowed if
        1. There are only 2 exit to the tile
        2. None of the exit is a door
        3. The exit is NOT opposite of each other (although it makes no different)

XXXXXXXXXXXXXXXXXXXX[data:2][wall:1]
if wall value is 0 then there is no wall
if data is 1, then there is a data in the maze structure 

"""
def is_wall(value):
    return value & 1 > 0

def set_wall(maze, x, y, value):
    newvalue = maze["structure"][x][y] 
    maze["structure"][x][y] = set_bit(maze["structure"][x][y], 0, 1 if value else 0)
"""
"""

def is_adjacent(pos_x, pos_y, target_x, target_y):
    distance = abs(pos_x - pos_y) + abs(target_x - target_y)
    return distance == 1

def is_passable_from(maze, pos_x, pos_y, target_x, target_y):
    target = maze[target_x][target_y]
    if is_wall(target) :
        return False
    return True

def can_exit(maze, x, y):
    if maze["start_x"] == x and maze["start_y"] == y :
        return True
    return False

def get_direction_mod(direction):
    if direction == NORTH:
        return (0, -1)
    elif direction == SOUTH:
        return (0, 1)
    elif direction == EAST:
        return (1, 0)
    elif direction == WEST:
        return (-1, 0)
    else :
        return (0, 0)

"""
get_direction_of(LEFT, NORTH)
this will return WEST
get_direction_of(BACK, SOUTH)
this will return NORTH
"""
def get_direction_of(relative_direction, direction):
    if relative_direction == FRONT:
        return direction
    elif relative_direction == LEFT:
        if direction == NORTH:
            return WEST
        elif direction == WEST:
            return SOUTH
        elif direction == SOUTH:
            return EAST
        else : #EAST
            return NORTH
    elif relative_direction == RIGHT:
        if direction == NORTH:
            return EAST
        elif direction == EAST:
            return SOUTH
        elif direction == SOUTH:
            return WEST
        else : #WEST
            return NORTH
    else: #BACK
        if direction == NORTH:
            return SOUTH
        elif direction == SOUTH:
            return NORTH
        elif direction == EAST:
            return WEST
        else: #WEST
            return EAST
def get_relative_direction_string(relative_direction):
    if relative_direction == FRONT:
        return "Front"
    elif relative_direction == LEFT:
        return "Left"
    elif relative_direction == RIGHT:
        return "Right"
    else:
        return "Back"

def in_range(maze, x, y):
    return x >= 0 and x < maze["x"] and y >= 0 and y < maze["y"] 

def change_direction(direction):
    i = randint(0, 1)
    if direction == NORTH:
        if i:
            return EAST
        else:
            return WEST
    else:
        if i:
            return NORTH
        else:
            return SOUTH

def opposite_direction_of(direction):
    if direction == NORTH:
        return SOUTH
    elif direction == SOUTH:
        return NORTH
    elif direction == EAST:
        return WEST
    else:
        return EAST

def is_decision_point(maze, pos_x, pos_y, facing_direction):
    passable = get_passable_relative_direction(maze, pos_x, pos_y, facing_direction, can_pass_through)
    num_exit = sum(passable)
    if num_exit > 2:
        return True
    return False

def to_maze(data):
    maze = { "x" : 0, "y" : 0, "structure" : [], "start_x" : 0, "start_y" : 0}
    for k in maze:
        if k in data:
            maze[k] = data[k]
    return maze

def can_pass_through(maze, pos_x, pos_y, target_x, target_y):
    # make sure that we are in range for both source and target
    if not in_range(maze, pos_x, pos_y) or not in_range(maze, target_x, target_y):
        return False
    if is_wall(maze["structure"][target_x][target_y]):
        return False
    return True


"""
Navigation Code for navigating a maze.
"""

"""
Move the state to the position
"""
def move_to(maze, target_pos_x, target_pos_y, state):
    time_required = 1
    state["x"] = target_pos_x
    state["y"] = target_pos_y
    return time_required

"""
can_pass_through : 
    function that takes in a maze, pos_x, pos_y, target_pos_x, target_pos_y
    return boolean representing if target_pos_x, target_pos_y is reachable from pos_x, pos_y
"""
def get_passable_direction(maze, pos_x, pos_y, can_pass_through):
    returnVal = []
    for d in range(0, 4):  # NORTH SOUTH EAST WEST
        direction_mod_x, direction_mod_y = get_direction_mod(d)
        target_pos_x, target_pos_y = pos_x + direction_mod_x, pos_y + direction_mod_y
        returnVal.append(can_pass_through(maze, pos_x, pos_y, target_pos_x, target_pos_y))
    return returnVal

"""
facing_direction : the direction that the program is facing
can_pass_through : 
    function that takes in a maze, pos_x, pos_y, target_pos_x, target_pos_y
    return boolean representing if target_pos_x, target_pos_y is reachable from pos_x, pos_y

"""
def get_passable_relative_direction(maze, pos_x, pos_y, facing_direction, can_pass_through):
    returnVal = []
    for d in range(0, 4):  # FRONT BACK RIGHT LEFT
        direction_mod_x, direction_mod_y = get_direction_mod(get_direction_of(d, facing_direction))
        target_pos_x, target_pos_y = pos_x + direction_mod_x, pos_y + direction_mod_y
        returnVal.append(can_pass_through(maze, pos_x, pos_y, target_pos_x, target_pos_y))
    return returnVal
