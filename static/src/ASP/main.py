import sys

# ChatGpt Generated the following code for min heap
# I use the following promote: " implement a min heap in python; add a dict name "position" to map the data items to their indices;
# add a changePriority() function to allow a user change an item's priority; add a swap function,
# in side the swap function, maintenance the position mapping."

# Note the tuple (priority, data) is used to store the data in the heap.
# And in the position dict, the key is the data, and the value is the index of the data in the heap.


class MinHeap:
    def __init__(self):
        self.heap = []
        self.position = {}

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i][1]] = i
        self.position[self.heap[j][1]] = j

    def insert(self, item):
        self.heap.append(item)
        n = len(self.heap)
        self.position[item[1]] = n - 1
        self.sift_up(n - 1)

    def sift_up(self, i):
        while i > 0 and self.heap[i][0] < self.heap[self.parent(i)][0]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def extract_min(self):
        min_item = self.heap[0]
        del self.position[min_item[1]]
        last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = last_item
            self.position[last_item[1]] = 0
            self.sift_down(0)
        return min_item

    def sift_down(self, i):
        n = len(self.heap)
        min_idx = i
        l = self.left_child(i)
        if l < n and self.heap[l][0] < self.heap[min_idx][0]:
            min_idx = l
        r = self.right_child(i)
        if r < n and self.heap[r][0] < self.heap[min_idx][0]:
            min_idx = r
        if i != min_idx:
            self.swap(i, min_idx)
            self.sift_down(min_idx)

    def changePriority(self, item, new_priority):
        if item in self.position:
            i = self.position[item]
            old_priority = self.heap[i][0]
            self.heap[i] = (new_priority, item)
            if new_priority < old_priority:
                self.sift_up(i)
            else:
                self.sift_down(i)

    def isempty(self):
        return len(self.heap) == 0


def dijkstra(graph, start):
    n = len(graph)
    dist = [float('inf')] * n  # set all distances to infinity
    dist[start] = 0  # set the distance to the start node to 0
    heap = MinHeap()  # initialize heap
    # initialize heap with starting node and its distance
    heap.insert((0, start))
    prev = [[] for _ in range(n)]  # initialize predecessor list for all nodes
    while heap.isempty() == False:
        # get node with smallest distance from heap
        (distance, node) = heap.extract_min()
        if distance > dist[node]:  # if node is already processed, skip it
            continue
        for neighbor, weight in graph[node]:  # visit neighbors of the node
            new_distance = dist[node] + weight
            # if new distance to neighbor is shorter, update it
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                # set the node as the only predecessor of the neighbor
                prev[neighbor] = [node]
                # add neighbor and its distance to heap
                heap.insert((new_distance, neighbor))
            # if there's a tie in distance, add the node as a predecessor
            elif new_distance == dist[neighbor]:
                prev[neighbor].append(node)

    # break early if we reached the destination
        if node == dest:  # if we reached the destination, stop
            break
    return dist, prev


# delete all edges that are part of the shortest path
from collections import deque


def delete(graph, prev, s, t):
    # Initialize visited and queue for BFS
    visited = set()
    queue = deque([t])
    visited.add(t)

    # Traverse the previous node list with BFS
    while queue:
        u = queue.popleft()
        if u == s:
            break
        for v in prev[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
            # Remove the edge (u, v) from the graph
            graph[v] = [(w, weight) for w, weight in graph[v] if w != u]

    return graph


def read_graph():
    n, m = map(int, input().split())  # read n and m from first line
    if n == 0 and m == 0:  # end of input
        return None
    # read start and dest from second line
    start, dest = map(int, input().split())
    graph = [[] for _ in range(n)]  # initialize graph with n nodes
    for _ in range(m):
        a, b, w = map(int, input().split())  # read edge from input
        graph[a].append((b, w))  # add edge to graph
    return start, dest, graph


# main loop
while True:
    data = read_graph()
    if data is None:
        break
    start, dest, graph = data
    # do something with start, dest, and graph
    # print(graph)
    dist, prev = dijkstra(graph, start)
    # print(prev)
    delete(graph, prev, start, dest)
    # print(graph)
    # run dijkstra on the modified graph.
    # we don't care about the predecessor list this round.
    dist, _ = dijkstra(graph, start)
    if dist[dest] == float('inf'):
        print(-1)  # no path
    else:
        print(dist[dest])
