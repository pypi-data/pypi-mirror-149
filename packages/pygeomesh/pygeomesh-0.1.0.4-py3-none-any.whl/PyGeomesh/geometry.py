import abc
import numpy as np
from .sampler import Sampler


class Geometry(abc.ABC):
    def __init__(self, time_dependent):
        self.time_dependent = time_dependent
        self.points = []
        self.time_points = []
        self.boundary_points = dict()
        self.boundary_points["num"] = None

    # @abc.abstractmethod
    def is_internal(self, x):
        """
        Returns True if the point x is internal to the Geometry.
        """
        pass

    # @abc.abstractmethod
    def is_boundary(self, x):
        """
        Returns True if the point x is on the boundary of the Geometry.
        """
        pass

    # @abc.abstractmethod
    def grid_points(self, n):
        """
        Returns a list of n grid points.
        """
        pass

    # @abc.abstractmethod
    def grid_points_on_boundary(self, n):
        """
        Returns a list of n grid points on the boundary.
        """
        pass

    # @abc.abstractmethod
    def random_points(self, n):
        """
        Returns a list of n random points.
        """
        pass

    # @abc.abstractmethod
    def random_points_on_boundary(self, n):
        """
        Returns a list of n random points on the boundary.
        """
        pass

    def uniform_time_dependent(self, n, time_start, time_end):
        """
        Returns a list of n time-dependent points.
        """
        pass

    def random_time_dependent(self, n, time_start, time_end, samplingtype=None):
        time = Sampler(1, n, time_start, time_end, samplingtype=type)
        self.time_points = time
        return time

    def union(self, other):
        """
        Returns the union of the two geometries.
        """
        pass

    def intersection(self, other):
        """
        Returns the intersection of the two geometries.
        """
        pass

    def difference(self, other):
        # produce a list of points that are in self but not in other
        for boundary in self.boundary_points:

            self.boundary_points[boundary] = self.boundary_points[boundary][
                np.logical_not(other.is_internal(self.boundary_points[boundary]))
            ]

        # produce a list of points that are in other but not in self
        for boundary in other.boundary_points:

            self.boundary_points[num] = other.boundary_points[boundary][
                self.is_internal(other.boundary_points[boundary])
            ]

        # produce a list of points that are in both self and other
        self.points = self.points[np.logical_not(other.is_internal(self.points))]
