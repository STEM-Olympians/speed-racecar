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

if __name__ == "__main__":
	unittest.main()

