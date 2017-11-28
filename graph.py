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
    """ 
    Done by Tia
    """

    def __init__(self):
        self._graph = defaultdict(set)
        self._cost = defaultdict(lambda: INF)

    def get_nodes(self):
        return set(self._graph.keys())

    def set_nodes(self, nodes):
        """
        adds a list of Nodes specified by the input list nodes
        """
        for n in nodes:
            if n not in self.get_nodes():
                self._graph[n] = set()

    def set_edges(self, edge_list):
        """
        Edges are input as a list of tuples, (v,w,c) where v,w are Nodes and c is the cost of the edge
        """
        for (v, w, c) in edge_list:
            if v in self.get_nodes() and w in self.get_nodes():
                self._graph[v].add(w)
                # uses the edge with the smaller weight, if there are parallel edges
                self._cost[(v, w)] = min(c, self._cost[(v, w)])
            else:
                raise KeyError('No such node ' + str(v) + " or " + str(w) + " in graph")
    
    def get_edge_cost(self, u, v):
        return self._cost[(v, w)]

    def get_out_neighbours(self, node, k= 0):
        """
        :param node: the Node in the graph
        :return: a list of the outgoing neighbours from the node
        """
        if k == 0:
            if node in self.get_nodes():
                return self._graph[node]
            else:
                raise KeyError("No such node (" + str(node) + ") in graph")
        else:
            return



    def __repr__(self):
        return str(dict(self._graph))


class ShortestPathGraph(Graph):
    def __init__(self, root):
        Graph.__init__(self)
        self._root = root
        self.set_nodes([root])
        self._dijkstra_computed = False     # prevents unnecessary re-computation of distances
        self._bellman_ford_computed = False
        # stores distances from root as returned by the dijkstra algorithm
        self._d_dist = defaultdict(lambda: INF)
        # stores distances from root as returned by the bellman-ford algorithm
        self._bf_dist = defaultdict(lambda: INF)
        # stores the parent nodes of each node in the shortest path Dijkstra tree
        self._d_prev = defaultdict()
        self._d_prev[root] = None
        # stores the parent nodes of each node in the shortest path BF tree
        self._bf_prev = defaultdict()
        self._bf_prev[root] = None

    def _dijkstra(self):
        """
        An implementation of the Dijkstra's Algorithm, as taken from the pseudocode from class notes.
        Since python's heapq does not have an easily-accessible decreaseKey() function, we worked around this by
        maintaining the self._d_dist array to hold the 'correct', up-to-date distance. When we extract the minimum key
        from the heap, we first verify if this item represents the correct distance as in Line 93, before continuing as
        the pseudo-code describes.
        """
        self._dijkstra_computed = True
        # making the priority queue
        d = [(INF, node) if node != self._root else (0, node) for node in self.get_nodes()]
        self._d_dist[self._root] = 0  # setting the distance of the root to self as 0
        # loop through all the vertices
        for i in range(len(self.get_nodes())):
            (d_v, v) = heapq.heappop(d)  # extract the vertex with the minimum distance to the root
            if d_v == self._d_dist[v]:  # verifies that the popped item correctly contains the minimum distance
                for neighbour in self.get_out_neighbours(v):
                    new_distance = self._d_dist[v] + self._cost[(v, neighbour)]
                    if new_distance < self._d_dist[neighbour]:
                        self._d_dist[neighbour] = new_distance
                        # this line "decreases key" of the neighbour by pushing in a tuple containing the neighbour and
                        # the shorter distance value
                        heapq.heappush(d, (new_distance, neighbour))
                        self._d_prev[neighbour] = v

    def dijkstra_get_dist(self, node, numerical=False):
        """
        returns the value dist(root, node)
        """
        if not self._dijkstra_computed:
            print("Running Dijkstra Algorithm")
            self._dijkstra()
        if self._d_dist[node] == INF:
            return "There is no path from " + str(self._root) + " to " + str(node) + "."
        elif numerical:
            return self._d_dist[node]
        else:
            return "Distance from " + str(self._root) + " to " + str(i) + " is " + str(self._d_dist[node])

    def dijkstra_get_path(self, node):
        """
        returns the shortest path from node to root
        """
        if not self._dijkstra_computed:
            print("Running Dijkstra Algorithm")
            self._dijkstra()
        if self._d_dist[node] == INF:
            return "There is no path from " + str(self._root) + " to " + str(node) + "."
        else:
            v = node
            path = [node]
            while self._d_prev[v] is not None:
                path.append(self._d_prev[v])
                v = self._d_prev[v]
            path.reverse()
            return path

    def dijkstra_get_tree(self):
        if not self._dijkstra_computed:
            print("Running Dijkstra Algorithm")
            self._dijkstra()
        return list(map(lambda x: (x[1], x[0]), self._d_prev.items()))


    def _bellmanford(self):

        """
        This is the implementation of bellman_ford algorithm we learned during the class. 
        """
        n = len(self.get_nodes())
        self._bellmanford_computed = True
        d = [n][n]
        for i in range(n):
            if i != self._root:
                d[i][0] = INF
        d[self._root][0] = 0

        for k in range(1,n):
            for i in range(n):
                d[i][k] = d[i][k-1]
                for u in self.get_out_neighbours(i):
                    d[i][k] = min(d[i][k], d[u][k-1] +  self._cost[(u,i)])

        #(One more iteration to check the negative cycle)
        for i in range(n):
            for u in self.get_out_neighbours(i):
                if (d[i][n-1] > d[u][n-1] +  self._cost[(u,i)]):
                    print "Negative Cycle"
                    return 0

        # Assign final distance to each node
        for node in self.get_nodes:
            self._bf_dist[node] = d[node][n-1]
        return 1

    def bellmanford_get_dist(self, node):
        if not self._bellmanford_computed:
            if self._bellmanford() == 0:
                return -INF

        if self._d_dist[node] == INF:
            return "There is no path from " + str(self._root) + " to " + str(node) + "."
        else:
            print self._bf_dist[node] 
            return self._bf_dist[node] 




graph = ShortestPathGraph(0)
graph.set_nodes(range(10))
graph.set_edges([(0, 2, 1), (0, 3, 3), (2, 4, 6), (3, 1, 7), (1, 5, 3), (1, 9, 5), (2, 5, 3), (2, 4, 1), (3, 4, 1)])
<<<<<<< HEAD
print graph.dijkstra_get_dist(3)



=======
print(graph.dijkstra_get_tree())
>>>>>>> origin/master
