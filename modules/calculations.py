import numpy as np


def parallax_to_parsecs(parallax: np.ndarray):
    parsecs = 1000 / parallax  # remember that parallax is in milliseconds of arc

    return parsecs


def degrees_to_radians(angle_degrees: np.ndarray):
    angle_radians = angle_degrees * np.pi / 180

    return angle_radians


def cartesian_coordinates(r, ra, dec):
    x = r * np.cos(dec) * np.cos(ra)
    y = r * np.cos(dec) * np.sin(ra)
    z = r * np.sin(dec)

    return x, y, z
