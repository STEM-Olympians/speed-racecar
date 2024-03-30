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
	def click(self, game_window_name, x_percent, y_percent):
		window = gw.getWindowsWithTitle(game_window_name)[0]
		print("get window with title")

		window.activate()
		print("activated window")

		wleft, wtop, wwidth, wheight = window.left, window.top, window.width, window.height
		print("got dimensions")

		x = wleft + int(wheight*x_percent)
		y = wtop  + int(wtop*y_percent)
		print("multiplying data or something")

		pyautogui.click(x, y)
		print("clicked point on screen")

	def enter(self):
		window = gw.getWindowsWithTitle(game_window_name)[0]
		print("get window with title")

		window.activate()
		print("activated window")

		pyautogui.press("enter")
		print("enter pressed")
