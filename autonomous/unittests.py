import unittest
import numpy as np
import ml

class Tests(unittest.TestCase):
	def test_evolution(self):
		evolution = ml.Evolution()
		fitness_value = evolution.fitness(True, 8)
		self.assertEqual(fitness_value, (int(True)*10)+8)

	def test_mutation(self):
		evolution = ml.Evolution()

		child_node = np.array([1, 0.4, -1, 0.3])
		print(evolution.mutate_child(child_node))



if __name__ == "__main__":
	unittest.main()
