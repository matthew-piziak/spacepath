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

# obstacle constants
NUM_OBSTACLES = 12

# interpolation
INTERPOLATE = True
INTERPOLATION_FACTOR = 16

# drawing constants
NODE_RADIUS = 3
DRAW_SCALE = 4
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = 2 * NODE_RADIUS

# nodes
START = newt.Node(0, 0, 0, 0, 1)
GOAL = newt.Node(160, 160, 0, 0, 0)

def draw_obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    node_overlap = int(NODE_RADIUS * DRAW_SCALE * 1.3)
    radius = (obstacle.radius * DRAW_SCALE) - node_overlap
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 18
    minimum_obstacle_radius = NODE_RADIUS * 4
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
    goal_draw_radius = NODE_RADIUS * DRAW_SCALE * 4
    pygame.draw.circle(window, GOAL_COLOR, position, goal_draw_radius)

def draw_node(window, x, y, angle):
    """draw node"""
    node_x = int(x * DRAW_SCALE)
    node_y = int(y * DRAW_SCALE)
    node_draw_radius = NODE_RADIUS * DRAW_SCALE
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), node_draw_radius)
    node_angle = (math.pi / 4) * float(angle)
    origin = (node_x, node_y)
    angle_length_multiplier = DRAW_SCALE * ANGLE_LENGTH
    angle_x = (math.cos(node_angle) * angle_length_multiplier) + node_x
    angle_y = (math.sin(node_angle) * angle_length_multiplier) + node_y
    angle_tip = (angle_x, angle_y)
    pygame.draw.line(window, NODE_COLOR, origin, angle_tip, 2)

def draw_scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        draw_obstacle(window, obstacle)

def get_path(obstacles, bounds):
    """return nodes in path from A*"""
    heuristic = lambda n, g: newt.heuristic(n, g, obstacles, bounds)
    return pathing.a_star(START, GOAL, newt.adjacent, heuristic, newt.success)

def clear_images():
    """delete all PNGs from program directory"""
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)

def interpolate_angles(angles):
    """custom linear modulus interpolation for angles"""
    interpolated_angles = []
    fraction = 1.0 / INTERPOLATION_FACTOR
    for i in range(len(angles) - 1):
        start_angle = float(angles[i])
        end_angle = float(angles[i + 1])
        if abs(end_angle - start_angle) <= 4:
            for j in range(INTERPOLATION_FACTOR):
                start_factor = (INTERPOLATION_FACTOR - j) * start_angle
                end_factor = j * end_angle
                interpolated_angle = (start_factor + end_factor) * fraction
                interpolated_angles.append(interpolated_angle)
        else:
            for j in range(INTERPOLATION_FACTOR):
                if start_angle < 4:
                    start_angle += 8
                if end_angle < 4:
                    end_angle += 8
                start_factor = (INTERPOLATION_FACTOR - j) * start_angle
                end_factor = j * end_angle
                interpolated_angle = start_factor + end_factor
                interpolated_angle = (interpolated_angle * fraction) % 8
                interpolated_angles.append(interpolated_angle)
    return interpolated_angles

def interpolate_path(path):
    """generate a higher resolution path using cubic spline interpolation"""
    node_positions = [(n.x, n.y, n.angle) for n in path]
    if not INTERPOLATE:
        return node_positions
    node_positions.append((GOAL.x, GOAL.y, GOAL.angle))
    t = np.arange(0, len(node_positions))
    f_x = interpolate.interp1d(t, [p[0] for p in node_positions], 'cubic')
    f_y = interpolate.interp1d(t, [p[1] for p in node_positions], 'cubic')
    t_new = np.arange(0, len(node_positions) - 2, 1.0 / INTERPOLATION_FACTOR)
    interpolated_x = f_x(t_new)
    interpolated_y = f_y(t_new)
    interpolated_angle = interpolate_angles([p[2] for p in node_positions])
    return zip(interpolated_x, interpolated_y, interpolated_angle)

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
    window_dimensions = ((GOAL.x + 10) * DRAW_SCALE, (GOAL.y + 10) * DRAW_SCALE)
    window = pygame.display.set_mode(window_dimensions)
    draw_scene(window, obstacles)
    draw_goal(window)
    pygame.display.flip()
    path = get_path(obstacles, bounds)
    interpolated_path = interpolate_path(path)
    clear_images()
    for node in interpolated_path:
        draw_scene(window, obstacles)
        draw_goal(window)
        draw_node(window, node[0], node[1], node[2])
        pygame.display.flip()
        time.sleep(0.005)

if __name__ == "__main__":
    while True:
        main()
