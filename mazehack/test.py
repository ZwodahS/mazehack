from mazedef import get_time, is_passable
from generator import generate_maze
from navigator import run_instructions
import random
if __name__ == "__main__":
    random.seed(0)
    maze = generate_maze(21, 21)
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
    
    result = run_instructions(maze, ["BEGIN", "TURN 3", "MOVE 12", "TURN 1", "MOVE 12", "END"])
    for log in result["logs"]:
        print(log)

    print(result["result"])
