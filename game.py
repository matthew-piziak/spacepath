"""Game runner"""

import subprocess
import os

import pygame

import newt
import pathing
import draw
import obstacle

START = newt.Node(0, 0, 0, 0, 1)
GOAL = newt.Node(160, 160, 0, 0, 0)

def get_path(obstacles, bounds):
    """return nodes in path from A*"""
    heuristic = lambda n, g: newt.heuristic(n, g, obstacles, bounds)
    return pathing.a_star(START, GOAL, newt.adjacent, heuristic, newt.success)

def main():
    """generate path and render"""
    obstacles = obstacle.get_obstacles(START.x, START.y, GOAL.x, GOAL.y)
    bounds = (GOAL.x, GOAL.y)
    window = draw.init(obstacles, GOAL)
    pygame.display.flip()
    path = get_path(obstacles, bounds)
    draw.path(window, obstacles, GOAL, path)

if __name__ == "__main__":
    while True:
        main()
