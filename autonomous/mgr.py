import utils
import os

if __name__ == "__main__":
	racecar_app_path = "~/Desktop/speed/RacecarSim_Mac_v1.1.3.7.app"
	guiutils = utils.GUIUtils()
	os.system(f"open {racecar_app_path}")
	os.system("python3 ml.py")
	guiutils.click("RacecarGame", 50, 50)
	guiutils.enter()
