import sys
from mazehack.mazedef import get_time, is_passable
from mazehack.generator import generate_maze
from mazehack.navigator import run_instructions
from mazehack.navigator import compile
import json
import random
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "python test.py <seed> <instructions>"
        print "enter ? for seed to get a random seed"
    else:
        try:
            if sys.argv[1] == "?" :
                seedValue = random.randint(0, 1000000)
                print("".join(["Seed : ", str(seedValue)]))
            else:
                seedValue = int(sys.argv[1])
                random.seed(seedValue)
            d = generate_maze(21, 21)
            e = json.dumps(d)
            maze = json.loads(e)
            if len(sys.argv) > 3 and sys.argv[3] == "DEBUG":
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
            success, instructions = compile(sys.argv[2])
            if success :
                for instruction in instructions :
                    print(instruction)
                result = run_instructions(maze, instructions)
                print(result["result"])
                for log in result["logs"]:
                    print(log)
            else :
                print("".join(["Error : " , instructions["error"]]))

        except ValueError:
            print("Enter a numerical seed")
