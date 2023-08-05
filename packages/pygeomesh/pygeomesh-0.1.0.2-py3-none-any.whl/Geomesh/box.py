from .geometry import Geometry
import numpy as np


class Box(Geometry):
    def __init__(
        self,
        center: list,
        length: float,
        width: float,
        height: float,
        q: list = [0, 0, 0],
        time_dependent=False,
    ) -> None:
        super().__init__(time_dependent)
        self.center = center
        self.q = q
        self.length = length
        self.width = width
        self.height = height
        self.transformationMatrix = self.get_transformationMatrix()
        self.above_points = self.get_above_points()
        self.below_points = self.get_below_points()

    def __str__(self):
        return "Box: center: {}, q: {}, length: {}, width: {}, height: {}, ".format(
            self.center, self.q, self.length, self.width, self.height
        )

    @staticmethod
    def get_transformationMatrix(q):
        """
        Calculate rotation matrix from Euler angle meter.

        We first rotate around the z axis, then around the y axis,
        and finally around the x axis.

        ### TODO: check if q is correct
        ### Return:
        - `transformationMatrix`: transformation matrix
        """

        # compute the transformation matrix
        # we use the euler angles to rotate the box z-y-x
        gamma = np.array(
            [
                [np.cos(q[0]), -np.sin(q[0]), 0],
                [np.sin(q[0]), np.cos(q[0]), 0],
                [0, 0, 1],
            ]
        )
        beta = np.array(
            [
                [1, 0, 0],
                [0, np.cos(q[1]), -np.sin(q[1])],
                [0, np.sin(q[1]), np.cos(q[1])],
            ]
        )
        alpha = np.array(
            [
                [np.cos(q[2]), 0, np.sin(q[2])],
                [0, 1, 0],
                [-np.sin(q[2]), 0, np.cos(q[2])],
            ]
        )
        return np.dot(np.dot(gamma, beta), alpha)

    def do_transform(self, x):
        """
        Transform a point from the box to the global frame.

        ### Args:
        - `x` (dict): point to transform
        ### Return:
        - `x` (dict): transformed point
        """
        for key in x:
            x[key] = x[key] - self.center
            x[key] = np.dot(self.transformationMatrix, x[key].T).T
            x[key] = x[key] + self.center
        return x

    def get_above_points(self):
        above_point = np.array(
            [
                [
                    self.center[0] - self.length / 2,
                    self.center[1] - self.width / 2,
                    self.center[2] + self.height,
                ],
                [
                    self.center[0] + self.length / 2,
                    self.center[1] - self.width / 2,
                    self.center[2] + self.height,
                ],
                [
                    self.center[0] + self.length / 2,
                    self.center[1] + self.width / 2,
                    self.center[2] + self.height,
                ],
                [
                    self.center[0] - self.length / 2,
                    self.center[1] + self.width / 2,
                    self.center[2] + self.height,
                ],
            ]
        )
        return above_point

    def get_below_points(self):
        below_point = np.array(
            [
                [
                    self.center[0] - self.length / 2,
                    self.center[1] - self.width / 2,
                    self.center[2],
                ],
                [
                    self.center[0] + self.length / 2,
                    self.center[1] - self.width / 2,
                    self.center[2],
                ],
                [
                    self.center[0] + self.length / 2,
                    self.center[1] + self.width / 2,
                    self.center[2],
                ],
                [
                    self.center[0] - self.length / 2,
                    self.center[1] + self.width / 2,
                    self.center[2],
                ],
            ]
        )
        return below_point

    def _is_internal(self, x):
        """
        Check if a point is inside the box.

        ### Args:
        - `x` (list): point to check
        ### Return:
        - `is_internal` (bool): True if point is inside the box, False otherwise
        """
        # check if point is inside the box
        if np.all(x >= self.center - self.length / 2) and np.all(
            x <= self.center + self.length / 2
        ):
            return True
        else:
            return False

    def is_internal(self, x):
        """
        Check if a list point is inside the box.
        ### Args:
        - `x` (list): list of points to check like [[x1, y1, z1], [x2, y2, z2], ...]
        ### Return:
        - `is_internal` (list): True if point is inside the box, False otherwise
        """
        if isinstance(x, list):
            return [self._is_internal(i) for i in x]
        else:
            return self._is_internal(x)

    def _is_boundary(self, x):
        """
        Check if a point is on the boundary of the box.

        ### Args:
        - `x` (list): point to check
        ### Return:
        - `is_boundary` (bool): True if point is on the boundary of the box, False otherwise
        """
        # check if point is on the boundary of the box
        if np.all(x == self.center - self.length / 2) or np.all(
            x == self.center + self.length / 2
        ):
            return True
        else:
            return False

    def is_boundary(self, x):
        """
        Check if a list point is on the boundary of the box.
        ### Args:
        - `x` (list): list of points to check like [[x1, y1, z1], [x2, y2, z2], ...]
        ### Return:
        - `is_boundary` (list): True if point is on the boundary of the box, False otherwise
        """
        return [self._is_boundary(i) for i in x]

    def grid_points(self, n):
        """
        Generate a grid of points inside the box.

        ### Args:
        - `n` (int): spacing of the grid
        ### Return:
        - `grid_points` (list): list of points inside the box
        """
        # generate a list of points on the box
        x = np.linspace(
            self.center[0] - self.length / 2, self.center[0] + self.length / 2, n
        )
        y = np.linspace(
            self.center[1] - self.width / 2, self.center[1] + self.width / 2, n
        )
        z = np.linspace(self.center[2], self.center[2] + self.height, n)
        points = np.vstack(np.meshgrid(x, y, z)).reshape(3, -1).T
        points = np.dot(self.transformationMatrix, points.T).T
        self.points = points
        return points

    def grid_points_on_edge(self, n):
        """
        Generate a grid of points on the edge of the box.

        ### Args:
        - `n` (int): spacing of the grid
        ### Return:
        - `grid_points` (list): list of points on the edge of the box
        """
        edge_points = {}
        for i in [0, 2]:
            point = np.arange(
                self.above_points[i, 0],
                self.above_points[(i + 1) % 4, 0],
                1
                / n
                * (1, -1)[self.above_points[i, 0] > self.above_points[(i + 1) % 4, 0]],
            )
            edge_points[i] = np.vstack(
                (
                    point,
                    self.above_points[i, 1] * np.ones(len(point)),
                    self.above_points[i, 2] * np.ones(len(point)),
                )
            ).T

            point = np.arange(
                self.below_points[i, 0],
                self.below_points[(i + 1) % 4, 0],
                1
                / n
                * (1, -1)[self.below_points[i, 0] > self.below_points[(i + 1) % 4, 0]],
            )
            edge_points[i + 4] = np.vstack(
                (
                    point,
                    self.below_points[i, 1] * np.ones(len(point)),
                    self.below_points[i, 2] * np.ones(len(point)),
                )
            ).T

        for i in [1, 3]:
            point = np.arange(
                self.above_points[i, 1],
                self.above_points[(i + 1) % 4, 1],
                1
                / n
                * (1, -1)[self.above_points[i, 1] > self.above_points[(i + 1) % 4, 1]],
            )
            edge_points[i] = np.vstack(
                (
                    self.above_points[i, 0] * np.ones(len(point)),
                    point,
                    self.above_points[i, 2] * np.ones(len(point)),
                )
            ).T

            point = np.arange(
                self.below_points[i, 1],
                self.below_points[(i + 1) % 4, 1],
                1
                / n
                * (1, -1)[self.below_points[i, 1] > self.below_points[(i + 1) % 4, 1]],
            )
            edge_points[i + 4] = np.vstack(
                (
                    self.below_points[i, 0] * np.ones(len(point)),
                    point,
                    self.below_points[i, 2] * np.ones(len(point)),
                )
            ).T

        for i in range(4):
            point = np.arange(
                self.above_points[i, 2],
                self.below_points[i, 2],
                1 / n * (1, -1)[self.above_points[i, 2] > self.below_points[i, 2]],
            )
            edge_points[i + 8] = np.vstack(
                (
                    self.above_points[i, 0] * np.ones(len(point)),
                    self.above_points[i, 1] * np.ones(len(point)),
                    point,
                )
            ).T

        edge_points = self.do_transform(edge_points)

        return edge_points

    def grid_points_on_surface(self, spacing):
        """
        Generate a dict of points on the box surface.

        ### Args:
        - `spacing`: spacing between points on the surface

        ### Returns:
        - `surface_points`: dict of points on the box surface
        """

        surfacepoints = {}
        x = np.arange(
            self.center[0] - self.length / 2,
            self.center[0] + self.length / 2,
            1 / spacing * (1, -1)[self.center[0] > self.center[0] + self.length / 2],
        )
        y = np.arange(
            self.center[1] - self.width / 2,
            self.center[1] + self.width / 2,
            1 / spacing * (1, -1)[self.center[1] > self.center[1] + self.width / 2],
        )
        z = np.arange(
            self.center[2],
            self.center[2] + self.height,
            1 / spacing * (1, -1)[self.center[2] > self.center[2] + self.height],
        )
        flag = 1
        for i in range(2):
            point = (
                np.meshgrid(x, self.center[1] + flag * self.width / 2, z)
                .reshape(3, -1)
                .T
            )
            surfacepoints[i] = np.dot(self.transformationMatrix, point.T).T
            flag *= -1

        for i in range(2):
            point = (
                np.meshgrid(self.center[0] + flag * self.length / 2, y, z)
                .reshape(3, -1)
                .T
            )
            surfacepoints[i + 2] = np.dot(self.transformationMatrix, point.T).T
            flag *= -1

        point = np.meshgrid(x, y, self.center[2] + self.height).reshape(3, -1).T
        surfacepoints[4] = np.vstack((point[:, 0], point[:, 1], point[:, 2])).T
        point = np.meshgrid(x, y, self.center[2]).reshape(3, -1).T
        surfacepoints[5] = np.vstack((point[:, 0], point[:, 1], point[:, 2])).T

        return surfacepoints

    def grid_points_on_boundary(self, spacing):
        """
        Generate a list of points on the box boundary.

        ### Args:
        - `spacing`: spacing between points on the boundary

        ### Returns:
        - `boundary_points`: list of points on the box boundary
        """

        edge_points = self.grid_points_on_edge(spacing)
        surfacepoints = self.grid_points_on_surface(spacing)

        boundary_points = {}
        for i in range(12):
            boundary_points["e" + str(i)] = edge_points[i]
        for i in range(6):
            boundary_points["s" + str(i)] = surfacepoints[i]
        self.boundary_points = boundary_points
        return boundary_points

    def random_points(self, n):
        """
        Generate a dict of random points on the box.
        ### Args:
        - `n` : number of points
        ### Returns:
        dict: dict of random points on the box
        """
        vlist = []
        for i in range(n):
            x = np.random.uniform(
                self.center[0] - self.length / 2, self.center[0] + self.length / 2
            )
            y = np.random.uniform(
                self.center[1] - self.width / 2, self.center[1] + self.width / 2
            )
            z = np.random.uniform(self.center[2], self.center[2] + self.height)
            vlist.append([x, y, z])

        points = np.vstack(vlist)
        points = np.dot(self.transformationMatrix, points.T).T
        return points

    def random_points_on_edge(self, n):
        """
        Generate a dict of random points on the box edges.
        ### Args:
        n (int): number of points

        ### Returns:
        dict: dict of random points on the box edges
        """
        edge_points = {}
        # generate points towards the x-axis and the n is like self.length
        for i in [0, 2]:
            point = np.random.uniform(
                self.above_points[i, 0],
                self.above_points[(i + 1) % 4, 0],
                int(n * (self.length / self.length)),
            )
            edge_points[i] = np.vstack(
                (
                    point,
                    self.above_points[i, 1] * np.ones(len(point)),
                    self.above_points[i, 2] * np.ones(len(point)),
                )
            ).T
            point = np.random.uniform(
                self.below_points[i, 0],
                self.below_points[(i + 1) % 4, 0],
                int(n * (self.length / self.length)),
            )
            edge_points[i + 4] = np.vstack(
                (
                    point,
                    self.below_points[i, 1] * np.ones(len(point)),
                    self.below_points[i, 2] * np.ones(len(point)),
                )
            ).T

        # generate points towards the y-axis and the n is like self.width
        for i in [1, 3]:
            point = np.random.uniform(
                self.above_points[i, 1],
                self.above_points[(i + 1) % 4, 1],
                int(n * (self.width / self.length)),
            )
            edge_points[i] = np.vstack(
                (
                    self.above_points[i, 0] * np.ones(len(point)),
                    point,
                    self.above_points[i, 2] * np.ones(len(point)),
                )
            ).T

            point = np.random.uniform(
                self.below_points[i, 1],
                self.below_points[(i + 1) % 4, 1],
                int(n * (self.width / self.length)),
            )
            edge_points[i + 4] = np.vstack(
                (
                    self.below_points[i, 0] * np.ones(len(point)),
                    point,
                    self.below_points[i, 2] * np.ones(len(point)),
                )
            ).T

        # generate points towards the z-axis and the n is like self.height
        for i in range(4):
            point = np.random.uniform(
                self.above_points[i, 2],
                self.below_points[i, 2],
                int(n * (self.height / self.length)),
            )
            edge_points[i + 8] = np.vstack(
                (
                    self.above_points[i, 0] * np.ones(len(point)),
                    self.above_points[i, 1] * np.ones(len(point)),
                    point,
                )
            ).T

        edge_points = self.do_transform(edge_points)

        return edge_points

    def random_points_on_surface(self, n):
        """
        Generate a dict of points on the box surface.

        ### Args:
        n (int): number of points

        ### Returns:
        dict of points on the box surface
        """
        surfacepoints = {}
        for i in range(2):
            point = []
            for j in range(int(n)):
                x = np.random.uniform(
                    self.center[0] - self.length / 2, self.center[0] + self.length / 2
                )
                y = np.random.uniform(
                    self.center[1] - self.width / 2, self.center[1] + self.width / 2
                )
                point.append([x, y, self.center[2] + self.height * i])
            surfacepoints[i] = np.vstack(point)

        for i in range(2):
            point = []
            for j in range(int(n * (self.height / self.width))):
                x = np.random.uniform(
                    self.center[0] - self.length / 2, self.center[0] + self.length / 2
                )
                z = np.random.uniform(self.center[2], self.center[2] + self.height)
                point.append(
                    [x, self.center[1] + (self.width / 2) * (1, -1)[i == 0], z]
                )
            surfacepoints[i + 2] = np.vstack(point)

        for i in range(2):
            point = []
            for j in range(int(n * (self.height / self.length))):
                y = np.random.uniform(
                    self.center[1] - self.width / 2, self.center[1] + self.width / 2
                )
                z = np.random.uniform(self.center[2], self.center[2] + self.height)
                point.append(
                    [self.center[0] + (self.length / 2) * (1, -1)[i == 0], y, z]
                )
            surfacepoints[i + 4] = np.vstack(point)

        surfacepoints = self.do_transform(surfacepoints)

        return surfacepoints

    def random_points_on_boundary(self, surfacen: int, edgen: int = None) -> dict:
        """
        Generate a dict of points on the box boundary.
        ### Args:
        - surfacen (int): number of points on the surface
        - edgen (int): number of points on the edge (default: None)

        ### Note:
        - If edgen is None, surfacen square will be set as edgen.

        ### Returns:
        dict: dict of points on the box boundary
        """
        if edgen is None:
            edgen = int(np.floor(np.sqrt(surfacen)))
        boundary = {}
        edge_points = self.random_points_on_edge(edgen)
        surface_points = self.random_points_on_surface(surfacen)

        for i in range(6):
            boundary["s" + str(i)] = surface_points[i]

        for i in range(12):
            boundary["e" + str(i)] = edge_points[i]

        self.boundary_points = boundary

        return boundary
