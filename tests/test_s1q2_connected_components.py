from graph import Graph, graph_from_file
from main import connected_components_set
import unittest   # The test framework

###### QUESTION 1


class Test_GraphCC(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("/home/onyxia/work/Projet-de-programmation/input/network.00.in")
        cc = connected_components_set(g)
        self.assertEqual(cc, [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}])

    def test_network1(self):
        g = graph_from_file("/home/onyxia/work/Projet-de-programmation/input/network.01.in")
        dd = connected_components_set(g)
        self.assertEqual(dd, [{1, 2, 3}, {4, 5, 6, 7}])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)