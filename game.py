"""Game runner"""

import newt
import pygame
import random
import pathing
import math
import time
import subprocess
import os
from collections import namedtuple

# drawing constants
NODE_RADIUS = 12
DRAW_SCALE = 3
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = NODE_RADIUS * 1.5

# obstacle constants
NUM_OBSTACLES = 4

# nodes
START = newt.Node(0, 0, 0, 0, 0)
GOAL = newt.Node(120, 90, 0, 0, 0)
curr = None

def draw_obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    radius = (obstacle.radius * DRAW_SCALE) - NODE_RADIUS
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 15
    max_x_position = GOAL.x - maximum_obstacle_radius
    max_y_position = GOAL.y - maximum_obstacle_radius
    min_x_position = START.x + maximum_obstacle_radius
    min_y_position = START.y + maximum_obstacle_radius
    radius = random.randint(NODE_RADIUS + 1, maximum_obstacle_radius)
    x = random.randint(min_x_position, max_x_position)
    y = random.randint(min_y_position, max_y_position)
    return newt.Circle(x, y, radius)

def draw_node(window, node):
    """draw node"""
    node_x = int(node.x * DRAW_SCALE)
    node_y = int(node.y * DRAW_SCALE)
    angle_x = int(node_x + math.cos(node.angle) * ANGLE_LENGTH)
    angle_y = int(node_y + math.sin(node.angle) * ANGLE_LENGTH)
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), NODE_RADIUS)
    pygame.draw.line(window, NODE_COLOR, (node_x, node_y), (angle_x, angle_y))

def draw_scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        draw_obstacle(window, obstacle)

def do_path(goal, obstacles, window):
    global curr
    if curr is None:
        start = START
    else:
        start = curr
    print("constructing path")
    path = pathing.a_star(start,
                          goal,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    print("path constructed")
    curr = goal
    for screen, node in enumerate(path):
        draw_scene(window, obstacles)
        draw_node(window, node)
        time.sleep(0.03)
        pygame.display.flip()

def main():
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    window = pygame.display.set_mode((240 * DRAW_SCALE, 160 * DRAW_SCALE))
    draw_scene(window, obstacles)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                goal = newt.Node(x // DRAW_SCALE, y // DRAW_SCALE, 0, 0, 0)
                do_path(goal, obstacles, window)

if __name__ == "__main__":
    main()
