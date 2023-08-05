from .sampler import Sampler
from .geometry import Geometry
import numpy as np


class Point(Geometry):
    def __init__(self, center, radius, time_dependent=False):
        super().__init__(time_dependent)
        self.center = center
        self.radius = radius
        self.dim = len(center)

    def __str__(self):
        return "Point({}, {})".format(self.center, self.radius)

    def is_internal(self, x):
        return np.linalg.norm(x - self.center, axis=1) <= self.radius

    def is_boundary(self, x):
        return np.linalg.norm(x - self.center, axis=1) == self.radius

    def grid_points(self, n):
        vlist = []
        for i in range(self.dim):
            vlist.append(
                Sampler(
                    1,
                    n,
                    self.center[i] - self.radius,
                    self.center[i] + self.radius,
                    type="grid",
                )
            )

        points = np.vstack(np.meshgrid(*vlist)).reshape(self.dim, -1).T
        points = points[self.is_internal(points)]
        self.points = points
        return points

    def grid_points_on_boundary(self, n):
        if self.dim == 2:
            theta = Sampler(1, n, 0, 2 * np.pi, type="grid")
            points = np.vstack(
                (
                    self.center[0] + self.radius * np.cos(theta),
                    self.center[1] + self.radius * np.sin(theta),
                )
            ).T
        elif self.dim == 3:
            i = Sampler(1, n, 0, n, type="grid")
            phi = np.arccos(((2 * i - 1) / n - 1).clip(-1, 1))
            theta = np.sqrt(n * np.pi) * phi
            points = np.vstack(
                (
                    self.center[0] + self.radius * np.cos(theta) * np.sin(phi),
                    self.center[1] + self.radius * np.sin(theta) * np.sin(phi),
                    self.center[2] + self.radius * np.cos(phi),
                )
            ).T
        self.boundary_points["b0"] = points
        self.boundary_points["num"] = 1
        return points

    def random_points(self, n):
        # http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/
        u = Sampler(self.dim, n, 0, 1, samplingtype="normal")
        norm = np.sum(u ** 2, axis=0) ** (0.5)
        r = self.radius * np.random.random(n) ** (1.0 / self.dim)
        points = r * u / norm
        points = points.T + self.center
        self.points = points
        return points

    def random_points_on_boundary(self, n, seed=None):
        if self.dim == 2:
            theta = Sampler(1, n, 0, 2 * np.pi, samplingtype="random")
            points = np.vstack(
                (self.radius * np.cos(theta), self.radius * np.sin(theta))
            ).T
        elif self.dim == 3:
            u = Sampler(1, n, 0, 1, samplingtype="normal")
            v = Sampler(1, n, 0, 1, samplingtype="normal")
            w = Sampler(1, n, 0, 1, samplingtype="normal")

            norm = np.sqrt(u ** 2 + v ** 2 + w ** 2)
            x = u / norm
            y = v / norm
            z = w / norm

            points = np.vstack((x, y, z)).T
            points = points * self.radius + self.center
        self.boundary_points["b0"] = points
        self.boundary_points["num"] = 1
        return points
