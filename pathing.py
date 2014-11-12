"""generalized pathing functions"""

import heapq

def a_star(start, goal, adjacent, heuristic, success):
    """A* pathing algorithm"""
    open_set = set()
    open_heap = []
    closed_set = set()
    came_from = {}
    open_set.add(start)
    open_heap.append((0, start))
    g_score = {}
    f_score = {}
    g_score[start] = 0
    f_score[start] = g_score[start] + heuristic(start, goal)
    while open_set:
        node = heapq.heappop(open_heap)[1]
        if success(node, goal):
            print(len(open_set))
            return _reconstruct_path(came_from, node)
        open_set.remove(node)
        closed_set.add(node)
        for adj in adjacent(node):
            if adj in closed_set:
                continue
            adj_distance = 1 # adjacency is based on a constant time step
            tentative_g_score = g_score[node] + adj_distance
            if adj not in open_set or tentative_g_score < g_score[adj]:
                came_from[adj] = node
                g_score[adj] = tentative_g_score
                f_score[adj] = g_score[adj] + heuristic(adj, goal)
                open_set.add(adj)
                heapq.heappush(open_heap, (f_score[adj], adj))
    return []

def _reconstruct_path(came_from, node):
    """trace back the path built by A*"""
    if node in came_from:
        path = _reconstruct_path(came_from, came_from[node])
        return path + [node]
    else:
        return [node]
