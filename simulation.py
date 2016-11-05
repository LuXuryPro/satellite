#!/usr/bin/env python
# -*- coding: utf-8 -*-

from objects import Planet, Satellite
from typing import  List


class Simulation:
    def __init__(self, planets: List[Planet], satellite: Satellite) -> None:
        self.planets = planets
        self.satellite = satellite

    def step(self, dt: float):
        for planet in self.planets:
            planet.step(dt)
        self.satellite.step(dt)
