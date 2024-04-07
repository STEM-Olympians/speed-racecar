import ml

rc = ml.RacecarRun()
rc.car.set_start_update(rc.start, rc.update, rc.update_slow)
rc.car.go()
