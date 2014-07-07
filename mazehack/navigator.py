from mazedef import NORTH, SOUTH, EAST, WEST
from mazedef import LEFT, RIGHT, FRONT, BACK
from mazedef import get_relative_direction_string, get_time, is_passable, get_direction_of, get_direction_mod, in_range
TOO_MANY_INSTRUCTION = 100
PROGRAM_TERMINATED_IN_NETWORK = 101
PROGRAM_EXITS = 200
"""
Available instructions are
MOVE
MOVE X (where X is a "cpu time")
TURN LEFT/RIGHT/BACK
"""

""" 
test if there are invalid instructions/insstruction length
"""
def compile(instructions):
    return True


def get_obj(x, y, facing_direction, maze, relative_direction):
    target_direction = get_direction_of(relative_direction, facing_direction)
    mod_x, mod_y = get_direction_mod(target_direction)
    target_pos_x, target_pos_y = (x + mod_x, y + mod_y)
    if in_range(maze, target_pos_x, target_pos_y):
        if is_passable(maze["structure"][target_pos_x][target_pos_y]):
            return "[Empty Space]"
    return None


def get_see(maze, program_state, ignoreFront=False, ignoreBack=False):
    saw = []
    obj = get_obj(program_state["x"], program_state["y"], program_state["direction"], maze, LEFT)
    if obj is not None:
        saw.append(" ".join(["Saw", obj, "On the Left"]))

    obj = get_obj(program_state["x"], program_state["y"], program_state["direction"], maze, RIGHT)
    if obj is not None:
        saw.append(" ".join(["Saw", obj, "On the Right"]))

    if not ignoreFront:
        obj = get_obj(program_state["x"], program_state["y"], program_state["direction"], maze, FRONT)
        if obj is not None:
            saw.append(" ".join(["Saw", obj, "In front"]))
    if not ignoreBack:
        obj = get_obj(program_state["x"], program_state["y"], program_state["direction"], maze, BACK)
        if obj is not None:
            saw.append(" ".join(["Saw", obj, "Behind"]))

    return saw

def move_instruction(maze, program_state, cpu = None):
    if cpu is None:
        program_state["logs"].append("".join(["[Executing Move Instruction] Move"]))
    else:
        program_state["logs"].append("".join(["[Executing Move Instruction] Move ", str(cpu)]))
    time = 0


    structure = maze["structure"]
    while (cpu is None or cpu >= get_time(structure[program_state["x"]][program_state["y"]])) and (program_state["cpu"] > 0):
        print(program_state["x"], program_state["y"])
        # add what we see to the logs
        saw = get_see(maze, program_state, True, True)
        for seen in saw : 
            program_state["logs"].append("".join(["    ", seen, " at ", str(time), " cpu-time"]))
        ## prepare to move and calculate where we will be moving 
        direction_mod_x, direction_mod_y = get_direction_mod(program_state["direction"])
        target_pos_x, target_pos_y = program_state["x"] + direction_mod_x, program_state["y"] + direction_mod_y
        # check if we can move there
        if in_range(maze, target_pos_x, target_pos_y) and is_passable(structure[target_pos_x][target_pos_y]):
            time_required = get_time(structure[program_state["x"]][program_state["y"]])
            if cpu is not None :
                cpu -= time_required
            program_state["cpu"] -= time_required
            if program_state["cpu"] <= 0:
                break
            time += time_required
            current_pos_x, current_pos_y = target_pos_x, target_pos_y
            program_state["x"] = target_pos_x
            program_state["y"] = target_pos_y
        else:
            # can't move there
            program_state["logs"].append("".join(["    ", "Hit Obstacle at ", str(time), " cpu-time"]))
            return
    saw = get_see(maze, program_state)
    for seen in saw : 
        program_state["logs"].append("".join(["    ", seen, " at ", str(time), " cpu-time"]))


def turn_instruction(maze, program_state, relative_direction):
    program_state["logs"].append("".join(["[Executing Turn Instruction] Turn ", get_relative_direction_string(relative_direction)]))
    
    new_direction = get_direction_of(relative_direction, program_state["direction"])
    program_state["direction"] = new_direction

    saw = get_see(maze, program_state)
    for seen in saw:
        program_state["logs"].append("".join(["    ", seen, " after turning"]))

def begin_instruction(maze, program_state):
    program_state["logs"].append("".join(["[Begin - ]"]))
    saw = get_see(maze, program_state)
    for seen in saw : 
        program_state["logs"].append("".join(["    ", seen]))

def run_instructions(maze, instructions):
    result = {}
    program_state = {"cpu" : 200, "direction" : NORTH, "logs" : [] , "x" : maze["start_x"], "y" : maze["start_y"] } 
    current_instruction = 0 
    while program_state["cpu"] > 0 and current_instruction < len(instructions):
        instruction = instructions[current_instruction] 
        instruction_split = instruction.split(" ")
        if len(instruction_split) > 1 :
            if instruction_split[0] == "MOVE":
                move_instruction(maze, program_state, int(instruction_split[1]))
            elif instruction_split[0] == "TURN":
                turn_instruction(maze, program_state, int(instruction_split[1]))
        else :
            if instruction_split[0] == "MOVE":
                move_instruction(maze, program_state, instruction)
            elif instruction_split[0] == "BEGIN":
                begin_instruction(maze, program_state)
            elif instruction_split[0] == "END":
                program_state["logs"].append("".join(["[End - ]"]))
                print("End cond", program_state["x"], program_state["y"], maze["start_x"], maze["start_y"])
                if program_state["x"] == maze["start_x"] and program_state["y"] == maze["start_y"]:
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
