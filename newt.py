"""Newtonian physics specificiations"""

import math
from collections import namedtuple

Node = namedtuple('Node', ['x', 'y', 'v_x', 'v_y', 'angle'])
Circle = namedtuple('Circle', ['x', 'y', 'radius'])

def adj_position(node):
    """determines position for the next time step"""
    return [(node.x + node.v_x, node.y + node.v_y)]

def adj_velocities(node):
    """assumes acceleration = 2 to use fast sine and cosine"""
    angle = node.angle
    sin = {0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: -1, 6: -1, 7: -1}
    cos = {0: 1, 1: 1, 2: 0, 3: -1, 4: -1, 5: -1, 6: 0, 7: 1}
    delta_v_x = cos[angle]
    delta_v_y = sin[angle]
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
                adj_node = Node(pos[0], pos[1], vel[0], vel[1], angle)
                adj_nodes.append(adj_node)
    return adj_nodes

def circle_contains_node(circle, node):
    """returns whether the node is contained in the circle"""
    dx = abs(node.x - circle.x)
    dy = abs(node.y - circle.y)
    if dx > circle.radius:
        return False
    if dy > circle.radius:
        return False
    if dx + dy <= circle.radius:
        return True
    return (dx ** 2) + (dy ** 2) <= circle.radius ** 2

def heuristic(node, goal, obstacles):
    """newtonian physics heuristic for A*"""
    for obstacle in obstacles:
        circle = Circle(obstacle.x, obstacle.y, obstacle.radius)
        if circle_contains_node(circle, node):
            return 1000000
    acceleration = 2 # hardcoded for sine and cosine optimization
    heuristic_x = ((-1 * node.v_x) - (2 * goal.v_x)
                   + math.sqrt((7 * (goal.v_x ** 2))
                               + (2 * (node.v_x ** 2))
                               + (4 * acceleration * abs(goal.x - node.x)))) / 2
    heuristic_y = ((-1 * node.v_y) - (2 * goal.v_y)
                   + math.sqrt((7 * (goal.v_y ** 2))
                               + (2 * (node.v_y ** 2))
                               + (4 * acceleration * abs(goal.y - node.y)))) / 2
    return heuristic_x + heuristic_y

def success(node, goal):
    """success function for A*"""
    success_radius = 4
    success_region = Circle(goal.x, goal.y, success_radius)
    location = circle_contains_node(success_region, node)
    speed = abs(node.v_x - goal.v_x) + abs(node.v_y - goal.v_y) == 0
    return location and speed
