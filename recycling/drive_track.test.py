import unittest
import drive_track

class TestMathUtils(unittest.TestCase):
	def test_modified_log(self):
		try:
			mutils = drive_track.MathUtils()
			mutils.modified_log(-1)
			mutils.modified_log(0)
			mutils.modified_log(1)
			print("passed")
		except ValueError():
			print("failed")

	@unittest.skip()
	def test_rad_log(self):
		rcd = drive_track.RacecarDrive()
		print(rcd.rad_log_growth(0, 10))

		print(rcd.rad_log_decay(0, 10))

if __name__ == "__main__":
	unittest.main()

