#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Evolution algorithm to evolve best initial state for satellite

Function to minimize

f() = satelite_fly_time + satelite_closest_approach
"""
import math

import random
from objects import Planet
from objects import Satellite
from simulation import Simulation


class Cpu:
    """
    This class describes satellite initial state
    """

    def __init__(self, speed: float, angle: float, time: int) -> None:
        self.speed = speed
        self.angle = angle
        self.time = time
        self.score = 10e10
        self.closest_encounter = 0
        self.closest_encounter_time = 0

    def cross_over_other(self, other: 'Cpu', stability):
        speed = (self.speed + other.speed) / 2 + (2 * stability * random.random() - stability)
        angle = (self.angle + other.angle) / 2 + (2 * stability * random.random() - stability)
        time = (self.time + other.time) / 2 + (2 * stability * random.random() - stability)
        return Cpu(speed, angle, time)

    def __str__(self):
        return str(self.score) + " speed: " + str(self.speed) + " angle: " + str(self.angle) + " time: " + str(self.time) + " ce: " + str(self.closest_encounter) + " cet: " + str(self.closest_encounter_time)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_random():
        return Cpu(10 * random.random(),
                   2 * math.pi * random.random(),
                   10 * random.random())

    @staticmethod
    def init_population(size: int):
        return [Cpu.get_random() for i in range(size)]

    @staticmethod
    def evaluate(population):
        """
        For every phenotype in population simulate it and give score
        """
        for cpu in population:
            planets = [
                    Planet(50, 10, 0), # start planet
                    Planet(100, 20, math.pi/2),
                    ]
            satellite = Satellite(planets[0], cpu, planets[1])
            simulation = Simulation(planets=planets, satellite=satellite)
            simulation_time = 1000
            delta = 0.05
            for i in range(simulation_time):
                simulation.step(delta)
            cpu.score = satellite.get_score()
            cpu.closest_encounter = satellite.closest_encounter
            cpu.closest_encounter_time = satellite.closest_encounter_time

        population.sort(key = lambda c: c.score)
        return population

    @staticmethod
    def cross_over(population):
        p = population[0: len(population)//2]
        n = p[:]
        for i, cpu in enumerate(p):
            a = random.choice(p)
            b = random.choice(p)
            c = a.cross_over_other(b, 10 + math.exp(-i))
            n.append(c)
        return n



if __name__ == "__main__":
    n = Cpu.init_population(10)
    for i in range(1000):
        n = Cpu.evaluate(n)
        print(n[0])
        n = Cpu.cross_over(n)


