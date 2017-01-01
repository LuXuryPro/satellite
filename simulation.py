#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import sys

from math2d import Vector
from objects import Planet, Satellite
from typing import List

G = 1


class Simulation:
    def __init__(self, planets: List[Planet],
            satellite: Satellite) -> None:
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
    def load_from_file(file_name) -> (List[Planet], Planet, Planet, int):

        file_name = file_name or "config.json"

        try:
            with open(file_name) as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            raise RuntimeError("File " + file_name + " was not found. Please provide it using readme as guide.")
        except Exception:
            raise RuntimeError("Your file " + file_name + " is not valid. Please check readme for examples.")

        planets_json = data["planets"]
        planets = []

        start_planet = None
        destination_planet = None

        for planet_json in planets_json:
            planet = Planet(int(planet_json["distance-to-sun"]),
                            int(planet_json["mass"]),
                            float(planet_json["start-angle"]))
            planets.append(planet)
            if planet_json.get('start'):
                start_planet = planet
            elif planet_json.get('destination'):
                destination_planet = planet

        sun_mass = int(data["sun-mass"])

        if not start_planet:
            raise RuntimeError(
                    "You must mark start planet in config file")
        if not destination_planet:
            raise RuntimeError(
                    "You must mark destination planet in config file")

        return planets, start_planet, destination_planet, sun_mass

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
