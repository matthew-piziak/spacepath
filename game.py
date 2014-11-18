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
NUM_OBSTACLES = random.randint(2, 8)

# nodes
START = newt.NewtNode(0, 0, 0, 0, 0)
GOAL = newt.NewtNode(random.randint(70, 200), random.randint(70, 150), 0, 0, 0)

Obstacle = namedtuple('Obstacle', ['x', 'y', 'radius'])

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
    return Obstacle(x, y, radius)


def draw_goal(window):
    """draw goal"""
    position = (GOAL.x * DRAW_SCALE, GOAL.y * DRAW_SCALE)
    pygame.draw.circle(window, GOAL_COLOR, position, NODE_RADIUS * 2)

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

def main():
    """break this out"""
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    window = pygame.display.set_mode((240 * DRAW_SCALE, 160 * DRAW_SCALE))
    draw_scene(window, obstacles)
    draw_goal(window)
    pygame.display.flip()
    path = pathing.a_star(START,
                          GOAL,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    if len(path) == 1:
        draw_scene(window, obstacles)
        draw_node(window, path[0])
        for adj in newt.adjacent(path[0]):
            draw_node(window, adj)
        pygame.display.flip()
        time.sleep(3)
        exit()
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)
    for screen, node in enumerate(path):
        draw_scene(window, obstacles)
        draw_goal(window)
        draw_node(window, node)
        time.sleep(0.03)
        pygame.display.flip()
        pygame.image.save(window, str(screen).zfill(4) + "screen.png")
    print("label: " + str(int(time.time())))
    gif_command = "bash make_gif.sh maneuver" + str(int(time.time())) + ".gif"
    subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)

if __name__ == "__main__":
    while True:
        main()
