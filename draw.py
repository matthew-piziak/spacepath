"""Game rendering functions"""

import pygame
import numpy
import math
from scipy import interpolate

# drawing constants
NODE_RADIUS = 3
DRAW_SCALE = 4
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = 2 * NODE_RADIUS

# interpolation
INTERPOLATE = True
INTERPOLATION_FACTOR = 16

def draw_obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    node_overlap = int(NODE_RADIUS * DRAW_SCALE * 1.3)
    radius = (obstacle.radius * DRAW_SCALE) - node_overlap
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def draw_goal(window, goal):
    """draw goal"""
    position = (goal.x * DRAW_SCALE, goal.y * DRAW_SCALE)
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
    t = numpy.arange(0, len(node_positions))
    f_x = interpolate.interp1d(t, [p[0] for p in node_positions], 'cubic')
    f_y = interpolate.interp1d(t, [p[1] for p in node_positions], 'cubic')
    t_new = numpy.arange(0, len(node_positions) - 2, 1.0 / INTERPOLATION_FACTOR)
    interpolated_x = f_x(t_new)
    interpolated_y = f_y(t_new)
    interpolated_angle = interpolate_angles([p[2] for p in node_positions])
    return zip(interpolated_x, interpolated_y, interpolated_angle)
