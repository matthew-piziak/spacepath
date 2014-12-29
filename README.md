# Spacepath

Spacepath is a demonstration of A* pathfinding applied to Newtonian physics.

To run the demo, invoke `python demo.py`

The demo spawns a spaceship in the upper left, a goal region in the bottom
right, and a random number of gray obstacles.

The spaceship paths to the goal region using a time-optimal path, with two
constraints:
    - the ship must come to a complete stop in the goal region
    - the ship must avoid any obstacles en route

Note that the ship obeys conservation of momentum and takes this fact into
account while calculating the optimal path.

The pathfinding algorithm used is standard A*. All domain information about
Newtonian physics is entirely contained in the `newt` heuristic function. This
demonstrates that A* can efficiently perform Newtonian pathfinding. For a
representative simulation the `newt` heuristic searches only 0.1% of the space
that would be explored by breadth-first search.

## Implementation Details

### Bounded relaxation

Bounded relaxation is a pathfinding technique where the heuristic sacrifices
some optimality in favor of letting the pathfinder search deeper along the
best-guess path. Spacepath uses a bounded relaxation factor of 2%, which means
that generated paths are only guaranteed to be 98% optimal.

### Angular resolution

The ship sometimes wobbles as it navigates. This is because the angular
resolution is currently set to 8, which corresponds to turning angles of 45
degrees. Increasing the angular resolution is a planned future improvement.
