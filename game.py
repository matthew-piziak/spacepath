"""Game runner"""

import newt
import pygame
import random
import pathing
import math
import time

DRAW_SCALE = 10
NUM_OBSTACLES = 2

class Obstacle(object):
    """wrapper for obstacles"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def generate_obstacle():
    """generate random obstacle"""
    MAXIMUM_OBSTACLE_RADIUS = 15
    MAX_X_POSITION = newt.NEWT_GOAL.x - MAXIMUM_OBSTACLE_RADIUS
    MAX_Y_POSITION = newt.NEWT_GOAL.y - MAXIMUM_OBSTACLE_RADIUS
    radius = int(random.random() * MAXIMUM_OBSTACLE_RADIUS)
    x_position = int(random.random() * MAX_X_POSITION)
    y_position = int(random.random() * MAX_Y_POSITION)
    return Obstacle(x_position, y_position, radius)
        
def draw_obstacles(window, obstacles):
    """draw obstacles"""
    for obstacle in obstacles:
        obstacle_location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
        pygame.draw.circle(window,
                           (255, 50, 255),
                           obstacle_location,
                           obstacle.radius)

def draw_node(window, node):
    """draw node"""
    node_color = (255, 255, 255)
    node_radius = 10
    node_position = (int(node.x * DRAW_SCALE), int(node.y * DRAW_SCALE))
    pygame.draw.circle(window, (255, 100, 100), (700, 700), 10)
    pygame.draw.circle(window, node_color, node_position, node_radius)
    angle_length = 25
    angle = node.angle
    angle_point = (int((node.x * DRAW_SCALE) + (math.cos(angle) * angle_length)),
                   int((node.y * DRAW_SCALE) + (math.sin(angle) * angle_length)))
    pygame.draw.line(window, node_color, node_position, angle_point)

if __name__ == "__main__":
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacle = generate_obstacle()
        obstacles.append(obstacle)
    PATH = pathing.a_star(newt.NEWT_START,
                          newt.NEWT_GOAL,
                          newt.adjacent,
                          lambda n, g: newt.heuristic(n, g, obstacles),
                          newt.success)
    WINDOW = pygame.display.set_mode((90 * DRAW_SCALE, 90 * DRAW_SCALE))
    save = True
    while True:
        for screen, node in enumerate(PATH):
            WINDOW.fill((0, 0, 0))
            draw_node(WINDOW, node)
            draw_obstacles(WINDOW, obstacles)
            time.sleep(0.02)
            pygame.display.flip()
            if save:
                pygame.image.save(WINDOW, str(screen).zfill(4) + "screen.jpg")
        save = False
