"""Game runner"""

import newt
import pygame
import random
import pathing
import math
import time

# drawing constants
NODE_RADIUS = 10
DRAW_SCALE = 3
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = NODE_RADIUS * 2

# obstacle constants
NUM_OBSTACLES = 6

class Obstacle(object):
    """an obstacle for the path to avoid"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, window):
        """draw obstacle"""
        location = (self.x * DRAW_SCALE, self.y * DRAW_SCALE)
        radius = (self.radius * DRAW_SCALE) - NODE_RADIUS
        pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 25
    max_x_position = newt.GOAL.x - maximum_obstacle_radius
    max_y_position = newt.GOAL.y - maximum_obstacle_radius
    min_x_position = newt.START.x + maximum_obstacle_radius
    min_y_position = newt.START.y + maximum_obstacle_radius
    radius = random.randint(NODE_RADIUS + 1, maximum_obstacle_radius)
    x = random.randint(min_x_position, max_x_position)
    y = random.randint(min_y_position, max_y_position)
    return Obstacle(x, y, radius)


def draw_goal(window):
    """draw goal"""
    position = (newt.GOAL.x * DRAW_SCALE, newt.GOAL.y * DRAW_SCALE)
    pygame.draw.circle(window, GOAL_COLOR, position, NODE_RADIUS)

def draw_node(window, node):
    """draw node"""
    node_x = int(node.x * DRAW_SCALE)
    node_y = int(node.y * DRAW_SCALE)
    angle_x = int(node_x + math.cos(node.angle) * ANGLE_LENGTH)
    angle_y = int(node_y + math.sin(node.angle) * ANGLE_LENGTH)
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), NODE_RADIUS)
    pygame.draw.line(window, NODE_COLOR, (node_x, node_y), (angle_x, angle_y))

def draw_scene(window, obstacles):
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        obstacle.draw(window)
    
if __name__ == "__main__":
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    window = pygame.display.set_mode((360 * DRAW_SCALE, 240 * DRAW_SCALE))
    draw_scene(window, obstacles)
    draw_goal(window)
    pygame.display.flip()
    PATH = pathing.a_star(newt.START,
                          newt.GOAL,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    if len(PATH) == 1:
        draw_scene(window, obstacles)
        draw_node(window, PATH[0])
        for adj in newt.adjacent(PATH[0]):
            draw_node(window, adj)
        pygame.display.flip()
        time.sleep(3)
        exit()
    for screen, node in enumerate(PATH):
        draw_scene(window, obstacles)
        draw_node(window, node)
        draw_goal(window)
        time.sleep(0.03)
        pygame.display.flip()
        pygame.image.save(window, str(screen).zfill(4) + "screen.png")
    while True:
        for screen, node in enumerate(PATH):
            draw_scene(window, obstacles)
            draw_node(window, node)
            draw_goal(window)
            time.sleep(0.03)
            pygame.display.flip()
