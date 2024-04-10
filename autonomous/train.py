import ml
import utils
import time

gutils = utils.GUIUtils("RacecarSim")
while True:
	gutils.start()
	time.sleep(1)
	gutils.enter()
	time.sleep(1)
	gutils.end()
	time.sleep(1)
