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
"""
def calculate_bit(original_value, index, value):
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

XXXXXXXXX[exit:1][speed:3][passable:1]
"""
def is_passable(value):
    return value & 1 > 0

def set_passable(structure, x, y, value):
    newvalue = structure[x][y] 
    structure[x][y] = calculate_bit(structure[x][y], 0, 1 if value else 0)
""" 
get the time needed to move out of the tile
"""
def get_time(value):
    time = (value & 14) >> 1
    return pow(2, time-1)
""" 
Must be 1, 2, 3, 4, 5
"""
def set_time(value, time_value):
    if time_value < 1 or time_value > 5:
        time_value = 3
    time_value << 1
    mask = 7 << 1
    value &= ~mask
    value |= time_value
    return value
    

def is_curved(value):
    return value & 16 > 0

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

def get_relative_direction_string(direction):
    if direction == FRONT:
        return "FRONT"
    elif direction == BACK:
        return "BACK"
    elif direction == RIGHT:
        return "RIGHT"
    else: # direction == LEFT
        return "LEFT"

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

def to_maze(data):
    maze = { "x" : 0, "y" : 0, "structure" : [], "start_x" : 0, "start_y" : 0}
    for k in maze:
        if k in data:
            maze[k] = data[k]
    return maze
