# import tkinter
import time
import math
import keyboard
import ctypes
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import osu_parser

screen_x = ctypes.windll.user32.GetSystemMetrics(0)
screen_y = ctypes.windll.user32.GetSystemMetrics(1)
screen_dif = (0.6 / 19) * screen_y

def spin(duration):
    angle = 0
    end = time.time() + duration / 1000

    while end > time.time():
        x = int(math.cos(angle) * (screen_x * 0.025) + (screen_x / 2))
        y = int(math.sin(angle) * (screen_x * 0.025) + (screen_y + screen_dif) / 2)
    
        ctypes.windll.user32.SetCursorPos(x, y)
        angle += 1

def main():
    Tk().withdraw()
    DT, HT = True, False
    LOADED = False

    while True:
        if keyboard.is_pressed("l"):
            beatmap = askopenfilename(filetypes=[("Osu files", "*.osu")])

            try:
                f = open(file=beatmap, mode="r", encoding="utf8")
            except FileNotFoundError:
                print("Error.")
                continue

            SL = osu_parser.parse_SL(f)
            SM = osu_parser.parse_SM(f)
            TPs = osu_parser.parse_TPs(f, DT, HT)
            HOs = osu_parser.parse_HOs(f, DT, HT)
            LOADED = True

            print("Loaded successfully")

        elif keyboard.is_pressed("s") and LOADED:
            tracker = 0
            start = time.time()

            while len(HOs) > tracker:
                if (time.time() - start) * 1000 >= HOs[tracker].offset - HOs[0].offset:
                    if HOs[tracker].obj == 3:
                        spin(HOs[tracker].end_offset - HOs[tracker].offset)
                    else:
                        ctypes.windll.user32.SetCursorPos(HOs[tracker].x, HOs[tracker].y)
                    tracker += 1

if __name__ == "__main__":
    main()
