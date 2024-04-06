import os
import json
import pyautogui
import pygetwindow as gw

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
		window = gw.getWindowsWithTitle(self.game_window_name)[0]
		print("get window with title")

		window.activate()
		print("activated window")

		pyautogui.click(x, y)
		print("clicked point on screen")

	def enter(self):
		window = gw.getWindowsWithTitle(self.game_window_name)[0]

		window.activate()

		pyautogui.press("enter")

	# x343 y480 <- start button
	def start(self):
		window = gw.getwindowWithTitle(self.game_window_name)[0]

		window.activate()

		self._click(343, 480)

	def end(self):
		window = gw.getWindowWithTitle(self.game_window_name)[0]

		window.activate()

		pyautogui.press("escape")
