# turtle placeholders from https://www.flaticon.com/free-icons/turtle"
# images by Ehtisham Abid

import random
from psychopy import event, core
from psychopy.visual import Window, TextBox2, ImageStim
from psychopy.visual.rect import Rect
from psychopy.event import Mouse
from psychopy.core import CountdownTimer

# CONSTANTS #
# State
STATE_INTRO = 0
STATE_GO = 1  # display "go"
STATE_NOGO = 2  # display "no go"
STATE_ISI = 3  # interstimulus interval
STATE_END = 4

# Interface
WIDTH = 1920
HEIGHT = 1080
TEXT_ARGS = {
    "units": "pix",
    "color": "black",
    "autoDraw": True,
    "alignment": "center",
    "size": [None, None]
}

INTRO_FONTSIZE = 30
TEXT1_POS = (0, 300)
TEXT1_CONTENT = "In the following trials, only press [space]"\
                + " if you see this message:"
TEXT2_POS = (0, 0)
TEXT2_CONTENT = "Do nothing (no go) if you see the following message:"
TEXT3_POS = (0, -300)
TEXT3_CONTENT = "When you're ready, press [space] to start!"

IMG_SIZE = (150, 150)
IMG1_POS = (0, 150)
IMG2_POS = (0, -150)

ISI = 1  # inter-stimulus interval, seconds

# GLOBALS #
window = Window((WIDTH, HEIGHT), color="white", fullscr=True, units="pix")
file = open("data.csv", "w")
# TODO: file-writing stuff
state = STATE_INTRO
isi_timer = None

# FUNCTIONS #


# MAINLOOP #
while True:
    keys = event.getKeys()

    if "escape" in keys:
        file.close()
        core.quit()

    if state == STATE_INTRO:
        text1 = TextBox2(win=window, pos=TEXT1_POS, text=TEXT1_CONTENT,
                         letterHeight=INTRO_FONTSIZE, **TEXT_ARGS)
        img1 = ImageStim(win=window, image="go.png", size=IMG_SIZE,
                         pos=IMG1_POS)
        img1.draw()
        text2 = TextBox2(win=window, pos=TEXT2_POS, text=TEXT2_CONTENT,
                         letterHeight=INTRO_FONTSIZE, **TEXT_ARGS)
        img2 = ImageStim(win=window, image="nogo.png", size=IMG_SIZE,
                         pos=IMG2_POS)
        img2.draw()
        text3 = TextBox2(win=window, pos=TEXT3_POS, text=TEXT3_CONTENT,
                         letterHeight=INTRO_FONTSIZE, **TEXT_ARGS)
        if "space" in keys:
            state = STATE_ISI
            isi_timer = CountdownTimer(ISI)
            text1.setText("something else")
            # TODO: fix text boxes still displaying old text
            del img1
            del img2

    window.flip()
