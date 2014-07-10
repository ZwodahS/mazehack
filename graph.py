import sys
import random
from mazehack import mazedef, generator, navigation
from mazehack.mazedef import NORTH, SOUTH, EAST, WEST
from mazehack.mazedef import FRONT, BACK, RIGHT, LEFT 
"""
generate the graph from a maze
"""
def move_to(maze, target_pos_x, target_pos_y, traverser):
    traverser["x"] = target_pos_x
    traverser["y"] = target_pos_y
    return 1
"""
move from the current position to the next part of the maze
"""
def move_to_next_node(maze, traverser):
    success, time = navigation.move_in_this_direction(maze, traverser)
    while success and not mazedef.is_decision_point(maze, traverser["x"], traverser["y"], traverser["direction"]):
        success, cost = navigation.move_in_this_direction(maze, traverser)
        time += cost
    return time
"""
Find a node in nodes, that is a x, y position
"""
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
    pos_x, pos_y = generator.get_random_passable_position(maze["x"], maze["y"])
    traverser = { "x" : pos_x, "y" : pos_y, "direction" : NORTH}
    passable = mazedef.get_passable_direction(maze, traverser["x"], traverser["y"], mazedef.can_pass_through)
    while sum(passable) < 3 :
        pos_x, pos_y = generator.get_random_passable_position(maze["x"], maze["y"])
        traverser["x"] = pos_x
        traverser["y"] = pos_y
        passable = mazedef.get_passable_direction(maze, traverser["x"], traverser["y"], mazedef.can_pass_through)
    
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

            passable = mazedef.get_passable_direction(maze, traverser["x"], traverser["y"], mazedef.can_pass_through)
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

    maze = generator.generate_maze(7, 7)
    for y in range(0, maze["y"]):
        string = []
        for x in range(0, maze["x"]):
            if x == maze["start_x"] and y == maze["start_y"]:
                string.append("@")
            elif mazedef.is_wall(maze["structure"][x][y]):
                string.append("#")
            else :
                string.append(" ")
        print("".join(string))
    print("StartX: " + str(maze["start_x"]))
    print("StartY: " + str(maze["start_y"]))


    # graph = generate_graph(maze)
    # for n in graph :
    #     print(n)
