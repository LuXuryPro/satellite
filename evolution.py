#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Evolution algorithm to evolve best initial state for satellite
"""
import math

import random


class Cpu:
    """
    This class describes satellite initial state
    """

    def __init__(self, speed: float, angle: float, time: int) -> None:
        self.speed = speed
        self.angle = angle
        self.time = time
        self.score = 10e10

    def __add__(self, other: 'Cpu'):
        speed = (self.speed + other.speed) / 2 + random.random()
        angle = (self.angle + other.angle) / 2 + random.random()
        time = (self.time + other.time) / 2 + random.random()
        return Cpu(speed, angle, time)

    @staticmethod
    def get_random():
        return Cpu(10 * random.random(),
                   2 * math.pi * random.random(),
                   10 * random.random())

    @staticmethod
    def init_population(size: int):
        population = []
        for i in range(size):
            population.append(Cpu.get_random())

    @staticmethod
    def evaluate(population):
        for cpu in population:
            pass

    @staticmethod
    def cross_over(population):
        for cpu in population:
            pass
