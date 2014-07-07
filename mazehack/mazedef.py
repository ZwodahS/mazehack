from random import randint
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
    print("Setting : " + str(x) + " " + str(y) + " to " + str(value))
    newvalue = structure[x][y] 
    structure[x][y] = calculate_bit(structure[x][y], 0, 1 if value else 0)

""" 
get the time needed to move out of the tile
"""
def get_time(value):
    time = (value & 14) >> 1
    return pow(2, time-1)

def is_curved(value):
    return value & 16 > 0

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
"""
origin is top left
"""
def get_direction_mod(direction):
    if direction is NORTH:
        return (0, -1)
    elif direction is SOUTH:
        return (0, 1)
    elif direction is EAST:
        return (1, 0)
    elif direction is WEST:
        return (-1, 0)
    else :
        return (0, 0)

def in_range(maze, x, y):
    return x >= 0 and x < maze["x"] and y >= 0 and y < maze["y"] 

def change_direction(direction):
    i = randint(0, 1)
    if direction is NORTH:
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
    if direction is NORTH:
        return SOUTH
    elif direction is SOUTH:
        return NORTH
    elif direction is EAST:
        return WEST
    else:
        return EAST
