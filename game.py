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
from scipy import interpolate
import numpy as np

# obstacle constants
NUM_OBSTACLES = 16

# drawing constants
NODE_RADIUS = 12
DRAW_SCALE = 16
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = NODE_RADIUS * 1.5

# nodes
START = newt.Node(0, 0, 0, 0, 0)
GOAL = newt.Node(70, 30, 0, 0, 0)

def draw_obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    radius = (obstacle.radius * DRAW_SCALE) - int(2.8 * DRAW_SCALE)
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 10
    max_x_position = GOAL.x - maximum_obstacle_radius
    max_y_position = GOAL.y - maximum_obstacle_radius
    min_x_position = START.x + maximum_obstacle_radius
    min_y_position = START.y + maximum_obstacle_radius
    radius = random.randint((NODE_RADIUS // DRAW_SCALE) + 3, maximum_obstacle_radius)
    x = random.randint(min_x_position, max_x_position)
    y = random.randint(min_y_position, max_y_position)
    return newt.Circle(x, y, radius)


def draw_goal(window):
    """draw goal"""
    position = (GOAL.x * DRAW_SCALE, GOAL.y * DRAW_SCALE)
    pygame.draw.circle(window, GOAL_COLOR, position, NODE_RADIUS * 4)
def draw_node(window, node):
    """draw node"""
    node_x = int(node.x * DRAW_SCALE)
    node_y = int(node.y * DRAW_SCALE)
    angle_x = int(node_x + math.cos(node.angle) * ANGLE_LENGTH)
    angle_y = int(node_y + math.sin(node.angle) * ANGLE_LENGTH)
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), NODE_RADIUS)
    pygame.draw.line(window, NODE_COLOR, (node_x, node_y), (angle_x, angle_y))

def draw_dot(window, x, y):
    node_x = int(x * DRAW_SCALE)
    node_y = int(y * DRAW_SCALE)
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), NODE_RADIUS)

def draw_scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        draw_obstacle(window, obstacle)

def main():
    """break this out"""
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    window = pygame.display.set_mode(((GOAL.x + 10) * DRAW_SCALE, (GOAL.y + 10) * DRAW_SCALE))
    draw_scene(window, obstacles)
    draw_goal(window)
    pygame.display.flip()
    path = pathing.a_star(START,
                          GOAL,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)
    node_x = []
    node_y = []
    for node in path:
        node_x.append(node.x)
        node_y.append(node.y)
    node_x.append(GOAL.x)
    node_y.append(GOAL.y)
    t = np.arange(0, len(node_x))
    f_x = interpolate.interp1d(t, node_x, 'cubic')
    f_y = interpolate.interp1d(t, node_y, 'cubic')
    t_new = np.arange(0, len(node_x) - 2, 0.2)
    x_i = f_x(t_new)
    y_i = f_y(t_new)
    for i in range(len(t_new)):
        draw_scene(window, obstacles)
        draw_goal(window)
        draw_dot(window, x_i[i], y_i[i])
        pygame.display.flip()
        pygame.image.save(window, str(i).zfill(4) + "screen.png")
    print("label: " + str(int(time.time())))
    gif_command = "bash make_gif.sh maneuver" + str(int(time.time())) + ".gif"
    subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()
