"""Unit tests for pathing module"""

import pathing
import unittest
import math
import time

class TestPathing(unittest.TestCase):
    """Test suite for pathing module"""
    # pylint: disable=R0904

    def setUp(self):
        self.start = (0, 0)
        self.goal = (4, 4)
        def manhattan(node):
            """returns a list of adjacent nodes in mahattan distance"""
            adjacency_list = []
            adjacency_list.append(((node[0] + 1, node[1]), None))
            adjacency_list.append(((node[0] - 1, node[1]), None))
            adjacency_list.append(((node[0], node[1] + 1), None))
            adjacency_list.append(((node[0], node[1] - 1), None))
            return adjacency_list
        self.adjacent = manhattan
        def euclidean_distance(node, goal):
            """returns crows-flight distance between node and goal"""
            return math.sqrt((goal[0]-node[0])**2 + (goal[1]-node[1])**2)
        self.heuristic = euclidean_distance
        self.success = lambda node, goal: node == goal

    def test_a_star(self):
        """test that path is optimal and obeys heuristic"""
        start = time.time()
        path = pathing.a_star(self.start,
                              self.goal,
                              self.adjacent,
                              self.heuristic,
                              self.success)
        stop = time.time()
        elapsed_ms = (stop - start) * 1000
        self.assertEqual(len(path), 9)
        self.assertIn(((2, 2), None), path)
        print("Path found. Time elapsed: %f milliseconds.", elapsed_ms)

if __name__ == '__main__':
    unittest.main()
