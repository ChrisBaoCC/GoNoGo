import random
from psychopy import event, core
from psychopy.visual import Window, TextBox2
from psychopy.visual.rect import Rect
from psychopy.event import Mouse
from psychopy.core import Clock

# CONSTANTS #
WIDTH = 1920
HEIGHT = 1080

# GLOBALS #
window = Window((WIDTH, HEIGHT), color="white", fullscr=True, units="pix")
file = open("data.csv", "w")
# TODO: file-writing stuff

# FUNCTIONS #


# MAINLOOP #
while True:
    keys = event.getKeys()

    if "escape" in keys:
        file.close()
        core.quit()

    window.update()
