from webserver import app
from flask import render_template, jsonify, request
import mazehack.generator as generator
import mazehack.navigator as runtime
from model import db_add_maze, db_get_maze, db_reset_mazes

@app.route("/", methods=["GET"])
def view_index():
    return render_template("index.html")

@app.route("/generate_maze", methods=["POST"])
def view_generate_new_maze():
    if "key" in request.values:
        print(request.values["key"], app.config["GENERATEMAZE_KEY"])
        if request.values["key"] == app.config["GENERATEMAZE_KEY"]:
            db_reset_mazes()
            return jsonify( { "result" : "Maze generated"}), 200
        else:
            return jsonify({}), 403
    else:
        return jsonify({}), 403

@app.route("/getmaze/<string:id>")
def view_get_maze(id):
    maze = db_get_maze(id)
    if maze is None:
        return jsonify({}), 404
    return jsonify(maze), 200

@app.route("/execute/<string:id>", methods=["GET"])
def view_execute_empty_instructions(id):
    return view_execute_instructions(id, "")

@app.route("/execute/<string:id>/<string:instruction>", methods=["GET"])
def view_execute_instructions(id, instruction):
    maze = db_get_maze(id)
    if maze is None:
        return jsonify({"error" : "Maze not found"}), 404
    elif instruction is None:
        return jsonify({"error" : "Empty instruction"}), 400
    
    success, instructions = runtime.compile(instruction)
    if not success:
        return jsonify(instructions), 200

    result = runtime.run_instructions(maze, instructions)
    print(result)
    return jsonify(result), 200
