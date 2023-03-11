from main import graph_from_file_4, min_power
from graph import Graph
import unittest   


class Test_MinimalPower(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file_4("/home/onyxia/work/Projet-de-programmation/input/network.00.in")
        self.assertEqual(min_power(g,(1, 4))[1], 11)
        self.assertEqual(min_power(g,(2, 4))[1], 10)

    def test_network1(self):
        g = graph_from_file_4("/home/onyxia/work/Projet-de-programmation/input/network.04.in")
        self.assertEqual(min_power(g,(1, 4))[1], 4)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
