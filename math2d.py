#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import json


class Vector:
    """
    2d vector class
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> None:
        length = self.length() or 0.0001
        self.x /= length
        self.y /= length

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: 'Vector') -> 'Vector':
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def distance(self, other: 'Vector') -> float:
        return self.direction(other).length()

    def direction(self, other: 'Vector') -> 'Vector':
        return other - self

    def get_int_vector(self):
        return Vector(int(self.x), int(self.y))

    def get_int_tuple(self):
        return (int(self.x), int(self.y))

    def __mul__(self, other: float) -> 'Vector':
        return Vector(self.x * other, self.y * other)

    def dot(self, other: 'Vector') -> float:
        """
        Calc vector dot product
        """
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def toDict(self):
        return {"x": self.x, "y": self.y}
