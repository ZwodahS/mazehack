from mazedef import FRONT, LEFT, RIGHT, BACK
import mazedef

# traverser have the following
# x, y : int
# direction : the direction that the traverser is facing
def move_in_this_direction(maze, traverser):
    time_required = 1
    passable = mazedef.get_passable_relative_direction(maze, traverser["x"], traverser["y"], traverser["direction"], mazedef.can_pass_through)
    direction = traverser["direction"]
    if passable[FRONT]:
        direction = traverser["direction"]
    else:
        if passable[LEFT] and passable[RIGHT]:
            return False, 0
        elif passable[LEFT]:
            direction = mazedef.get_direction_of(LEFT, direction)
        elif passable[RIGHT]:
            direction = mazedef.get_direction_of(RIGHT, direction)
        else:
            return False, 0

    traverser["direction"] = direction
    direction_mod_x, direction_mod_y = mazedef.get_direction_mod(traverser["direction"])
    target_pos_x, target_pos_y = traverser["x"] + direction_mod_x, traverser["y"] + direction_mod_y
    kime_required = mazedef.move_to(maze, target_pos_x, target_pos_y, traverser)
    return True, time_required
