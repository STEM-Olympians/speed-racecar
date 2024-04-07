import os
import json

import time
import threading
import pyautogui
import pygetwindow as gw
from AppKit import NSWorkspace

class MathUtils:
	def sign(self, num):
		return bool(num-num)

class FileUtils:
	def __init__(self, filename):
		self.filename = filename

	def write_data(self, key, data):
		with open(self.filename, "r+") as f:
			dat = json.load(f)
			dat[key] = data
			f.seek(0)
			json.dump(dat, f, indent=4)

		return

	def read_data(self, key) -> list:
		with open(self.filename, "r+") as f:
			dat = json.load(f)
			return dat[key]

class GUIUtils:
    def __init__(self, game_window_name):
        self.game_window_name = game_window_name

    def _click(self, x, y):
        while True:
            if NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'] == "RacecarSim":
                time.sleep(0.5)
                pyautogui.click(x, y)
                break

    def _press(self, keyname):
        while True:
            if NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'] == "RacecarSim":
                time.sleep(0.5)
                pyautogui.press(keyname)
                break

    def enter(self):
        l = lambda: os.system("/bin/zsh -c \"source ~/.zshrc; cd ~/Desktop/speed/racecar/autonomous; racecar sim handler.py\"")
        t = threading.Thread(target=l, args=()).start()
        time.sleep(0.5)
        self._press("enter")


	# x343 y480 <- start button
    def start(self):
        startButtonX  = 343
        startButtonY  = 480
        self._click(startButtonX, startButtonY)

    def end(self):
        self._press("esc")
