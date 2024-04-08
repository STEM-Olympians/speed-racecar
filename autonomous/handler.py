import utils
import ml

rc = ml.RacecarTrain()
rc.car.set_start_update(rc.start, rc.update, rc.update_slow)
rc.car.go()
