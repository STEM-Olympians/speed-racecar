import utils
import ml

def Handler():
	rc = ml.RacecarTrain()
	rc.car.set_start_update(rc.start, rc.update, rc.update_slow)
	rc.car.go()

Handler()
