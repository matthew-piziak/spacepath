import pathing
import math
import pygame
import sys
import time
import random

NEWT_START = (0, 0, 0, 0, 0)
NEWT_GOAL = (70, 70, 0, 0, 0)
ACCELERATION = 0.2
TURNING_ANGLE = math.pi / 8
DRAW_SCALE = 10

obstacles = []

def obstacle():
    radius = int(random.random() * 15)
    position = (int(random.random() * 50 + 5), int(random.random() * 50 + 5))
    obstacles.append((radius, position))
    
def adj_position(x, y, v_x, v_y):
    return [(x + v_x, y + v_y)]

def adj_velocities(v_x, v_y, angle):
    delta_v_x = math.cos(angle) * ACCELERATION
    delta_v_y = math.sin(angle) * ACCELERATION
    return [(v_x, v_y), (v_x + delta_v_x, v_y + delta_v_y)]

def adj_angles(angle):
    adj_angles = [angle, angle - TURNING_ANGLE, angle + TURNING_ANGLE]
    adj_angles_normalized =  [a % (2 * math.pi) for a in adj_angles]
    random.shuffle(adj_angles_normalized)
    return adj_angles_normalized
    
def newt_adjacent(node):
    x = node[0]
    y = node[1]
    v_x = node[2]
    v_y = node[3]
    angle = node[4]
    adj_nodes = []
    for p in adj_position(x, y, v_x, v_y):
        for v in adj_velocities(v_x, v_y, angle):
            for a in adj_angles(angle):
                adj_nodes.append((p[0], p[1], v[0], v[1], a))
    return adj_nodes

def newt_heuristic(node, goal):
    for obstacle in obstacles:
        radius = obstacle[0]
        pos_x, pos_y = obstacle[1]
        if math.sqrt((node[0]-pos_x)**2 + (node[1]-pos_y)**2) < radius:
            return 100
    pos_distance = math.sqrt((goal[0]-node[0])**2 + (goal[1]-node[1])**2)
    opt_vel_x = (goal[0]-node[0]) * ACCELERATION * 0.5
    opt_vel_y = (goal[1]-node[1]) * ACCELERATION * 0.5
    vel_distance = math.sqrt((opt_vel_x-node[2])**2 + (opt_vel_y-node[3])**2)
#    vel_distance = math.sqrt((goal[2]-node[2])**2 + (goal[3]-node[3])**2)
    return 1.01 * (pos_distance + vel_distance)
        
def newt_success(node, goal):
    pos_distance = math.sqrt((goal[0]-node[0])**2 + (goal[1]-node[1])**2)
    return pos_distance < 2

def draw_node(window, node):
    node_color = (255, 255, 255)
    node_radius = 10
    node_position = (int(node[0] * DRAW_SCALE), int(node[1] * DRAW_SCALE))
    pygame.draw.circle(window, (255, 100, 100), (700, 700), 10)
    for obstacle in obstacles:
        pygame.draw.circle(window,
                           (255, 50, 255),
                           (obstacle[1][0] * DRAW_SCALE, obstacle[1][1] * DRAW_SCALE),
                           obstacle[0])
    pygame.draw.circle(window, node_color, node_position, node_radius)
    angle_length = 25
    angle = node[4]
    angle_point = (int((node[0] * DRAW_SCALE) + (math.cos(angle) * angle_length)),
                   int((node[1] * DRAW_SCALE) + (math.sin(angle) * angle_length)))
    pygame.draw.line(window, node_color, node_position, angle_point)

if __name__ == "__main__":
    num_obstacles = 4
    for _ in range(num_obstacles):
        obstacle()
    path = pathing.a_star(NEWT_START,
                          NEWT_GOAL,
                          newt_adjacent,
                          newt_heuristic,
                          newt_success)
    window = pygame.display.set_mode((90 * DRAW_SCALE, 90 * DRAW_SCALE))
    save = True
    while True:
        screen = 0
        for node in path:
            window.fill((0, 0, 0))
            draw_node(window, node)
            time.sleep(0.02)
            pygame.display.flip()
            if(save):
                pygame.image.save(window, str(screen).zfill(4) + "screen.jpg")
            screen += 1
        save = False
          
    
    
