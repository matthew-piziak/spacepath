"""Game runner"""

import newt
import pygame
import random
import pathing
import time
import subprocess
import os
from scipy import interpolate
import numpy as np

# obstacle constants
NUM_OBSTACLES = 16

# drawing constants
NODE_RADIUS = 1
DRAW_SCALE = 16
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)

# nodes
START = newt.Node(0, 0, 0, 0, 0)
GOAL = newt.Node(70, 30, 0, 0, 0)

def draw_obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    radius = (obstacle.radius * DRAW_SCALE) - int(NODE_RADIUS * DRAW_SCALE)
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 10
    minimum_obstacle_radius = NODE_RADIUS
    max_x_position = GOAL.x - maximum_obstacle_radius
    max_y_position = GOAL.y - maximum_obstacle_radius
    min_x_position = START.x + maximum_obstacle_radius
    min_y_position = START.y + maximum_obstacle_radius
    radius = random.randint(minimum_obstacle_radius, maximum_obstacle_radius)
    x = random.randint(min_x_position, max_x_position)
    y = random.randint(min_y_position, max_y_position)
    return newt.Circle(x, y, radius)

def draw_goal(window):
    """draw goal"""
    position = (GOAL.x * DRAW_SCALE, GOAL.y * DRAW_SCALE)
    goal_draw_radius = NODE_RADIUS * DRAW_SCALE * 3
    pygame.draw.circle(window, GOAL_COLOR, position, goal_draw_radius)

def draw_node(window, x, y):
    """draw node"""
    node_x = int(x * DRAW_SCALE)
    node_y = int(y * DRAW_SCALE)
    node_draw_radius = NODE_RADIUS * DRAW_SCALE
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), node_draw_radius)

def draw_scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        draw_obstacle(window, obstacle)

def get_path(obstacles):
    """return nodes in path from A*"""
    heuristic = lambda n, g: newt.heuristic(n, g, obstacles)
    return pathing.a_star(START, GOAL, newt.adjacent, heuristic, newt.success)

def clear_images():
    """delete all PNGs from program directory"""
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)

def interpolate_path(path):
    """generate a higher resolution path using cubic spline interpolation"""
    interpolation_factor = 5
    node_positions = [(n.x, n.y) for n in path]
    node_positions.append((GOAL.x, GOAL.y))
    t = np.arange(0, len(node_positions))
    f_x = interpolate.interp1d(t, [p[0] for p in node_positions], 'cubic')
    f_y = interpolate.interp1d(t, [p[1] for p in node_positions], 'cubic')
    t_new = np.arange(0, len(node_positions) - 2, 1.0 / interpolation_factor)
    return zip(f_x(t_new), f_y(t_new))

def main():
    """generate path and render"""
    clear_images()
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    window_dimensions = ((GOAL.x + 10) * DRAW_SCALE, (GOAL.y + 10) * DRAW_SCALE)
    window = pygame.display.set_mode(window_dimensions)
    draw_scene(window, obstacles)
    draw_goal(window)
    pygame.display.flip()
    path = get_path(obstacles)
    interpolated_path = interpolate_path(path)
    for i, node in enumerate(interpolated_path):
        draw_scene(window, obstacles)
        draw_goal(window)
        draw_node(window, node[0], node[1])
        pygame.display.flip()
        pygame.image.save(window, str(i).zfill(4) + "screen.png")
    print("label: " + str(int(time.time())))
    gif_command = "bash make_gif.sh maneuver" + str(int(time.time())) + ".gif"
    subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)

if __name__ == "__main__":
    main()
