#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 01:36:01 2018

@author: Iswariya Manivannan
"""

import sys
import os
import time


def getNeighbor(maze_map, node, dir=None):
    if dir == "U":
        neighbor = list(
            filter(
                lambda neighbor: node["row"] > 0
                and node["row"] - 1 == neighbor["row"]
                and node["col"] == neighbor["col"],
                maze_map,
            )
        )[0]
        return neighbor
    elif dir == "D":
        neighbor = list(
            filter(
                lambda neighbor: node["row"] + 1 == neighbor["row"]
                and node["col"] == neighbor["col"],
                maze_map,
            )
        )[0]
        return neighbor
    elif dir == "L":
        neighbor = list(
            filter(
                lambda neighbor: node["col"] > 0
                and node["row"] == neighbor["row"]
                and node["col"] - 1 == neighbor["col"],
                maze_map,
            )
        )[0]
        return neighbor
    elif dir == "R":
        neighbor = list(
            filter(
                lambda neighbor: node["row"] == neighbor["row"]
                and node["col"] + 1 == neighbor["col"],
                maze_map,
            )
        )[0]
        return neighbor
    elif dir == None:
        neighbors = list(
            filter(lambda neighbor: checkNeighbor(node, neighbor) == True, maze_map)
        )
        return neighbors

    return False


def checkNeighbor(node, neighbor):
    if node["col"] == neighbor["col"]:
        if node["row"] - 1 == neighbor["row"] or node["row"] + 1 == neighbor["row"]:
            return True
    elif node["row"] == neighbor["row"]:
        if node["col"] - 1 == neighbor["col"] or node["col"] + 1 == neighbor["col"]:
            return True
    return False


def checkValidMove(maze_map, node):
    neighbors = getNeighbor(maze_map, node)

    for neighbor in neighbors:
        if neighbor["value"] == "=" or neighbor["value"] == "|":
            continue
        else:
            if node["row"] - 1 == neighbor["row"] and node["col"] == neighbor["col"]:
                node["moves"].append("U")
            elif node["row"] + 1 == neighbor["row"] and node["col"] == neighbor["col"]:
                node["moves"].append("D")
            elif node["row"] == neighbor["row"] and node["col"] - 1 == neighbor["col"]:
                node["moves"].append("L")
            elif node["row"] == neighbor["row"] and node["col"] + 1 == neighbor["col"]:
                node["moves"].append("R")


def maze_map_to_tree(maze_map):
    """Function to create a tree from the map file. The idea is
    to check for the possible movements from each position on the
    map and encode it in a data structure like list.

    Parameters
    ----------
    maze_map : List
        List with each row in the maze as a string

    Returns
    -------
    maze_map_tree : List
        List of Dictionaries with each node's row, column, value, availabile moves from that node
    """
    maze_map_tree = [
        {"row": i, "col": j, "value": ch, "moves": [], "Explored": False}
        for i in range(len(maze_map))
        for j, ch in enumerate(maze_map[i])
    ]

    for node in maze_map_tree:
        checkValidMove(maze_map_tree, node)

    return maze_map_tree


def getTurnCharacter(maze_map, current_node, prev_node):
    char = [
        "\u2502",
        "\u2500",
        "\u2510",
        "\u250c",
        "\u2518",
        "\u2514",
        "\u251c",
        "\u2524",
        "\u2534",
        "\u252c",
        "\u253c",
    ]
    if current_node["row"] == prev_node["row"] + 1:
        if (
            getNeighbor(maze_map, prev_node, "R")["value"] in char
            and getNeighbor(maze_map, prev_node, "L")["value"] in char
        ):
            return "\u252c"
        elif getNeighbor(maze_map, prev_node, "L")["value"] in char:
            return "\u2510"
        elif getNeighbor(maze_map, prev_node, "R")["value"] in char:
            return "\u250c"
    if current_node["row"] == prev_node["row"] + 1:
        if (
            getNeighbor(maze_map, prev_node, "R")["value"] in char
            and getNeighbor(maze_map, prev_node, "L")["value"] in char
        ):
            return "\u252c"
        elif getNeighbor(maze_map, prev_node, "L")["value"] in char:
            return "\u2510"
        elif getNeighbor(maze_map, prev_node, "R")["value"] in char:
            return "\u250c"


def assign_character_for_nodes(maze_map, current_node, prev_node):
    """Function to assign character for the visited nodes. Please assign
    meaningful characters based on the direction of tree traversal.

    Parameters
    ----------
    maze_map : [type]
        [description]
    current_node : [type]
        [description]
    prev_node : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    hor_dchar = [
        "\u2500",
        "\u2510",
        "\u250c",
        "\u2534",
        "\u252c",
        "\u253c",
    ]
    hor_uchar = [
        "\u2500",
        "\u2518",
        "\u2514",
        "\u2534",
        "\u252c",
        "\u253c",
    ]
    vert_rchar = [
        "\u2502",
        "\u2510",
        "\u2518",
        "\u2524",
        "\u251c",
        "\u253c",
    ]
    vert_lchar = [
        "\u2502",
        "\u250c",
        "\u2514",
        "\u2524",
        "\u251c",
        "\u253c",
    ]
    if current_node["col"] == prev_node["col"]:
        if prev_node["value"] in ["\u2500", "\u2534", "\u252c"]:
            if current_node["row"] == prev_node["row"] + 1:
                current_node["value"] = "\u2502"
                if (
                    getNeighbor(maze_map, prev_node, "R")["value"] in hor_dchar
                    and getNeighbor(maze_map, prev_node, "L")["value"] in hor_dchar
                ):
                    prev_node["value"] = "\u252c"
                elif prev_node["last_node"]["col"] + 1 == prev_node["col"]:
                    prev_node["value"] = "\u2510"
                else:
                    prev_node["value"] = "\u250c"
            elif current_node["row"] == prev_node["row"] - 1:
                current_node["value"] = "\u2502"
                if (
                    getNeighbor(maze_map, prev_node, "R")["value"] in hor_uchar
                    and getNeighbor(maze_map, prev_node, "L")["value"] in hor_uchar
                ):
                    prev_node["value"] = "\u2534"
                elif prev_node["last_node"]["col"] + 1 == prev_node["col"]:
                    prev_node["value"] = "\u2518"
                else:
                    prev_node["value"] = "\u2514"
        else:
            if current_node["value"] in ["\u2518", "\u2510"]:
                current_node["value"] = "\u2524"
            elif current_node["value"] in ["\u2514", "\u250c"]:
                current_node["value"] = "\u251c"
            elif current_node["value"] == "\u2500":
                current_node["value"] = "\u253c"
            else:
                current_node["value"] = "\u2502"
    elif current_node["row"] == prev_node["row"]:
        if prev_node["value"] in ["\u2502", "\u2524", "\u251c"]:
            if current_node["col"] == prev_node["col"] - 1:
                current_node["value"] = "\u2500"
                if (
                    getNeighbor(maze_map, prev_node, "U")["value"] in vert_lchar
                    and getNeighbor(maze_map, prev_node, "D")["value"] in vert_lchar
                ):
                    prev_node["value"] = "\u2524"
                elif prev_node["last_node"]["row"] + 1 == prev_node["row"]:
                    prev_node["value"] = "\u2518"
                else:
                    prev_node["value"] = "\u2510"
            elif current_node["col"] == prev_node["col"] + 1:
                current_node["value"] = "\u2500"
                if (
                    getNeighbor(maze_map, prev_node, "U")["value"] in vert_rchar
                    and getNeighbor(maze_map, prev_node, "D")["value"] in vert_rchar
                ):
                    prev_node["value"] = "\u251c"
                elif prev_node["last_node"]["row"] + 1 == prev_node["row"]:
                    prev_node["value"] = "\u2514"
                else:
                    prev_node["value"] = "\u250c"
        else:
            if current_node["value"] in ["\u250c", "\u2510"]:
                current_node["value"] = "\u252c"
            elif current_node["value"] in ["\u2518", "\u2514"]:
                current_node["value"] = "\u2534"
            elif current_node["value"] == "\u2502":
                current_node["value"] = "\u253c"
            else:
                current_node["value"] = "\u2500"


