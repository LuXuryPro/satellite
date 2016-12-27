#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import sys

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

    @staticmethod
    def load_from_file() -> (List[Planet], Planet, Planet):

        file_name = "config.json"
        if len(sys.argv) > 1:
            file_name = sys.argv[1]

        try:
            with open(file_name) as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            print("File " + file_name + " was not found. Please provide it using readme as guide.")
            sys.exit(0)
        except Exception:
            print("Your file " + file_name + " is not valid. Please check readme for examples.")
            sys.exit(0)

        planets_json = data["simulation"]["planets"]
        planets = []

        for i in range(len(planets_json)):
            planet_json = planets_json[i]
            planets.append(Planet(int(planet_json["distance-to-sun"]), int(planet_json["mass"]),
                                  float(planet_json["start-angle"])))

        start_index = int(data["simulation"]["start-planet"])
        destination_index = int(data["simulation"]["destination-planet"])

        if start_index < 0 or start_index >= len(planets) or \
                        destination_index < 0 or destination_index >= len(planets):
            print("Your file " + file_name + " is not valid. Please check readme for examples.")
            sys.exit(0)

        start_planet = planets[start_index]
        destination_planet = planets[destination_index]

        return planets, start_planet, destination_planet

    def calc_overall_force(self) -> Vector:
        force = Vector()
        for planet in self.planets:
            distance = self.satellite.position.distance(planet.position)
            direction = self.satellite.position.direction(planet.position)
            direction.normalize()
            this_planet_force_magnitude = planet.mass * G / (
                distance * distance)
            force += (direction * this_planet_force_magnitude)
        # sun force
        distance = self.satellite.position.distance(Vector(0, 0))
        direction = self.satellite.position.direction(Vector(0, 0))
        direction.normalize()
        sun_force_magnitude = (self.sun_mass * G) / (distance * distance)
        force += (direction * sun_force_magnitude)

        return force
