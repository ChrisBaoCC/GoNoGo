# turtle placeholders from https://www.flaticon.com/free-icons/turtle"
# images by Ehtisham Abid

from random import shuffle
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
STATE_FEEDBACK = 3
STATE_ISI = 4  # interstimulus interval
STATE_END = 5

# Interface
WIDTH = 1920
HEIGHT = 1080
TEXT_ARGS = {
    "units": "pix",
    "color": "black",
    "alignment": "center",
    "letterHeight": 30,
    "size": [None, None]
}

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

TEXT_END_CONTENT = "Thank you for participating! Press [esc] to exit."

ISI = 0.5  # inter-stimulus interval, seconds
FB_DURATION = 1
RXN_DURATION = 2

FB_LATE = "[space] was not pressed in time"
FB_WRONG = "[space] was pressed incorrectly"

# GLOBALS #
window = Window((WIDTH, HEIGHT), color="white", fullscr=True, units="pix")
file = open("data.csv", "w")
file.write("condition,rt,correct\n")
state = STATE_INTRO
feedback_timer = None
isi_timer = None
reaction_timer = None

feedback = ""

trial = 0  # number of the trial we're on (index)
trials = [True, True, False]  # * 3
shuffle(trials)

text1 = TextBox2(win=window, pos=TEXT1_POS, text=TEXT1_CONTENT,
                 **TEXT_ARGS)
text2 = TextBox2(win=window, pos=TEXT2_POS, text=TEXT2_CONTENT,
                 **TEXT_ARGS)
text3 = TextBox2(win=window, pos=TEXT3_POS, text=TEXT3_CONTENT,
                 **TEXT_ARGS)
img1 = ImageStim(win=window, image="go.png", size=IMG_SIZE,
                 pos=IMG1_POS)
img2 = ImageStim(win=window, image="nogo.png", size=IMG_SIZE,
                 pos=IMG2_POS)
end_text = TextBox2(win=window, pos=(0, 0), text=TEXT_END_CONTENT,
                    **TEXT_ARGS)

# FUNCTIONS #
# return the reaction time (reads clock value)


def formatTime():
    return str(2-reaction_timer.getTime())[:5]


# MAINLOOP #
while True:
    keys = event.getKeys()

    if "escape" in keys:
        file.close()
        core.quit()

    if state == STATE_GO:
        img1.draw()
        if "space" in keys:
            file.write("go,"+formatTime()+",1\n")
            state = STATE_ISI
            isi_timer = CountdownTimer(FB_DURATION)
            continue
        if reaction_timer.getTime() < 0:
            file.write("go,2,0\n")
            feedback = FB_LATE
            state = STATE_FEEDBACK
            feedback_timer = CountdownTimer(FB_DURATION)
            continue

    if state == STATE_NOGO:
        img2.draw()
        if "space" in keys:
            file.write("nogo,"+formatTime()+",0\n")
            feedback = FB_WRONG
            state = STATE_FEEDBACK
            feedback_timer = CountdownTimer(FB_DURATION)
            continue
        if reaction_timer.getTime() < 0:
            file.write("nogo,2,1\n")
            state = STATE_ISI
            isi_timer = CountdownTimer(FB_DURATION)
            continue

    if state == STATE_FEEDBACK:
        if feedback_timer.getTime() < 0:
            state = STATE_ISI
            isi_timer = CountdownTimer(ISI)
            continue
        fb_text = TextBox2(win=window, pos=(0, 0), text=feedback,
                           **TEXT_ARGS)
        fb_text.draw()

    if state == STATE_ISI and isi_timer.getTime() < 0:
        isi_timer = None
        if trial == len(trials):
            state = STATE_END
            continue
        state = STATE_GO if trials[trial] else STATE_NOGO
        trial += 1
        reaction_timer = CountdownTimer(RXN_DURATION)
        continue

    if state == STATE_END:
        end_text.draw()

    if state == STATE_INTRO:
        text1.draw()
        img1.draw()
        text2.draw()
        img2.draw()
        text3.draw()
        if "space" in keys:
            img1.pos = img2.pos = (0, 0)
            state = STATE_ISI
            isi_timer = CountdownTimer(ISI)

    window.flip()
