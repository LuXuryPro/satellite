#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math2d import Vector
from objects import Planet, Satellite
from typing import List

G = 1


class Simulation:
    def __init__(self, planets: List[Planet], satellite: Satellite) -> None:
        self.sun_mass = 10000
        self.planets = planets
        self.satellite = satellite

    def step(self, dt: float):
        for planet in self.planets:
            planet.step(dt)
        force_vector = self.calc_overall_force()
        self.satellite.set_force(force_vector)
        self.satellite.step(dt)

    def load_from_file(self, file_name: str):
        pass

    def calc_overall_force(self) -> Vector:
        force = Vector()
        for planet in self.planets:
            distance = self.satellite.position.distance(planet.position)
            direction = self.satellite.position.direction(planet.position)
            direction.normalize()
            this_planet_force_magnitude = planet.mass * G / (
                distance * distance)
            force = force + direction * this_planet_force_magnitude
        # sun force
        distance = self.satellite.position.distance(Vector(0, 0))
        direction = self.satellite.position.direction(Vector(0, 0))
        direction.normalize()
        sun_force_magnitude = (self.sun_mass * G) / (distance * distance)
        force = force + direction * sun_force_magnitude

        return force
