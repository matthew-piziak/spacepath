"""Newtonian physics specificiations"""

import math
import obstacle
from collections import namedtuple

Node = namedtuple('Node', ['x', 'y', 'v_x', 'v_y', 'angle'])

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
    velocities = [burn, cruise]
    return velocities

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
                if not vel == (node.v_x, node.v_y):
                    adj_nodes.append((adj_node, "cruise"))
                else:
                    adj_nodes.append((adj_node, "burn"))
    return adj_nodes

def heuristic(node, goal, obstacles, bounds):
    """newtonian physics heuristic for A*"""
    acceleration = 2 # hardcoded for sine and cosine optimization
    def outside_arena():
        """determines if the node is outside permissible bounds"""
        return not (0 < node.x < bounds[0] and 0 < node.y < bounds[1])
    def leaving_arena():
        """determines if the node is moving too fast to remain in the arena"""
        braking_time_x = abs(node.v_x) // acceleration
        braking_time_y = abs(node.v_y) // acceleration
        v_component_x = abs(node.v_x) * braking_time_x
        v_component_y = abs(node.v_y) * braking_time_y
        a_component_x = 0.5 * acceleration * braking_time_x
        a_component_y = 0.5 * acceleration * braking_time_y
        braking_distance_x = v_component_x + a_component_x
        braking_distance_y = v_component_y + a_component_y
        if node.v_x > 0:
            if braking_distance_x > bounds[0] - node.x:
                return True
        if node.v_y > 0:
            if braking_distance_y > bounds[0] - node.y:
                return True
        if node.v_x < -1:
            if braking_distance_x > node.x:
                return True
        if node.v_y < -1:
            if braking_distance_y > node.y:
                return True
    def in_obstacle():
        """determines if the node is inside an obstacle"""
        x = node.x
        y = node.y
        return any([obstacle.contains_node(x, y, o) for o in obstacles])
    h_max = 1000000
    if outside_arena() or leaving_arena() or in_obstacle():
        return h_max
    heuristic_x = (- node.v_x +
                   math.sqrt((2 * (node.v_x ** 2)) +
                             (4 * acceleration * abs(goal.x - node.x)))) / 2
    heuristic_y = (- node.v_y +
                   math.sqrt((2 * (node.v_y ** 2)) +
                             (4 * acceleration * abs(goal.y - node.y)))) / 2
    return 1.02 * (heuristic_x + heuristic_y)

def success(node, goal):
    """success function for A*"""
    success_radius = 6
    success_region = obstacle.Obstacle(goal.x, goal.y, success_radius)
    location = obstacle.contains_node(node.x, node.y, success_region)
    speed = abs(node.v_x - goal.v_x) + abs(node.v_y - goal.v_y) == 0
    return location and speed
