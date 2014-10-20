from collections import namedtuple
import heapq
import math

Node = namedtuple('Node', 'x y dx dy')

def aStar(start, end):
    openSet = set()
    openHeap = []
    closedSet = set()
    parentOf = {}
    length = 10
    height = 10
    goalPositionThreshold = 20;
    
    def reachedGoal(node):
        return heuristic(node) < goalPositionThreshold
    
    def adjacent(node):
        x_adj = node.x + node.dx
        y_adj = node.y + node.dy
        return [Node(x_adj, y_adj, node.dx + ddx, node.dy + ddy) for (ddx, ddy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    
    def heuristic(node):
        return math.sqrt(((node.x - goal.x) ** 2) + ((node.y - goal.y) ** 2))

    def retracePath(node):
        path = [node]
        while node in parentOf:
            node = parentOf[node]
            path.append(node)
        path.reverse()
        return [(n.x, n.y) for n in path]
        
    openSet.add(start)
    openHeap.append((0,start))
    while openSet:
        node = heapq.heappop(openHeap)[1]
        if reachedGoal(node):
            return retracePath(node)
        openSet.remove(node)
        closedSet.add(node)
        for adj in adjacent(node):
            if adj not in closedSet:
                if adj not in openSet:
                    openSet.add(adj)
                    heapq.heappush(openHeap, (heuristic(adj), adj))
                parentOf[adj] = node
    return []
    
    
start = Node(10, 10, 0, 0)
goal = Node(30, 30, 0, 0)

aStar(start, goal)

print("test")
