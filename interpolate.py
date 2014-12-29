"""Draw interpolation"""

from collections import namedtuple
from scipy import interpolate
import numpy

INTERPOLATE = True
INTERPOLATION_FACTOR = 12

InterpolationNode = namedtuple('InterpolationNode', ['x', 'y', 'angle'])

def interpolate_path(path):
    """Generate a higher resolution path using cubic spline interpolation."""
    def get_interpolation_node(node):
        """Simplify the node so that interpolation is easier."""
        return InterpolationNode(node[0].x, node[0].y, node[0].angle)
    interpolaton_nodes = [get_interpolation_node(n) for n in path]
    if not INTERPOLATE:
        return interpolaton_nodes
    t = numpy.arange(0, len(interpolaton_nodes))
    f_x = interpolate.interp1d(t, [p.x for p in interpolaton_nodes], 'cubic')
    f_y = interpolate.interp1d(t, [p.y for p in interpolaton_nodes], 'cubic')
    t_new = numpy.arange(0,
                         len(interpolaton_nodes) - 2,
                         1.0 / INTERPOLATION_FACTOR)
    interpolated_x = f_x(t_new)
    interpolated_y = f_y(t_new)
    interpolated_angle = _angles([p.angle for p in interpolaton_nodes])
    actionless_path = zip(interpolated_x, interpolated_y, interpolated_angle)
    def get_actions(path):
        """Get actions for each node in the interpolated path.

        Each interpolated node is assigned the same action as the
        previous real node.

        """
        actions = []
        for node in path:
            actions += [node[1] for _ in range(INTERPOLATION_FACTOR)]
        return actions
    interpolated_path = zip(actionless_path, get_actions(path))
    return interpolated_path

def _angles(angles):
    """Perform linear modulus interpolation for angles."""
    interpolated_angles = []
    fraction = 1.0 / INTERPOLATION_FACTOR
    for i in range(len(angles) - 1):
        start_angle = float(angles[i])
        end_angle = float(angles[i + 1])
        if abs(end_angle - start_angle) <= 4:
            for j in range(INTERPOLATION_FACTOR):
                start_factor = (INTERPOLATION_FACTOR - j) * start_angle
                end_factor = j * end_angle
                interpolated_angle = (start_factor + end_factor) * fraction
                interpolated_angles.append(interpolated_angle)
        else:
            for j in range(INTERPOLATION_FACTOR):
                if start_angle < 4:
                    start_angle += 8
                if end_angle < 4:
                    end_angle += 8
                start_factor = (INTERPOLATION_FACTOR - j) * start_angle
                end_factor = j * end_angle
                interpolated_angle = start_factor + end_factor
                interpolated_angle = (interpolated_angle * fraction) % 8
                interpolated_angles.append(interpolated_angle)
    return interpolated_angles
