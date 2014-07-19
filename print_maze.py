import sys
from mazehack.mazedef import is_wall
from mazehack.generator import generate_maze, get_random_variable_position
from mazehack.navigator import run_instructions
from mazehack.navigator import compile
import json
import random
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("print_maze width height seed")
        print("Enter ? for random seed")
    else:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        seed = random.randint(0, 1000000) if sys.argv[3] == "?" else int(sys.argv[3])
        loop = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        
        random.seed(seed)

        maze = generate_maze(width, height, {"loop" : loop})
        for y in range(0, maze["y"]):
            string = []
            for x in range(0, maze["x"]):
                if is_wall(maze["structure"][x][y]):
                    string.append("#")
                else :
                    string.append(" ")
            print("".join(string))
