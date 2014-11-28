"""Rendering functions"""

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
