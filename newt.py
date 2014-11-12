"""Newtonian physics specificiations"""

import pathing
import math
import pygame
import time
import random
import itertools
from collections import namedtuple

class NewtNode:
    def __init__(self, node):
        self.x = node[0]
        self.y = node[1]
        self.v_x = node[2]
        self.v_y = node[3]
        self.angle = node[4]

    # dummy sort
    def __lt__(self, other):
        return True
    

NEWT_START = NewtNode((0, 0, 0, 0, 0))
NEWT_GOAL = NewtNode((70, 70, 0, 0, 0))
ACCELERATION = 0.2
TURNING_ANGLE = math.pi / 8
DRAW_SCALE = 10

def generate_obstacle():
    """generate random obstacle"""
    radius = int(random.random() * 15)
    position = (int(random.random() * 50 + 5), int(random.random() * 50 + 5))
    return (radius, position)

def adj_position(node):
    """determines position for the next time step"""
    return [(node.x + node.v_x, node.y + node.v_y)]

def adj_velocities(node):
    """choices are burn or cruise"""
    delta_v_x = math.cos(node.angle) * ACCELERATION
    delta_v_y = math.sin(node.angle) * ACCELERATION
    cruise = (node.v_x, node.v_y)
    burn = (node.v_x + delta_v_x, node.v_y + delta_v_y)
    return [cruise, burn]

def adj_angles(node):
    """determines adjacent angles based on turning choice"""
    angle = node.angle
    adj_angles_unnormalized = [angle,
                               angle - TURNING_ANGLE,
                               angle + TURNING_ANGLE]
    adj_angles_normalized = [a % (2 * math.pi) for a in adj_angles_unnormalized]
    random.shuffle(adj_angles_normalized)
    return adj_angles_normalized

def newt_adjacent(node):
    """finds possible adjacent nodes based on burn and turn choices"""
    adj_nodes = []
    for pos in adj_position(node):
        for vel in adj_velocities(node):
            for angle in adj_angles(node):
                adj_node = NewtNode((pos[0], pos[1], vel[0], vel[1], angle))
                adj_nodes.append(adj_node)
    return adj_nodes

def newt_heuristic(node, goal, obstacles):
    """newtonian physics heuristic for A*"""
    for obstacle in obstacles:
        radius = obstacle[0]
        pos_x, pos_y = obstacle[1]
        if math.sqrt((node[0]-pos_x)**2 + (node[1]-pos_y)**2) < radius:
            return 100
    pos_distance = math.sqrt((goal.x-node.x)**2 + (goal.y-node.y)**2)
    opt_v_x = (goal.x-node.x) * ACCELERATION * 0.5
    opt_v_y = (goal.y-node.y) * ACCELERATION * 0.5
    vel_distance = math.sqrt((opt_v_x-node.v_x)**2 + (opt_v_y-node.v_y)**2)
    return 1.01 * (pos_distance + vel_distance)

def newt_success(node, goal):
    """success function for A*"""
    pos_distance = math.sqrt((goal.x-node.x)**2 + (goal.y-node.y)**2)
    return pos_distance < 50

def draw_obstacles(window, obstacles):
    """draw obstacles"""
    for obstacle in obstacles:
        obstacle_location = (obstacle[1][0] * DRAW_SCALE,
                             obstacle[1][1] * DRAW_SCALE)
        pygame.draw.circle(window,
                           (255, 50, 255),
                           obstacle_location,
                           obstacle[0])

def draw_node(window, node):
    """draw node"""
    node_color = (255, 255, 255)
    node_radius = 10
    node_position = (int(node.x * DRAW_SCALE), int(node.y * DRAW_SCALE))
    pygame.draw.circle(window, (255, 100, 100), (700, 700), 10)
    pygame.draw.circle(window, node_color, node_position, node_radius)
    angle_length = 25
    angle = node.angle
    angle_point = (int((node.x * DRAW_SCALE)
                       + (math.cos(angle) * angle_length)),
                   int((node.y * DRAW_SCALE)
                       + (math.sin(angle) * angle_length)))
    pygame.draw.line(window, node_color, node_position, angle_point)
    
if __name__ == "__main__":
    NUM_OBSTACLES = 0
    OBSTACLES = itertools.repeat(generate_obstacle(), NUM_OBSTACLES)
    PATH = pathing.a_star(NEWT_START,
                          NEWT_GOAL,
                          newt_adjacent,
                          lambda n, g: newt_heuristic(n, g, OBSTACLES),
                          newt_success)
    WINDOW = pygame.display.set_mode((90 * DRAW_SCALE, 90 * DRAW_SCALE))
    save = True
    while True:
        for screen, node in enumerate(PATH):
            WINDOW.fill((0, 0, 0))
            draw_node(WINDOW, node)
            time.sleep(0.02)
            pygame.display.flip()
            if save:
                pygame.image.save(WINDOW, str(screen).zfill(4) + "screen.jpg")
        save = False
