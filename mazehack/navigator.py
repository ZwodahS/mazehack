from mazedef import NORTH, SOUTH, EAST, WEST
from mazedef import LEFT, RIGHT, FRONT, BACK
from mazedef import get_relative_direction_string, get_time, is_passable, get_direction_of, get_direction_mod, in_range, can_exit
from instructions import compile
TOO_MANY_INSTRUCTION = 100
PROGRAM_TERMINATED_IN_NETWORK = 101
PROGRAM_EXITS = 200

def can_pass_through(maze, pos_x, pos_y, program_state):
    if in_range(maze, pos_x, pos_y) and is_passable(maze["structure"][pos_x][pos_y]):
        return True
    else:
        return False

def move_to(maze, target_pos_x, target_pos_y, program_state):
    time_required = get_time(maze["structure"][program_state["x"]][program_state["y"]])
    program_state["cpu"] -= time_required
    program_state["x"] = target_pos_x
    program_state["y"] = target_pos_y
    return time_required

"""
return 4 values in a list
such that values[RIGHT] is a bool representing if that direction is passable
"""
def get_passable_direction(maze, program_state):
    returnVal = []
    for d in range(0, 4):  # NORTH SOUTH EAST WEST
        direction_mod_x, direction_mod_y = get_direction_mod(d)
        target_pos_x, target_pos_y = program_state["x"] + direction_mod_x, program_state["y"] + direction_mod_y
        returnVal.append(can_pass_through(maze, target_pos_x, target_pos_y, program_state))
    return returnVal

def get_passable_relative_direction(maze, program_state):
    returnVal = []
    for d in range(0, 4): # FRONT BACK RIGHT LEFT
        direction_mod_x, direction_mod_y = get_direction_mod(get_direction_of(d, program_state["direction"]))
        target_pos_x, target_pos_y = program_state["x"] + direction_mod_x, program_state["y"] + direction_mod_y
        returnVal.append(can_pass_through(maze, target_pos_x, target_pos_y, program_state))
    return returnVal

def is_decision(maze, program_state):
    passable = get_passable_relative_direction(maze, program_state)
    num_exit = sum(passable)
    if num_exit > 2 :
        return True
    if program_state["x"] == maze["start_x"] and program_state["y"] == maze["start_y"]:
        return True
    return False

def move_in_this_direction(maze, program_state):
    time_required = 0
    ## get the relative direction that the program can pass
    passable = get_passable_relative_direction(maze, program_state)

    direction = program_state["direction"]
    if passable[FRONT] :  #if the front is passable, we just move in front
        direction = program_state["direction"]
    else:                 # front is not passable, we want check if both left and right is passable
        if passable[LEFT] and passable[RIGHT]:
            return False, 0
        elif passable[LEFT]:
            direction = get_direction_of(LEFT, program_state["direction"])
        elif passable[RIGHT]:
            direction = get_direction_of(RIGHT, program_state["direction"])
        else:  # the only exit from this tile is back
            return False, 0
    
    program_state["direction"] = direction
    direction_mod_x, direction_mod_y = get_direction_mod(program_state["direction"])
    target_pos_x, target_pos_y = program_state["x"] + direction_mod_x, program_state["y"] + direction_mod_y
    time_required = move_to(maze, target_pos_x, target_pos_y, program_state)
    return True, time_required

def move_instruction(maze, program_state):
    program_state["logs"].append("".join(["[Executing Move Instruction] Move"]))
    structure = maze["structure"]
    success, time = move_in_this_direction(maze, program_state)
    while success and program_state["cpu"] > 0:
        success, cost = move_in_this_direction(maze, program_state)
        time += cost
        if is_decision(maze, program_state) or not success:
            break

    program_state["logs"].append("".join(["Move terminates after ", str(time), " cpu-cycle."]))
    add_information(maze, program_state)

def turn_instruction(maze, program_state, relative_direction):
    program_state["logs"].append("".join(["[Executing Turn Instruction] Turn ", get_relative_direction_string(relative_direction)]))
    new_direction = get_direction_of(relative_direction, program_state["direction"])
    program_state["direction"] = new_direction
    add_information(maze, program_state)

def begin_instruction(maze, program_state):
    program_state["logs"].append("".join(["[Begin - ]"]))
    add_information(maze, program_state)

def add_information(maze, program_state):
    passable = get_passable_relative_direction(maze, program_state)
    if passable[FRONT] :
        program_state["logs"].append("".join(["[    ","Front is passable","]"]))
    else :
        program_state["logs"].append("".join(["[    ","Front is not passable","]"]))

    if passable[BACK] :
        program_state["logs"].append("".join(["[    ","Back is passable","]"]))
    else :
        program_state["logs"].append("".join(["[    ","Back is not passable","]"]))

    if passable[LEFT] :
        program_state["logs"].append("".join(["[    ","Left is passable","]"]))
    else :
        program_state["logs"].append("".join(["[    ","Left is not passable","]"]))

    if passable[RIGHT] :
        program_state["logs"].append("".join(["[    ","Right is passable","]"]))
    else :
        program_state["logs"].append("".join(["[    ","Right is not passable","]"]))

    if program_state["x"] == maze["start_x"] and program_state["y"] == maze["start_y"] :
        program_state["logs"].append("".join(["[    ","At entrance", "]"]))
"""
The main run instructions method, all that you need.
"""
def run_instructions(maze, instructions, debug=False):
    result = {"logs":[]}
    program_state = {"cpu" : 200, "direction" : NORTH, "logs" : [] , "x" : maze["start_x"], "y" : maze["start_y"] } 
    current_instruction = 0 
    
    # terminates when the program do not have any more cpu or when the instruction runs out.
    while program_state["cpu"] > 0 and current_instruction < len(instructions):
        instruction = instructions[current_instruction] 
        instruction_split = instruction.split(" ")

        if len(instruction_split) > 1 :
            True  #Shouldn't have anything here at the moment
        else :
            if instruction_split[0] == "MOVE":
                move_instruction(maze, program_state)
            elif instruction_split[0] == "RIGHT":
                turn_instruction(maze, program_state, RIGHT)
            elif instruction_split[0] == "LEFT":
                turn_instruction(maze, program_state, LEFT)
            elif instruction_split[0] == "BACK":
                turn_instruction(maze, program_state, BACK)
            elif instruction_split[0] == "BEGIN":
                begin_instruction(maze, program_state)
            elif instruction_split[0] == "END":
                program_state["logs"].append("".join(["[End - ]"]))
                if can_exit(maze, program_state["x"], program_state["y"]) :
                    program_state["logs"].append("".join(["    ", "Successfully exit"]))
                    result["result_code"] = PROGRAM_EXITS
                    result["result"] = "Program exits properly"
                    result["logs"] = program_state["logs"]
                    return result

        current_instruction+=1
        
    result["result_code"] = PROGRAM_TERMINATED_IN_NETWORK
    result["result"] = "Program terminated without returning"
    result["logs"] = program_state["logs"]

    return result
