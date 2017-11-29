"""
Tools used to test our graphs in both negative and non-negative edge graphs.
Author: Qi Ying Lim
"""

from sys import maxsize
from random import choice

INF = maxsize


class TestTools:
    @staticmethod
    def brute_force_result(g, node):
        """
        computes the shortest distance, and the shortest path from graph at index to specified node using brute force
        """
        if node not in g.get_nodes():
            return "node " + str(node) + " does not exist."
        else:
            paths = TestTools.find_paths(g, g.get_root(), node)
            if len(paths) == 0:
                return 0, INF
            costs = []
            for path in paths:
                cost = sum([g.get_edge_cost(path[i], path[i + 1]) for i in range(len(path) - 1)])
                costs.append(cost)
            z = list(zip(paths, costs))
            shortest = min(z, key=lambda x: x[1])
            return shortest

    @staticmethod
    def find_paths(g, start_node, end_node, path=None):
        """
        Code algorithm taken from https://stackoverflow.com/questions/2606018/path-between-two-nodes
        Recursive algorithm to find all the paths from the start and end nodes
        """
        if path is None:
            path = []
        path = path + [start_node]
        if start_node == end_node:
            return [path]

        paths = []
        for node in g.get_out_neighbours(start_node):
            if node not in path:
                new_paths = TestTools.find_paths(g, node, end_node, path)
                paths.extend(new_paths)
        return paths
