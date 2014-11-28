"""Draw interpolation"""

import numpy
from scipy import interpolate

INTERPOLATE = True
INTERPOLATION_FACTOR = 16

def interpolate_path(path):
    """generate a higher resolution path using cubic spline interpolation"""
    node_positions = [(n.x, n.y, n.angle) for n in path]
    if not INTERPOLATE:
        return node_positions
    t = numpy.arange(0, len(node_positions))
    f_x = interpolate.interp1d(t, [p[0] for p in node_positions], 'cubic')
    f_y = interpolate.interp1d(t, [p[1] for p in node_positions], 'cubic')
    t_new = numpy.arange(0, len(node_positions) - 2, 1.0 / INTERPOLATION_FACTOR)
    interpolated_x = f_x(t_new)
    interpolated_y = f_y(t_new)
    interpolated_angle = _angles([p[2] for p in node_positions])
    return zip(interpolated_x, interpolated_y, interpolated_angle)

def _angles(angles):
    """custom linear modulus interpolation for angles"""
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
