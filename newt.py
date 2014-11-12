"""Newtonian physics specificiations"""

import math
import random

class NewtNode(object):
    """wrapper for node tuples"""
    def __init__(self, x, y, v_x, v_y, angle):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.angle = angle

    # sort arbitrarily
    def __lt__(self, other):
        return True

START = NewtNode(0, 0, 0, 0, 0)
GOAL = NewtNode(70, 70, 0, 0, 0)
ACCELERATION = 0.3
TURNING_ANGLE = math.pi / 8

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
    adj_angles_unnormalized = [node.angle,
                               node.angle - TURNING_ANGLE,
                               node.angle + TURNING_ANGLE]
    adj_angles_normalized = [a % (2 * math.pi) for a in adj_angles_unnormalized]
    return adj_angles_normalized

def adjacent(node):
    """finds possible adjacent nodes based on burn and turn choices"""
    adj_nodes = []
    for pos in adj_position(node):
        for vel in adj_velocities(node):
            for angle in adj_angles(node):
                adj_node = NewtNode(pos[0], pos[1], vel[0], vel[1], angle)
                adj_nodes.append(adj_node)
    return adj_nodes

def heuristic(node, goal, obstacles):
    """newtonian physics heuristic for A*"""
    for obstacle in obstacles:
        dx = abs(node.x - obstacle.x)
        dy = abs(node.y - obstacle.y)
        if dx + dy <= obstacle.radius:
            return 10000
        if dx > obstacle.radius:
            continue
        if dy > obstacle.radius:
            continue
        if dx**2 + dy**2 <= obstacle.radius**2:
            return 10000
    pos_distance = math.sqrt((goal.x-node.x)**2 + (goal.y-node.y)**2)
    opt_v_x = (goal.x-node.x) * ACCELERATION * 0.7
    opt_v_y = (goal.y-node.y) * ACCELERATION * 0.7
    vel_distance =  math.sqrt((opt_v_x-node.v_x)**2 + (opt_v_y-node.v_y)**2)
    return 1.01 * (pos_distance + vel_distance)

def success(node, goal):
    """success function for A*"""
    pos_distance = math.sqrt((goal.x-node.x)**2 + (goal.y-node.y)**2)
    return pos_distance < 2

