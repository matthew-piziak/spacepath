"""Game rendering functions"""

import pygame
import math
import interpolate
import time

# drawing constants
NODE_RADIUS = 3
DRAW_SCALE = 6
NODE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (100, 100, 100)
GOAL_COLOR = (100, 100, 255)
BACKGROUND_COLOR = (0, 0, 0)
ANGLE_LENGTH = 1.5 * NODE_RADIUS

# animation
FRAME_STEP = 0.01

class Ship(pygame.sprite.Sprite):
    """Represents the ship"""
    # pylint: disable=R0903
    # This is a necessary extension of the sprite class, so the 'Too
    # few public methods' pylint warning can be ignored.

    def __init__(self, x, y, angle, action):
        scale = NODE_RADIUS * DRAW_SCALE * 2
        images = {"cruise": "ship.png", "burn": "ship_burn.png"}
        self.image = pygame.image.load(images[action])
        self.image = pygame.transform.smoothscale(self.image,
                                                  (scale, scale))
        def rot_center(angle):
            """rotate an image while keeping its center and size"""
            orig_rect = self.image.get_rect()
            rot_image = pygame.transform.rotate(self.image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            self.image = rot_image
        rot_center(-90)
        rot_center(-1 * angle * 45)
        self.rect = self.image.get_rect()
        self.x = x * DRAW_SCALE
        self.y = y * DRAW_SCALE

    def draw(self, surface):
        """Draw ship sprite to surface."""
        surface.blit(self.image, (self.x, self.y))

def init(obstacles, goal):
    """draw initial scene and obstacles"""
    window_dimensions = ((goal.x + 10) * DRAW_SCALE, (goal.y + 10) * DRAW_SCALE)
    window = pygame.display.set_mode(window_dimensions)
    _scene(window, obstacles)
    _goal(window, goal)
    return window

def animate_path(window, obstacles, goal, path):
    """animate path"""
    path[0] = (path[0], "cruise")
    interpolated_path = interpolate.interpolate_path(path)
    for node, action in interpolated_path:
        _scene(window, obstacles)
        _goal(window, goal)
        ship = Ship(node[0], node[1], node[2], action)
        ship.draw(window)
        pygame.display.flip()
        time.sleep(0.01)

def _obstacle(window, obstacle):
    """draw obstacle"""
    location = (obstacle.x * DRAW_SCALE, obstacle.y * DRAW_SCALE)
    node_overlap = int(NODE_RADIUS * DRAW_SCALE * 2)
    radius = (obstacle.radius * DRAW_SCALE) - node_overlap
    pygame.draw.circle(window, OBSTACLE_COLOR, location, radius)

def _goal(window, goal):
    """draw goal"""
    position = (goal.x * DRAW_SCALE, goal.y * DRAW_SCALE)
    goal_draw_radius = NODE_RADIUS * DRAW_SCALE * 4
    pygame.draw.circle(window, GOAL_COLOR, position, goal_draw_radius)

def _node(window, x, y, angle, action):
    """draw node"""
    node_x = int(x * DRAW_SCALE)
    node_y = int(y * DRAW_SCALE)
    node_draw_radius = NODE_RADIUS * DRAW_SCALE
    pygame.draw.circle(window, NODE_COLOR, (node_x, node_y), node_draw_radius)
    node_angle = (math.pi / 4) * float(angle)
    origin = (node_x, node_y)
    angle_length_multiplier = DRAW_SCALE * ANGLE_LENGTH
    angle_x = (-1 * math.cos(node_angle) * angle_length_multiplier) + node_x
    angle_y = (-1 * math.sin(node_angle) * angle_length_multiplier) + node_y
    angle_tip = (angle_x, angle_y)
    angle_color = NODE_COLOR
    if action == "burn":
        angle_color = GOAL_COLOR
    pygame.draw.line(window, angle_color, origin, angle_tip, 10)

def _scene(window, obstacles):
    """draw scene"""
    window.fill(BACKGROUND_COLOR)
    for obstacle in obstacles:
        _obstacle(window, obstacle)
