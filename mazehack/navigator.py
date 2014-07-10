from mazedef import NORTH, SOUTH, EAST, WEST
from mazedef import LEFT, RIGHT, FRONT, BACK
import mazedef
import navigation
from instructions import compile

TOO_MANY_INSTRUCTION = 100
PROGRAM_TERMINATED_IN_NETWORK = 101
PROGRAM_EXITS = 200

def is_decision(maze, program_state):
    passable = mazedef.get_passable_relative_direction(maze, program_state["x"], program_state["y"], program_state["direction"], mazedef.can_pass_through)
    num_exit = sum(passable)
    if num_exit > 2 :
        return True
    if program_state["x"] == maze["start_x"] and program_state["y"] == maze["start_y"]:
        return True
    return False

def move_instruction(maze, program_state):
    program_state["logs"].append("".join(["[Executing Move Instruction] Move"]))
    success, time = navigation.move_in_this_direction(maze, program_state)
    while success and not mazedef.is_decision_point(maze, program_state["x"], program_state["y"], program_state["direction"]):
        success, cost = navigation.move_in_this_direction(maze, program_state)
        time += cost

    program_state["logs"].append("".join(["Move terminates after ", str(time), " cpu-cycle."]))
    add_information(maze, program_state)

def turn_instruction(maze, program_state, relative_direction):
    program_state["logs"].append("".join(["[Executing Turn Instruction] Turn ", mazedef.get_relative_direction_string(relative_direction)]))
    new_direction = mazedef.get_direction_of(relative_direction, program_state["direction"])
    program_state["direction"] = new_direction
    add_information(maze, program_state)

def begin_instruction(maze, program_state):
    program_state["logs"].append("".join(["[Begin - ]"]))
    add_information(maze, program_state)

def add_information(maze, program_state):
    passable = mazedef.get_passable_relative_direction(maze, program_state["x"], program_state["y"], program_state["direction"], mazedef.can_pass_through)
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
                if mazedef.can_exit(maze, program_state["x"], program_state["y"]) :
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