def single_goal_traversal(solution, maze_map, file):
    prev_node = solution[0]
    prev_node["last_node"] = None
    path_coordinates = [[prev_node["row"], prev_node["col"], prev_node["value"]]]
    for idx, move in enumerate(solution[2]):
        current_node = getNeighbor(maze_map, prev_node, dir=move)
        assign_character_for_nodes(maze_map, current_node, prev_node)
        path_coordinates.append(
            [
                current_node["row"],
                current_node["col"],
                prev_node["value"],
                current_node["value"],
                move,
            ]
        )
        current_node["last_node"] = prev_node
        prev_node = current_node
        if current_node == solution[1]:
            current_node["value"] = "*"

    print_map(maze_map, solution)
    write_to_file(file, maze_map, solution)


def print_map(path_map, soluton):
    print_maze = []
    num_rows = max(node["row"] for node in path_map) + 1

    for i in range(num_rows):
        print_maze.append(
            "".join([node["value"] for node in path_map if node["row"] == i])
        )

    print("%s" % "\n".join(map(str, print_maze)))


def write_to_file(file_name, path_map, solution):
    """Function to write output to console and the optimal path
    from start to each goal to txt file.
    Please ensure that it should ALSO be possible to visualize each and every
    step of the tree traversal algorithm in the map in the console.
    This enables understanding towards the working of your
    tree traversal algorithm as to how it reaches the goals.

    Parameters
    ----------
    file_name : string
        This parameter defines the name of the txt file.
    path : list
        list of nodes
    solution : list
        list containing [start node, goal node, path from start to goal]

    """

    print_maze = []
    num_rows = max(node["row"] for node in path_map) + 1

    for i in range(num_rows):
        print_maze.append(
            "".join([node["value"] for node in path_map if node["row"] == i])
        )
        print_maze.append("\n")

    with open(file_name, "a+") as output_file:
        output_file.write(
            "Starting Search @ {},{}\n".format(solution[0]["row"], solution[0]["col"])
        )
        output_file.write(
            "Goal Found @ {},{}\n".format(solution[1]["row"], solution[1]["col"])
        )
        output_file.writelines(print_maze)
    output_file.close()
