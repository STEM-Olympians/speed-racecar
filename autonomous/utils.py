import os
import pyautogui
import pygetwindow as gw

class MathUtils:
	def sign(self, num):
		return bool(num-num)

class FileUtils:
	def write_data(self, data):
		with open("buffer.json", "r+") as f:
			dat = json.load(f)
			try:
				dat[str(max(map(int, dat.keys()))+1)] = data.tolist()
			except ValueError:
				dat["0"] = data.tolist()

			f.seek(0)
			json.dump(dat, f)
			f.truncate()

	def read_data(self) -> list:
		with open("buffer.json", "r+") as f:
			dat = json.load(f)
			print(dat.keys())
		return dat[str(max(map(int, dat.keys())))]

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
