from mazedef import get_time
from generator import generate_maze

if __name__ == "__main__":

    maze = generate_maze(51, 51)
    for row in maze["structure"] :
        string = []
        for v in row:
            if v is 1 :
                string.append(" ")
            else:
                string.append("#")
        print("".join(string))

