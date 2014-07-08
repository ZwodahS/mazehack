from mazedef import NORTH, SOUTH, EAST, WEST
from mazedef import LEFT, RIGHT, FRONT, BACK
from mazedef import get_relative_direction_string, get_time, is_passable, get_direction_of, get_direction_mod, in_range, can_exit
TOO_MANY_INSTRUCTION = 100
PROGRAM_TERMINATED_IN_NETWORK = 101
PROGRAM_EXITS = 200
"""
Available instructions are
BEGIN
END
MOVE
MOVE X (where X is a "cpu time")
TURN LEFT/RIGHT/BACK
"""

""" 
Compile a string to a instructions list

syntax for the string
    must start with b for BEGIN
    must end with e for END
    m followed by a number will be translated to MOVE X
    m followed by a non-number will be treated as MOVE
    t must be followed by l/r/b, 
"""
def compile(string, max_length=100):
    
    curr_index = 0  
    instructions = [] 
    while curr_index < len(string):  
        if string[curr_index] == " " :
            True
        elif string[curr_index] == "m" :
            if curr_index != len(string) -1 and not string[curr_index+1].isdigit():
                instructions.append("MOVE")
            else :
                intstring = []
                while string[curr_index+1].isdigit():
                    intstring.append(string[curr_index+1])
                    curr_index+=1
                instructions.append(" ".join(["MOVE", "".join(intstring)]))
        elif string[curr_index] == "t" :
            if curr_index == len(string) -1:
                return False, { "error" : "".join(["Need a value after 'turn'"]) }
            elif string[curr_index+1] == "r":
                instructions.append(" ".join(["TURN", str(RIGHT)]))
            elif string[curr_index+1] == "b":
                instructions.append(" ".join(["TURN", str(BACK)]))
            elif string[curr_index+1] == "l":
                instructions.append(" ".join(["TURN", str(LEFT)]))
            else:
                return False, { "error" : "".join(["A value of either b/r/l (back/right/left) required after 'turn', found ", string[curr_index+1]]) }
            curr_index+=1
        elif string[curr_index] == "b" :
            instructions.append("BEGIN")
        elif string[curr_index] == "e" :
            instructions.append("END")
        else:
            return False, { "error" : "".join(["Unrecognized symbol : ", str(string[curr_index])]) }
        curr_index+=1
    if len(instructions) > max_length:
        return False, { "error" : "".join(["Number of instructions can only be at most ", str(max_length)]) }
    return True, instructions

"""
Get object at position
"""
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
            if cpu is not None:
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
            if instruction_split[0] == "MOVE":
                move_instruction(maze, program_state, int(instruction_split[1]))
            elif instruction_split[0] == "TURN":
                turn_instruction(maze, program_state, int(instruction_split[1]))
        else :
            if instruction_split[0] == "MOVE":
                move_instruction(maze, program_state)
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
    if debug:
        result["logs"] = program_state["logs"]

    return result
