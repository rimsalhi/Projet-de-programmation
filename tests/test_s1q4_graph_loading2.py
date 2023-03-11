import unittest 
from graph import Graph
from main import graph_from_file_4

###### QUESTION 4
class Test_GraphLoading(unittest.TestCase):
    def test_network4(self):
        g = graph_from_file_4("/home/onyxia/work/Projet-de-programmation/input/network.04.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        self.assertEqual(g.graph[1][0][2], 6)
        self.assertEqual(g.graph[4][1][1], 11)
        self.assertEqual(g.graph[2][1][0], 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)