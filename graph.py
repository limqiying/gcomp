"""
Creates graph object
"""

from collections import defaultdict
from sys import maxsize
import heapq

INF = maxsize  # infinity


class Graph:
    """
    creates a directed object, whose information is stored in the form of a dictionary, whose key is the vertex,
    and values are the list of neighbouring vertices. For example, if we have G where
        1 -> 2
        2 -> 3
        3 -> 1
        3 -> 2
    then our graph is stored in the dictionary:
        {1: [2], 2: [3], 3: [1,2]}
    """

    def __init__(self):
        self._graph = defaultdict(set)
        self._cost = defaultdict()

    def get_nodes(self):
        return list(self._graph.keys())

    def set_nodes(self, nodes):
        """
        adds a list of Nodes specified by the input list nodes
        """
        for n in nodes:
            self._graph[n] = set()

    def set_edges(self, edge_list):
        """
        Edges are input as a list of tuples, (v,w,c) where v,w are Nodes and c is the cost of the edge
        """
        for (v, w, c) in edge_list:
            if v in self._graph.get_nodes() and w in self._graph.get_nodes():
                self._graph[v].add(w)
                self._cost[(v, w)] = c
            else:
                raise KeyError('No such node ' + str(v) + " or " + str(w) + " in graph")

    def get_out_neighbours(self, node):
        """
        :param node: the Node in the graph
        :return: a list of the outgoing neighbours from the node
        """
        if node in self.get_nodes():
            return self._graph[node]
        else:
            raise KeyError("No such node (" + str(node) + ") in graph")

    def __repr__(self):
        return str(dict(self._graph))

# class ShortestPathGraph(Graph):
#
#     def __init__(self, root):
#         super(Graph, self).__init__()
#         self._d_dist = [INF]*len(self.get_nodes())    # stores distances from root as returned by the dijkstra algorithm
#         self._bf_dist = [INF]*len(self.get_nodes())   # stores distances from root as returned by the bellman-ford algorithm
#
#     @staticmethod
#     def siftdown(heap, startpos, pos):
#         """
#         This method is taken from the built-in function for heapq, to decrease the key value
#         :param heap: a heapq object
#         :param startpos:
#         :param pos:
#         """
#         newitem = heap[pos]
#         # Follow the path to the root, moving parents down until finding a place
#         # newitem fits.
#         while pos > startpos:
#             parentpos = (pos - 1) >> 1
#             parent = heap[parentpos]
#             if newitem < parent:
#                 heap[pos] = parent
#                 pos = parentpos
#                 continue
#             break
#         heap[pos] = newitem
#
#     def dijkstra(self, root):
#         d = [(INF, node) if node != root else (0, node) for node in self.get_nodes()]
#         heapq.heapify(d)
#         self._d_dist[root] = 0
#
#
#         set_X = set()
#         for i in range(len(self.get_nodes())):
#             (d_v, v) = heapq.heappop(d)
#             set_X.add(v)
#             for neighbour in self.get_out_neighbours(v):
#                 if (v.get_dist() + v.get_weight(neighbour)) < neighbour.get_dist():
#
