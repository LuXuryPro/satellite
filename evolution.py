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
import sys
from operator import attrgetter
import argparse
import ipdb


planets = None
start_planet = None
destination_planet = None
sun_mass = None



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

    def cross_over_other(self, other: 'Cpu'):
        speed = (self.speed + other.speed) / 2
        angle = (self.angle + other.angle) / 2
        time = (self.time + other.time) / 2
        return Cpu(speed, angle, time)

    def mutate(self, power):
        self.speed = self.speed  + (- power  + 2 * power * random.random())
        self.angle = self.angle + (- power  + 2 * power * random.random())
        self.time = self.time + (- power  + 2 * power * random.random())
        if self.time < 0:
            self.time = 0


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
            satellite = Satellite(start_planet, cpu, destination_planet)
            simulation = Simulation(planets=planets, satellite=satellite,
                                    sun_mass=sun_mass)
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
    def cross_over(population, i):
        start_len = len(population)
        p = population
        n = []
        n.append(p[0])
        s = int(0.1 * len(population))
        mt = 0.1
        while len(n) < start_len:
            sys.stdout.write('\r')
            sys.stdout.write('[')
            sys.stdout.write('='*len(n) + " "*(start_len - len(n)) + "]")
            sh = [random.choice(p) for x in range(s)]
            a = min(sh, key=attrgetter('score'))
            sh = [random.choice(p) for x in range(s)]
            b = min(sh, key=attrgetter('score'))
            c = a.cross_over_other(b)
            c.mutate(mt)
            k = Cpu.evaluate([c])
            c = k[0]
            if c.score < a.score and c.score < b.score or mt > 1:
                mt = 0.1
                n.append(c)
            else:
                mt += 0.1

        n.sort(key = lambda c: c.score)
        print('')
        return n

    @staticmethod
    def histogram(population):
        hist_x = len(population)
        hist_y = 30

        for y in range(hist_y):
            for x in range(hist_x):
                value = population[(len(population) * x) // hist_x].score
                value = hist_y * (value / max([z.score for z in population]))
                if value >= hist_y - y:
                    print ("+", end="")
                else:
                    print (" ", end="")
            print("\n", end="")






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulation visualization')
    parser.add_argument("-c", help="config file name", type=str, dest="config",
                        required=True)
    parser.add_argument("-g", type=int, required=True)
    parser.add_argument("-n", type=int, required=True)
    args = parser.parse_args()
    (planets, start_planet, destination_planet, sun_mass) = Simulation.load_from_file(args.config)
    n = Cpu.init_population(args.n)
    n = Cpu.evaluate(n)
    for i in range(args.g):
        Cpu.histogram(n)
        print(n[0])
        print (sum([x.score for x in n])/len(n))
        print(n[-1])
        n = Cpu.cross_over(n, i)


