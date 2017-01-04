#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Evolution algorithm to evolve best initial state for satellite

Function to minimize

f() = satelite_fly_time + satelite_closest_approach
"""
import math
import json

from parallel_processing import process_parallel
from math2d import Vector
import random
from objects import Planet
from objects import Satellite
from simulation import Simulation
import sys
from operator import attrgetter
import argparse
import time

args = None



def timeit(func):
    def newfunc(*args, **kwargs):
        startTime = time.time()
        result =  func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
        return result
    return newfunc

class Cpu:
    """
    This class describes satellite initial state
    """

    def __init__(self, speed: float, angle: float, time: int) -> None:
        self.speed = speed
        self.normalize_speed()
        self.angle = angle % (2 * math.pi)
        self.normalize_angle()
        self.time = time
        self.normalize_time()
        self.score = 10e10
        self.closest_encounter = 0
        self.closest_encounter_time = 0

    def clone(self):
        c = Cpu(self.speed, self.angle, self.time)
        c.score = self.score
        c.closest_encounter = self.closest_encounter
        c.closest_encounter_time = self.closest_encounter_time
        return c

    def normalize_speed(self):
        self.speed = abs(self.speed)

    def normalize_angle(self):
        self.angle = self.angle % (2 * math.pi)
        if self.angle < 0.0:
            self.angle = 2 * math.pi + self.angle

    def normalize_time(self):
        if self.time < 0:
            self.time = 0

    def cross_over_other(self, other: 'Cpu'):
        ratio = random.random()
        speed = ratio * self.speed + (1 - ratio) * other.speed
        self.normalize_speed()
        ratio = random.random()
        angle = ratio * self.angle + (1 - ratio) * other.angle
        self.normalize_angle()
        ratio = random.random()
        time = ratio * self.time + (1 - ratio) * other.time
        self.normalize_time()
        return Cpu(speed, angle, time)


    def mutate(self, power):
        self.speed = self.speed  + (- power  + 2 * power * random.random())
        self.normalize_speed()
        self.angle = self.angle + (- 2 * math.pi * power  + 2 * 2 * math.pi * power * random.random())
        self.normalize_angle()
        self.time = self.time + (- power  + 2 * power * random.random())
        self.normalize_time()

    def get_velocity_vector(self):
        return Vector(math.cos(self.angle),
                      math.sin(self.angle)) * self.speed


    def __str__(self):
        return str(self.score) + " speed: " + str(self.speed) + " angle: " + str(self.angle) + " time: " + str(self.time) + " ce: " + str(self.closest_encounter) + " cet: " + str(self.closest_encounter_time)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_random():
        return Cpu(100 * random.random(),
                   2 * math.pi * random.random(),
                   50 * random.random())

    @staticmethod
    @timeit
    def init_population(size: int):
        return [Cpu.get_random() for i in range(size)]

    @staticmethod
    @timeit
    def evaluate(population):
        """
        For every phenotype in population simulate it and give score
        """

        population = process_parallel(population, args)
        population.sort(key = lambda c: c.score)
        return population

    @staticmethod
    def turnament_selection(population, size_of_turnament, p):
        """
        p - probability of picking best one from turnament
        """
        turnament = [
                random.choice(population) for i in range(size_of_turnament)]
        return min(turnament, key=attrgetter('score'))

    @staticmethod
    @timeit
    def cross_over(population, i, size):
        n = []
        while len(n) < (size >> 1):
            sys.stdout.write('\r')
            sys.stdout.write('[')
            sys.stdout.write('='*len(n) + " "*(size - len(n)) + "]")
            size_of_turnament = args.t
            a = Cpu.turnament_selection(population, size_of_turnament, 0.8)
            b = Cpu.turnament_selection(population, size_of_turnament, 0.8)
            c = a.cross_over_other(b)
            if args.ma:
                c.mutate(args.m / (1 + i))
            else:
                c.mutate(args.m)
            n.append(c)

        print('')
        return n

    @staticmethod
    @timeit
    def union(parents, children, final_size):
        u = parents + children
        u.sort(key = lambda c: c.score)
        return u[:final_size - 1]


    @staticmethod
    @timeit
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
    parser.add_argument("-g", help="number of generations", type=int, required=True)
    parser.add_argument("-n", help="size of population", type=int, required=True)
    parser.add_argument("-t", help="turnament size", type=int, required=True)
    parser.add_argument("-m", help="mutation strenght", type=float, required=False, default=1.0)
    parser.add_argument("-f", help="ouput file name", type=str)
    parser.add_argument("--hist", help="draw histogram", action="store_true", default=False)
    parser.add_argument("--log", help="prepare scatter log", action="store_true", default=False)
    parser.add_argument("--annealing" ,"-ma", help="enable mutation strenght annealing", action="store_true", default=False, dest="ma")
    args = parser.parse_args()
    timestamp = str(int(time.time()))
    with open(args.f or timestamp, "a") as f:
        f.write("#" + str(args) + "\n")
    population = Cpu.init_population(args.n)
    population = Cpu.evaluate(population)
    for i in range(args.g):
        if args.hist:
            if i == 0 or i == args.g >> 9 or i == args.g >> 8 or i == args.g >> 7 or i == args.g >> 6 or i == args.g >> 5 or i == args.g >> 4 or i == args.g >> 3 or i == args.g >> 2 or i == args.g >> 1 or i == args.g - 1:
                with open(args.f or timestamp + "hist" + str(i), "a") as f:
                    for p in population:
                        f.write("{fitenss}\n".format(fitenss=p.score))
                #Cpu.histogram(population)
        print("Generation no. " + str(i))
        print(population[0])
        with open(args.f or timestamp, "a") as f:
            f.write("{best} {avg} {worst} {ce}\n".format(ce=population[0].closest_encounter,
                avg=(sum([x.score for x in population])/len(population)),
                worst=population[-1].score,
                best=population[0].score))
        if args.log:
            with open(args.f or timestamp + "scatter", "a") as f:
                for p in population:
                    f.write("{speed} {angle} {time}\n".format(
                        speed=p.speed, angle=p.angle, time=p.time))
        print(sum([x.score for x in population])/len(population))
        print(population[-1])
        children = Cpu.cross_over(population, i, args.n)
        children = Cpu.evaluate(children)
        population = Cpu.union(population, children, args.n)


