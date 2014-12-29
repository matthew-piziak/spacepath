"""Rendering functions"""

import os
import time
import subprocess

import pygame

def save_image(window, i):
    """save screenshot to disk"""
    pygame.image.save(window, str(i).zfill(4) + "screen.png")

def make_gif():
    """generate a gif from the accumulated screenshots"""
    label = str(int(time.time()))
    print("label: " + label)
    gif_command = "bash make_gif.sh maneuver" + label + ".gif"
    gif_process = subprocess.Popen(gif_command.split(), stdout=subprocess.PIPE)
    gif_process.wait()
    _clear_images()

def _clear_images():
    """delete all PNGs from program directory"""
    filelist = [f for f in os.listdir(".") if f.endswith("screen.png")]
    for filename in filelist:
        os.remove(filename)
