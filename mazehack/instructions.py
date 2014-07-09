""" 
Compile a string to a instructions list
syntax for the string
    m for MOVE
    l for LEFT
    r for RIGHT
    b for BACK
"""
def compile(string, max_length=100):
    curr_index = 0  
    instructions = ["BEGIN"] 
    while curr_index < len(string):  
        if string[curr_index] == " " :  # allow for empty space
            True
        elif string[curr_index] == "m" :
            instructions.append("MOVE")
        elif string[curr_index] == "r":
            instructions.append("RIGHT")
        elif string[curr_index] == "b":
            instructions.append("BACK")
        elif string[curr_index] == "l":
            instructions.append("LEFT")
        else:
            return False, { "error" : "".join(["Unrecognized symbol : ", str(string[curr_index])]) }
        curr_index+=1
    if len(instructions) > max_length:
        return False, { "error" : "".join(["Number of instructions can only be at most ", str(max_length)]) }
    instructions.append("END")
    return True, instructions
