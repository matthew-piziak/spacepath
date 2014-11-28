"""Game rendering functions"""

import pygame
import math
import interpolate
import time

# drawing constants
NODE_RADIUS = 3
DRAW_SCALE = 4
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = 2 * NODE_RADIUS

# animation
FRAME_STEP = 0.005

def init(obstacles, GOAL):
    window_dimensions = ((GOAL.x + 10) * DRAW_SCALE, (GOAL.y + 10) * DRAW_SCALE)
    window = pygame.display.set_mode(window_dimensions)
    _scene(window, obstacles)
    _goal(window, GOAL)
    return window

def path(window, obstacles, GOAL, path):
    interpolated_path = interpolate.path(path)
    for node in interpolated_path:
        _scene(window, obstacles)
        _goal(window, GOAL)
        _node(window, node[0], node[1], node[2])
        pygame.display.flip()
        time.sleep(FRAME_STEP)

def _obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    node_overlap = int(NODE_RADIUS * DRAW_SCALE * 1.3)
    radius = (obstacle.radius * DRAW_SCALE) - node_overlap
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def _goal(window, goal):
    """draw goal"""
    position = (goal.x * DRAW_SCALE, goal.y * DRAW_SCALE)
    goal_draw_radius = NODE_RADIUS * DRAW_SCALE * 4
    pygame.draw.circle(window, GOAL_COLOR, position, goal_draw_radius)

def _node(window, x, y, angle):
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

def _scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        _obstacle(window, obstacle)

