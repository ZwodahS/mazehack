import sys
import random
from mazehack.mazedef import NORTH, SOUTH, EAST, WEST
from mazehack.mazedef import FRONT, BACK, RIGHT, LEFT 
from mazehack.navigator import get_passable_direction, get_passable_relative_direction, is_decision
from mazehack.generator import generate_maze, get_random_passable_position
from mazehack.mazedef import get_relative_direction_string, get_time, is_passable, get_direction_of, get_direction_mod, in_range, can_exit
"""
generate the graph from a maze
"""
def move_to(maze, target_pos_x, target_pos_y, traverser):
    time_required = get_time(maze["structure"][traverser["x"]][traverser["y"]])
    traverser["x"] = target_pos_x
    traverser["y"] = target_pos_y
    return time_required
# adapted from the one in navigator
def move_in_this_direction(maze, traverser):
    time_required = 0
    ## get the relative direction that the program can pass
    passable = get_passable_relative_direction(maze, traverser)

    direction = traverser["direction"]
    if passable[FRONT] :  #if the front is passable, we just move in front
        direction = traverser["direction"]
    else:                 # front is not passable, we want check if both left and right is passable
        if passable[LEFT] and passable[RIGHT]:
            return False, 0
        elif passable[LEFT]:
            direction = get_direction_of(LEFT, traverser["direction"])
        elif passable[RIGHT]:
            direction = get_direction_of(RIGHT, traverser["direction"])
        else:  # the only exit from this tile is back
            return False, 0
    
    traverser["direction"] = direction
    direction_mod_x, direction_mod_y = get_direction_mod(traverser["direction"])
    target_pos_x, target_pos_y = traverser["x"] + direction_mod_x, traverser["y"] + direction_mod_y
    time_required = move_to(maze, target_pos_x, target_pos_y, traverser)
    return True, time_required

def move_to_next_node(maze, traverser):
    structure = maze["structure"]
    success, time = move_in_this_direction(maze, traverser)
    while success:
        success, cost = move_in_this_direction(maze, traverser)
        time += cost
        if is_decision(maze, traverser) or not success:
            break
    return time

def find_node(nodes, x, y):
    new_nodes = [n for n in nodes if n["x"] == x and n["y"] == y]
    if new_nodes:
        return new_nodes[0]
    return None

def generate_graph(maze):
    # each node is stored as a dictionary of 
    # id : the position of the node in the nodelist
    # x, y , to store the position on the map
    # edges : list of edges, 3 value, direction(N/S/E/W), cost, destination (id on the list)
    # example { "x" : 3, "y" ; 4 , "edges" : [ { "direction" : "N", "cost" : 5, destination : 4} ] }
    nodes = []
    
    # randomly select a spot from the map that is a junction
    pos_x, pos_y = get_random_passable_position(maze["x"], maze["y"])
    traverser = { "x" : pos_x, "y" : pos_y, "direction" : NORTH}
    passable = get_passable_direction(maze, traverser)
    while sum(passable) < 3 :
        pos_x, pos_y = get_random_passable_position(maze["x"], maze["y"])
        traverser["x"] = pos_x
        traverser["y"] = pos_y
        passable = get_passable_direction(maze, traverser)
    
    # create the initial node
    node = { "id" : len(nodes), "x" : traverser["x"], "y" : traverser["y"] , "edges" : [] }
        
    nodes.append(node)
    stack = []
    stack.append( { "node" : node, "N" : passable[NORTH], "S" : passable[SOUTH], "E" : passable[EAST], "W" : passable[WEST] })

    while stack :
        current = stack[-1]
        traverser["x"] = current["node"]["x"]
        traverser["y"] = current["node"]["y"]
        edge = {}
        # if any direction have not been traveled , then we continue
        if current["N"]:
            traverser["direction"] = NORTH
            edge = { "direction" : "N" }
            current["N"] = False
        elif current["S"]:
            traverser["direction"] = SOUTH
            edge = { "direction" : "S" }
            current["S"] = False
        elif current["E"]: 
            traverser["direction"] = EAST
            edge = { "direction" : "E" }
            current["E"] = False
        elif current["W"] :
            traverser["direction"] = WEST
            edge = { "direction" : "W" }
            current["W"] = False
        else:
            stack.pop()
            continue
        
        # this only happen if we are traversing
        cost = move_to_next_node(maze, traverser)
        edge["cost"] = cost

        existing_node = find_node(nodes, traverser["x"], traverser["y"])
        if existing_node:
            edge["node"] = existing_node["id"]
            current["node"]["edges"].append(edge)
        else:
            new_node = { "id" : len(nodes), "x" : traverser["x"], "y" : traverser["y"] , "edges" : [] }
            nodes.append(new_node)
            edge["node"] = new_node["id"]
            current["node"]["edges"].append(edge)

            passable = get_passable_direction(maze, traverser)
            stack.append( { "node" : new_node, "N" : passable[NORTH], "S" : passable[SOUTH], "E" : passable[EAST], "W" : passable[WEST] })
        
    return nodes

if __name__ == "__main__" :
    if len(sys.argv) > 1:
        if sys.argv[1] == "?" :
            seedValue = random.randint(0, 1000000)
            print("".join(["Seed : ", str(seedValue)]))
        else:
            seedValue = int(sys.argv[1])
            random.seed(seedValue)

    maze = generate_maze(11, 11, {"holes" : 30})
    for y in range(0, maze["y"]):
        string = []
        for x in range(0, maze["x"]):
            if x == maze["start_x"] and y == maze["start_y"]:
                string.append("@")
            elif is_passable(maze["structure"][x][y]):
                string.append(" ")
            else :
                string.append("#")
        print("".join(string))
    print("StartX: " + str(maze["start_x"]))
    print("StartY: " + str(maze["start_y"]))


    graph = generate_graph(maze)
    for n in graph :
        print(n)
