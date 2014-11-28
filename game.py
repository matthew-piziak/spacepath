"""Game runner"""

import newt
import pygame
import random
import pathing
import time
import subprocess
import os
import math
from scipy import interpolate
import numpy as np
import draw

# obstacle constants
NUM_OBSTACLES = 12

# nodes
START = newt.Node(0, 0, 0, 0, 1)
GOAL = newt.Node(160, 160, 0, 0, 0)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 18
    minimum_obstacle_radius = 12
    max_x_position = GOAL.x - maximum_obstacle_radius
    max_y_position = GOAL.y - maximum_obstacle_radius
    min_x_position = START.x + maximum_obstacle_radius
    min_y_position = START.y + maximum_obstacle_radius
    radius = random.randint(minimum_obstacle_radius, maximum_obstacle_radius)
    x = random.randint(min_x_position, max_x_position)
    y = random.randint(min_y_position, max_y_position)
    return newt.Circle(x, y, radius)

def get_path(obstacles, bounds):
    """return nodes in path from A*"""
    heuristic = lambda n, g: newt.heuristic(n, g, obstacles, bounds)
    return pathing.a_star(START, GOAL, newt.adjacent, heuristic, newt.success)

def clear_images():
    """delete all PNGs from program directory"""
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)

def save_image(window, i):
    """save screenshot to disk"""
    pygame.image.save(window, str(i).zfill(4) + "screen.png")

def make_gif():
    """generate a gif from the accumulated screenshots"""
    label = str(int(time.time()))
    print("label: " + label)
    gif_command = "bash make_gif.sh maneuver" + label + ".gif"
    subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)

def main():
    """generate path and render"""
    obstacles = []
    for _ in range(random.randint(0, NUM_OBSTACLES)):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    bounds = (GOAL.x + 10, GOAL.y + 10)
    window_dimensions = ((GOAL.x + 10) * 4, (GOAL.y + 10) * 4)
    window = pygame.display.set_mode(window_dimensions)
    draw.draw_scene(window, obstacles)
    draw.draw_goal(window, GOAL)
    pygame.display.flip()
    path = get_path(obstacles, bounds)
    interpolated_path = draw.interpolate_path(path)
    clear_images()
    for node in interpolated_path:
        draw.draw_scene(window, obstacles)
        draw.draw_goal(window, GOAL)
        draw.draw_node(window, node[0], node[1], node[2])
        pygame.display.flip()
        time.sleep(0.005)

if __name__ == "__main__":
    while True:
        main()
