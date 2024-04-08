import ml
import utils
import time

gutils = utils.GUIUtils("RacecarSim")
while True:
	gutils.start()
	time.sleep(0.2)
	gutils.enter()
	time.sleep(0.2)
	gutils.end()
