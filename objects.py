#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math2d import Vector
import math


class PhysicalObject:
    """
    This class describes objects in 2d world
    """

    def __init__(self, position: Vector) -> None:
        self.position = position
        self.speed = Vector()
        self.mass = 1

    def step(self, dt: float):
        """
        Change object position based on delta time.

        :param dt: delta time for integration
        """
        raise RuntimeError("Not implemented here")


class Planet(PhysicalObject):
    def __init__(self, distance_to_sun=1, mass=1, initial_angle=0):
        super(Planet, self).__init__(Vector())
        self.distance_to_sun = distance_to_sun
        self.mass = mass
        self.initial_angle = initial_angle
        self.angle = initial_angle
        self.angular_velocity = math.sqrt(2 / self.distance_to_sun)
        self.position.x = self.distance_to_sun * math.cos(self.angle)
        self.position.y = self.distance_to_sun * math.sin(self.angle)

    def step(self, dt: float):
        # angular_velocity in constant over time
        self.angle += self.angular_velocity * dt
        self.position.x = self.distance_to_sun * math.cos(self.angle)
        self.position.y = self.distance_to_sun * math.sin(self.angle)


class Sun(PhysicalObject):
    def __init__(self):
        super(Sun, self).__init__()
        self.mass = 1000


class Cpu:
    """
    This class describes satellite initial state
    """

    def __init__(self, speed: float, angle: float, time: int) -> None:
        self.speed = speed
        self.angle = angle
        self.time = time


class Satellite(PhysicalObject):
    def __init__(self, start_position: Planet, cpu: Cpu):
        super(Satellite, self).__init__(Vector())

    def step(self, dt: float):
        pass
