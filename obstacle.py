"""Obstacle generator"""

import random
import collections

Obstacle = collections.namedtuple('Obstacle', ['x', 'y', 'radius'])

def get_obstacles(min_x, min_y, max_x, max_y):
    """return an allotment of obstacles"""
    num_obstacles = 6
    generate = lambda: _generate_random_obstacle(min_x, min_y, max_x, max_y)
    return [generate() for _ in range(0, random.randint(1, num_obstacles))]

def contains_node(x, y, obstacle):
    """returns whether the node is contained in the obstacle"""
    dx = abs(x - obstacle.x)
    dy = abs(y - obstacle.y)
    if dx > obstacle.radius:
        return False
    if dy > obstacle.radius:
        return False
    if dx + dy <= obstacle.radius:
        return True
    return (dx ** 2) + (dy ** 2) <= obstacle.radius ** 2

def _generate_random_obstacle(min_x, min_y, max_x, max_y):
    """generate random obstacle"""
    maximum_obstacle_radius = 18
    minimum_obstacle_radius = 12
    radius = random.randint(minimum_obstacle_radius, maximum_obstacle_radius)
    x = random.randint(min_x + radius, max_x - radius)
    y = random.randint(min_y + radius, max_y - radius)
    return Obstacle(x, y, radius)
