import numpy as np


class Transform:
    @staticmethod
    def rotate(p, angle):
        """
        Rotate a point around the origin by a given angle.
        p: pointList to rotate
        angle: angle to rotate by
        """
        print(p.shape)
        c, s = np.cos(angle), np.sin(angle)
        R = np.array(((c, -s), (s, c)))
        return np.dot(p, R)

    @staticmethod
    def translate(p, x, y):
        """
        Translate a point by a given amount.
        p: pointList to translate
        x: amount to translate in the x direction
        y: amount to translate in the y direction
        """
        return np.add(p, np.array((x, y)))

    @staticmethod
    def scale(p, x, y):
        """
        Scale a point by a given amount.
        p: pointList to scale
        x: amount to scale in the x direction
        y: amount to scale in the y direction
        """
        return np.multiply(p, np.array((x, y)))

    @staticmethod
    def expand(p, theta):
        """
        Expand a point by a given angle.
        p: pointList to expand
        theta: angle to expand by
        """
        r = p[:, 0]
        x = np.array([r * np.cos(theta), r * np.sin(theta), p[:, 1]]).T
        return x
