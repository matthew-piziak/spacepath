# Spacepath

Spacepath is a demonstration of A* pathfinding applied to Newtonian
physics.

To run the demo, invoke `python demo.py`

The demo spawns a spaceship in the upper left, a goal region in the
bottom right, and a random number of gray obstacles.

31 prerendered demos can be seen [here](http://imgur.com/a/K8XfM).

The spaceship paths to the goal region using a time-optimal path, with
two constraints:
    - the ship must come to a complete stop in the goal region
    - the ship must avoid any obstacles en route

Note that the ship obeys conservation of momentum and takes this fact
into account while calculating the optimal path.

The pathfinding algorithm used is standard A*. All domain information
about Newtonian physics is entirely contained in the `newt` heuristic
function. This demonstrates that A* can efficiently perform Newtonian
pathfinding. For a representative simulation the `newt` heuristic
searches only 0.1% of the space that would be explored by
breadth-first search.

## Implementation Details

### The Graph Model

Each search node is five dimensional:
    - location X
    - location Y
    - velocity X
    - velocity Y
    - angle

At each search step, the velocity is applied to the location. The ship also makes two choices:
    - burn or cruise
	- fly straight or turn left or turn right

This corresponds to a branching factor of 6. Angular resolution is not
currently conserved, but this is a planned future improvement.

#### Angular resolution

The ship sometimes wobbles as it navigates. This is because the
angular resolution is currently set to 8, which corresponds to turning
angles of 45 degrees. Increasing the angular resolution is a planned
future improvement.

#### Turning bias

When two paths are equivalent, the ship breaks ties deterministically:
    - cruising > burning
    - straight > clockwise > counterclockwise

#### Fast sine and cosine

Fast sine and cosine approximations are applied to make all locations
and velocities integral. This avoids floating-point errors in node
equality checking.

### Bounded relaxation

Bounded relaxation is a pathfinding technique where the heuristic
sacrifices some optimality in favor of letting the pathfinder search
deeper along the best-guess path. Spacepath uses a bounded relaxation
factor of 2%, which means that generated paths are only guaranteed to
be 98% optimal.

## Thanks

### Physics

Thanks to Physics StackExchange users [Kurtovic](http://physics.stackexchange.com/users/44104/kurtovic) and [nivag](http://physics.stackexchange.com/users/44576/nivag) for helping
me determine the kinematic equations necessary to solve for the heuristic.

[Original Question](http://physics.stackexchange.com/questions/112687/how-long-does-it-take-to-optimally-change-position-and-velocity)

### Math

Thanks to Mathematics StackExchange users [ah-huh-moment](http://math.stackexchange.com/users/101504/ah-huh-moment) and
[hypergeometric](http://math.stackexchange.com/users/168053/hypergeometric) for helping me solve the resulting algebraic system.

[Original Question](http://math.stackexchange.com/questions/1021921/solve-system-of-kinematics-equation)

### Art

Thank you zxBranden from OpenGameArt for the spaceship sprite.

[Original source](http://opengameart.org/users/zxbranden)
