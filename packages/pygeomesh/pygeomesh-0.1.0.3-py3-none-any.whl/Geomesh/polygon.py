from .geometry import Geometry
from .sampler import Sampler
import numpy as np
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint


class Polygon(Geometry):
    def __init__(self, pointlist, time_dependent=False):
        super().__init__(time_dependent)
        self.shape = ShapelyPolygon(pointlist)
        self.pointlist = pointlist
        self.ndim = len(pointlist[0])
        self.n = len(pointlist)
        self.l_bounds = np.zeros(self.ndim)
        self.u_bounds = np.zeros(self.ndim)
        for i in range(self.ndim):
            self.l_bounds[i] = min([point[i] for point in pointlist])
            self.u_bounds[i] = max([point[i] for point in pointlist])

    def __str__(self):
        return "Polygon(%s)" % self.pointlist

    def _is_internal(self, x):
        return self.shape.intersects(ShapelyPoint(x))

    def is_internal(self, x):
        return [self._is_internal(point) for point in x]

    def _is_boundary(self, x):
        return self.shape.touches(ShapelyPoint(x))

    def is_boundary(self, x):
        return [self._is_boundary(point) for point in x]

    def grid_points(self, n):
        vlist = []
        for i in range(self.ndim):
            vlist.append(
                Sampler(1, n, self.l_bounds[i], self.u_bounds[i], samplingtype="grid")
            )

        points = np.vstack(np.meshgrid(*vlist)).reshape(self.ndim, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

    def grid_points_on_boundary(self, width):
        vlist = []
        for i in range(self.n):
            dx = self.pointlist[(i + 1) % self.n][0] - self.pointlist[i][0]
            dy = self.pointlist[(i + 1) % self.n][1] - self.pointlist[i][1]

            if dx == 0:
                y = Sampler(
                    1,
                    (1 / width, -1 / width)[dy < 0],
                    self.pointlist[i][1],
                    self.pointlist[(i + 1) % self.n][1],
                    samplingtype="grid",
                )
                x = np.full_like(y, self.pointlist[i][0])
            elif dy == 0:
                x = Sampler(
                    1,
                    (1 / width, -1 / width)[dx < 0],
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    samplingtype="grid",
                )
                y = np.full_like(x, self.pointlist[i][1])
            else:
                d = np.sqrt(np.square(1 / width) / (1 + np.square(dx / dy)))
                x = Sampler(
                    1,
                    (d, -d)[dx < 0],
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    samplingtype="grid",
                )
                y = (dy / dx) * (x - self.pointlist[i][0]) + self.pointlist[i][1]
            vlist.append(np.vstack((x, y)).T)
            # every segment will save like this: {'b0': [[x1, y1],...], 'b1': [[x2, y2],...], ...}
            self.boundary_points["b" + str(i)] = np.vstack((x, y)).T

        self.boundary_points["num"] = self.n
        # for development
        points = np.vstack(vlist)
        return points

    def random_points(self, n, samplingtype="random"):
        vlist = []
        for i in range(n):
            x = Sampler(
                1, 1, self.l_bounds[0], self.u_bounds[0], samplingtype=samplingtype
            )
            y = Sampler(
                1, 1, self.l_bounds[1], self.u_bounds[1], samplingtype=samplingtype
            )
            while not self._is_internal([x, y]):
                x = Sampler(
                    1, 1, self.l_bounds[0], self.u_bounds[0], samplingtype=samplingtype
                )
                y = Sampler(
                    1, 1, self.l_bounds[1], self.u_bounds[1], samplingtype=samplingtype
                )
            vlist.append([x, y])

        self.points = np.vstack(np.array(vlist).T).T.squeeze()
        return self.points

    def random_points_on_boundary(self, width):
        vlist = []
        for i in range(self.n):
            dx = self.pointlist[(i + 1) % self.n][0] - self.pointlist[i][0]
            dy = self.pointlist[(i + 1) % self.n][1] - self.pointlist[i][1]
            len = np.sqrt(dx ** 2 + dy ** 2)
            n = int(width * len)
            if dx == 0:
                y = Sampler(
                    1,
                    n,
                    self.pointlist[i][1],
                    self.pointlist[(i + 1) % self.n][1],
                    samplingtype="random",
                )
                x = np.full_like(y, self.pointlist[i][0])
            elif dy == 0:
                x = Sampler(
                    1,
                    n,
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    samplingtype="random",
                )
                y = np.full_like(x, self.pointlist[i][1])
            else:
                x = Sampler(
                    1,
                    n,
                    self.pointlist[i][0],
                    self.pointlist[(i + 1) % self.n][0],
                    samplingtype="random",
                )
                y = (dy / dx) * (x - self.pointlist[i][0]) + self.pointlist[i][1]
            vlist.append(np.vstack((x, y)).T)
            # every segment will save like this: {'b0': [[x1, y1],...], 'b1': [[x2, y2],...], ...}
            self.boundary_points["b" + str(i)] = np.vstack((x, y)).T

        self.boundary_points["num"] = self.n
        # for development
        points = np.vstack(vlist)
        return points
