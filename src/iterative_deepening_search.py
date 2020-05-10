#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:15:04 2018

@author: Iswariya Manivannan
"""
import sys
import os
import itertools
from collections import deque
from helper import maze_map_to_tree, getNeighbor, single_goal_traversal, write_to_file


def DLS(maze_map, queue, goal_pos, max_depth):
    while queue:
        current_node = queue.pop()
        if current_node[1] in goal_pos:
            return True, current_node
        elif current_node[1]["Explored"] == True:
            continue
        elif current_node[2] >= max_depth:
            current_node[1]["Explored"] = True
            continue
        elif current_node[2] < max_depth:
            for move in current_node[1]["moves"]:
                current_node[1]["Explored"] = True
                next_node = getNeighbor(maze_map, current_node[1], dir=move)
                if next_node["Explored"] == False:
                    path = current_node[0]
                    path += move
                    queue.append((path, next_node, current_node[2] + 1))

    return False, current_node


def iterative_deepening_depth_first_search(maze_map, start_pos, goal_pos, file):
    """Function to implement the DFS algorithm.
    Please use the functions in helper.py to complete the algorithm.
    Please do not clutter the code this file by adding extra functions.
    Additional functions if required should be added in helper.py

    Parameters
    ----------
    maze_map : list
        list of nodes in the maze. Each node is a dictionary
    start_pos : dict
        start node 
    goal_pos : list
        list of goal in the maze

    Returns
    -------
    solution : list
        list of start node, goal node and path from start to the goal in the maze. Each node is a dictionary
    """
    solution = []
    start = start_pos
    goal = goal_pos
    queue = deque([("", start, 0)])
    limit = len(maze_map) - len(
        list(filter(lambda node: node["value"] in ["=", "|"], maze_map))
    )  # Total Searchable nodes (excluding maze boundries)
    max_depth = 0

    while max_depth < limit:
        result, final_node = DLS(maze_map, queue, goal, max_depth)
        if result is True:
            print(
                "Goal Found! @ {},{}".format(final_node[1]["row"], final_node[1]["col"])
            )
            single_goal_traversal([start, final_node[1], final_node[0]], maze_map, file)
            goal.remove(final_node[1])
            solution.append([start, final_node[1], final_node[0]])
            final_node[1]["value"] = "X"
            for node in maze_map:
                if node["value"] not in ["*", "=", "|", "s"]:
                    node["value"] = " "
            if len(goal) > 0:
                queue = deque([("", start, 0)])
                max_depth = 0
                for node in maze_map:
                    node["Explored"] = False
            else:
                return solution
        elif result is False:
            queue = deque([("", start, 0)])
            max_depth += 1
            for node in maze_map:
                node["Explored"] = False

    for goal in goal_pos:
        print("Could not reach goal @ {},{}".format(goal["row"], goal["col"]))
        with open(file, "a") as output_file:
            output_file.write(
                "Could not reach goal @ {},{}\n".format(goal["row"], goal["col"])
            )
        output_file.close()

    return solution


if __name__ == "__main__":

    working_directory = os.getcwd()

    if len(sys.argv) > 1:
        map_directory = sys.argv[1]
    else:
        map_directory = "maps"

    file_path_map1 = os.path.join(working_directory, map_directory + "/map1.txt")
    file_path_map2 = os.path.join(working_directory, map_directory + "/map2.txt")
    file_path_map3 = os.path.join(working_directory, map_directory + "/map3.txt")

    maze_map_map1 = []
    with open(file_path_map1) as f1:
        maze_map_map1 = f1.read().splitlines()

    maze_map_map2 = []
    with open(file_path_map2) as f2:
        maze_map_map2 = f2.read().splitlines()

    maze_map_map3 = []
    with open(file_path_map3) as f3:
        maze_map_map3 = f3.read().splitlines()

    maze_map_tree1 = maze_map_to_tree(maze_map_map1)
    start_pos_map1 = [node for node in maze_map_tree1 if node["value"] == "s"][0]
    goal_pos_map1 = [node for node in maze_map_tree1 if node["value"] == "*"]

    print(
        "Starting Map #1 Search @ {},{}".format(
            start_pos_map1["row"], start_pos_map1["col"]
        )
    )
    solution_map1 = iterative_deepening_depth_first_search(
        maze_map_tree1, start_pos_map1, goal_pos_map1, "results/iddfs_map1.txt"
    )

    print(
        "Starting Map #2 Search @ {},{}".format(
            start_pos_map2["row"], start_pos_map2["col"]
        )
    )
    maze_map_tree2 = maze_map_to_tree(maze_map_map2)
    start_pos_map2 = [node for node in maze_map_tree2 if node["value"] == "s"][0]
    goal_pos_map2 = [node for node in maze_map_tree2 if node["value"] == "*"]

    solution_map2 = iterative_deepening_depth_first_search(
        maze_map_tree2, start_pos_map2, goal_pos_map2, "results/iddfs_map2.txt"
    )

    print(
        "Starting Map #3 Search @ {},{}".format(
            start_pos_map3["row"], start_pos_map3["col"]
        )
    )
    maze_map_tree3 = maze_map_to_tree(maze_map_map3)
    start_pos_map3 = [node for node in maze_map_tree3 if node["value"] == "s"][0]
    goal_pos_map3 = [node for node in maze_map_tree3 if node["value"] == "*"]

    solution_map3 = iterative_deepening_depth_first_search(
        maze_map_tree3, start_pos_map3, goal_pos_map3, "results/iddfs_map3.txt"
    )
