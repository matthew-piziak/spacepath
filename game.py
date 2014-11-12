"""Game runner"""

import newt
import pygame
import random
import pathing
import math
import time

# drawing constants
NODE_RADIUS = 10
DRAW_SCALE = 10
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = 25

# obstacle constants
NUM_OBSTACLES = 4

class Obstacle(object):
    """an obstacle for the path to avoid"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, window):
        """draw obstacle"""
        location = (self.x * DRAW_SCALE, self.y * DRAW_SCALE)
        radius = self.radius * DRAW_SCALE
        pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def generate_random_obstacle():
    """generate random obstacle"""
    maximum_obstacle_radius = 15
    max_x_position = newt.GOAL.x - maximum_obstacle_radius
    max_y_position = newt.GOAL.y - maximum_obstacle_radius
    radius = int(random.random() * maximum_obstacle_radius)
    x = int(random.random() * max_x_position)
    y = int(random.random() * max_y_position)
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

if __name__ == "__main__":
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_random_obstacle()
        obstacles.append(obstacle)
    PATH = pathing.a_star(newt.START,
                          newt.GOAL,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    for screen, node in enumerate(PATH):
        WINDOW = pygame.display.set_mode((90 * DRAW_SCALE, 90 * DRAW_SCALE))
        WINDOW.fill(BACKGROUND_COLOR)
        for obstacle in obstacles:
            obstacle.draw(WINDOW)
        draw_node(WINDOW, node)
        draw_goal(WINDOW)
        time.sleep(0.03)
        pygame.display.flip()
        # pygame.image.save(WINDOW, str(screen).zfill(4) + "screen.png")
