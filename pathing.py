"""generalized pathing functions"""

import heapq
import time

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
    seen.add(_node_to_tuple(start))
    while True:
        node = heapq.heappop(open_heap)[1]
        if len(open_heap) > 800000:
            print((node.x, node.y, node.v_x, node.v_y, node.angle))
            print(g_score[node])
            print(heuristic(node, goal))
            return [node]
        if success(node, goal):
            print(len(open_heap))
            return _reconstruct_path(came_from, node)
        for adj in adjacent(node):
            if _node_to_tuple(adj) in seen:
                continue
            seen.add(_node_to_tuple(adj))
            came_from[adj] = node
            # adjacency is based on a constant time step
            g_score[adj] = g_score[node] + 1
            h = heuristic(adj, goal)
            f_score[adj] = g_score[adj] + h
            heapq.heappush(open_heap, (f_score[adj], adj))

def _reconstruct_path(came_from, node):
    """trace back the path built by A*"""
    if node in came_from:
        path = _reconstruct_path(came_from, came_from[node])
        return path + [node]
    else:
        return [node]

def _node_to_tuple(node):
    return (node.x, node.y, node.v_x, node.v_y, node.angle)
