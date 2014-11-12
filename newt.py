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

    # sort arbitarily
    def __lt__(self, other):
        return True

START = NewtNode(0, 0, 0, 0, 0)
GOAL = NewtNode(random.randint(50, 150), random.randint(50, 150), 0, 0, 0)
ACCELERATION = 1

def adj_position(node):
    """determines position for the next time step"""
    return [(node.x + node.v_x, node.y + node.v_y)]

def adj_velocities(node):
    """choices are burn or cruise"""
    angle = node.angle * (1 / 8) * 2 * math.pi
    delta_v_x = int(math.cos(angle) * ACCELERATION)
    delta_v_y = int(math.sin(angle) * ACCELERATION)
    cruise = (node.v_x, node.v_y)
    burn = (node.v_x + delta_v_x, node.v_y + delta_v_y)
    return [burn, cruise]

def adj_angles(node):
    """determines adjacent angles based on turning choice"""
    adj_angles_unnormalized = [node.angle - 1,
                               node.angle + 1,
                               node.angle]
    adj_angles_normalized = [a % 8 for a in adj_angles_unnormalized]
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

def circle_contains(x, y, c_x, c_y, c_r):
    dx = abs(x - c_x)
    dy = abs(y - c_y)
    if dx > c_r:
        return False
    if dy > c_r:
        return False
    if dx + dy <= c_r:
        return True
    return dx**2 + dy**2 <= c_r**2


def heuristic(node, goal, obstacles):
    """newtonian physics heuristic for A*"""
    for obstacle in obstacles:
        if circle_contains(node.x, node.y, obstacle.x, obstacle.y, obstacle.radius):
            return 1000000
    distance = 0
    x = node.x
    y = node.y
    while True:
        x += node.v_x
        y += node.v_y
        r = (distance**2) * ACCELERATION * 0.5
        if circle_contains(goal.x, goal.y, x, y, r):
            return distance
        distance += 1
        
def success(node, goal):
    """success function for A*"""
    return circle_contains(node.x, node.y, goal.x, goal.y, 20)


