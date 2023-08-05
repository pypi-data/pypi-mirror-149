from .geometry import Geometry
import numpy as np
from .box import Box


class Cylinder(Geometry):
    def __init__(
        self, pos, radius=1, length=1, q: list = [0, 0, 0], time_dependent=False
    ):
        """
        Creat a Cylinder.
        ### Args:
        - `pos` : The position of the Cylinder.
        - `radius` : The radius of the Cylinder. Default is 1.
        - `length` : The length of the Cylinder. Default is 1.
        - `q` : The euler angles of the Cylinder. Default is [0, 0, 0].\n
        First angle is the rotation around the z-axis, second angle is the\n
        rotation around the y-axis, and the third angle is the rotation around\n
        the x-axis.
        - `time_dependent` : True if the Cylinder is time dependent. Default is False.

        ### Returns:
        - `Cylinder` : A Cylinder.
        """
        super().__init__(time_dependent)
        self.pos = pos
        self.radius = radius
        self.length = length
        self.q = q
        self.transformationMatrix = Box.get_transformationMatrix(self.q)

    def __str__(self):
        return "Cylinder({}, {}, {})".format(self.pos, self.radius, self.axis)

    def is_internal(self, x):
        """
        Returns True if the point x is internal to the Geometry.
        ### Args:
        - `x` : A point as like [x, y, z]
        ### Returns:
        - `bool` : True if the point x is internal to the Geometry.
        """
        x = np.array(x)
        x = np.dot(np.linalg.inv(self.transformationMatrix), x.T).T
        x = x - self.pos
        print(x.shape)
        r_log = np.linalg.norm(x[:, :-1], axis=1) < self.radius
        l_log = np.logical_and(x[:, -1] < self.length, x[:, -1] > 0)
        return np.logical_and(r_log, l_log)

    def _is_boundary(self, x):
        """
        Returns True if the point x is on the boundary of the Geometry.
        ### Args:
        - `x` : A point as like [x, y, z]
        ### Returns:
        - `bool` : True if the point x is on the boundary of the Geometry.
        """
        x = np.array(x)
        x = np.dot(np.linalg.inv(self.transformationMatrix), x.T).T
        x = x - self.pos
        return np.linalg.norm(x) == self.radius

    def is_boundary(self, x):
        """
        Returns True if the point x is on the boundary of the Geometry.
        ### Args:
        - `x` : list of points as like [[x, y, z], [x, y, z], ...]
        ### Returns:
        - `bool` : True if the point x is on the boundary of the Geometry.
        """
        if isinstance(x, list):
            return [self._is_boundary(xi) for xi in x]
        else:
            return self._is_boundary(x)

    def grid_points(self, n):
        """
        Returns a list of points on the Geometry.
        ### Args:
        - `n` : Number of points on the Geometry.
        ### Returns:
        - `list` : A list of points on the Geometry.
        """
        x = np.linspace(-self.radius, self.radius, n)
        y = np.linspace(-self.radius, self.radius, n)
        z = np.linspace(0, self.length, n)
        points = np.meshgrid(x, y, z)
        points = np.array(points).reshape(3, -1).T
        points = np.dot(self.transformationMatrix, points.T).T
        point = points[self.is_internal(points)]
        point = point + self.pos
        points = np.dot(self.transformationMatrix, point.T).T
        return points

    def grid_points_on_boundary(self, n):
        # boundary_points = {}
        theta = np.linspace(0, 2 * np.pi, n)
        l_po = np.linspace(0, self.length, n)
        vlist = []
        for i in range(n):
            point = np.array(
                [
                    self.radius * np.cos(theta),
                    self.radius * np.sin(theta),
                    l_po[i] * np.ones(n),
                ]
            )
            print(point.shape)
            vlist.append(point.reshape(-1, 3))

        vlist = np.vstack(vlist)
        vlist = vlist + self.pos
        vlist = np.dot(self.transformationMatrix, vlist.T).T
        return vlist
