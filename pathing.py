"""generalized pathing functions"""

import heapq

def a_star(start, goal, adjacent, heuristic, success):
    """A* pathing algorithm"""
    open_heap = []
    seen = set()
    came_from = {}
    g_score = {}
    f_score = {}
    g_score[start] = 0
    f_score[start] = g_score[start] + heuristic(start, goal)
    open_heap.append((f_score[start], start))
    seen.add(start)
    while True:
        node = heapq.heappop(open_heap)[1]
        if success(node, goal):
            print("heap: " + str(len(open_heap)))
            return _reconstruct_path(came_from, node)
        for adj, action in adjacent(node):
            if adj in seen:
                continue
            seen.add(adj)
            came_from[adj] = (node, action)
            # adjacency is based on a constant time step
            g_score[adj] = g_score[node] + 1
            h_score = heuristic(adj, goal)
            f_score[adj] = g_score[adj] + h_score
            heapq.heappush(open_heap, (f_score[adj], adj))

def _reconstruct_path(came_from, node):
    """trace back the path built by A*"""
    if node in came_from:
        path = _reconstruct_path(came_from, came_from[node][0])
        return path + [(node, came_from[node][1])]
    else:
        return [node]
