"""Game runner"""

import subprocess
import os

import pygame

import newt
import pathing
import draw
import obstacle

# nodes
START = newt.Node(0, 0, 0, 0, 1)
GOAL = newt.Node(160, 160, 0, 0, 0)

def get_path(obstacles, bounds):
    """return nodes in path from A*"""
    heuristic = lambda n, g: newt.heuristic(n, g, obstacles, bounds)
    return pathing.a_star(START, GOAL, newt.adjacent, heuristic, newt.success)

def clear_images():
    """delete all PNGs from program directory"""
    filelist = [f for f in os.listdir(".") if f.endswith(".png")]
    for filename in filelist:
        os.remove(filename)

def save_image(window, i):
    """save screenshot to disk"""
    pygame.image.save(window, str(i).zfill(4) + "screen.png")

def make_gif():
    """generate a gif from the accumulated screenshots"""
    label = str(int(time.time()))
    print("label: " + label)
    gif_command = "bash make_gif.sh maneuver" + label + ".gif"
    subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)

def main():
    """generate path and render"""
    obstacles = obstacle.get_obstacles(START.x, START.y, GOAL.x, GOAL.y)
    bounds = (GOAL.x + 10, GOAL.y + 10)
    window = draw.init(obstacles, GOAL)
    pygame.display.flip()
    path = get_path(obstacles, bounds)
    draw.path(window, obstacles, GOAL, path)

if __name__ == "__main__":
    while True:
        main()
