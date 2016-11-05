#!/usr/bin/env python
# -*- coding: utf-8 -*-
from evolution import Cpu
from math2d import Vector
import math


class Planet:
    def __init__(self, distance_to_sun=1, mass=1, initial_angle=0):
        self.distance_to_sun = distance_to_sun
        self.mass = mass
        self.initial_angle = initial_angle
        self.angle = initial_angle
        self.angular_velocity = math.sqrt(2 / self.distance_to_sun)
        self.position = Vector()
        self.position.x = self.distance_to_sun * math.cos(self.angle)
        self.position.y = self.distance_to_sun * math.sin(self.angle)
        self.velocity = Vector()  # linear velocity

    def step(self, dt: float):
        # angular_velocity in constant over time
        self.angle += self.angular_velocity * dt
        self.position.x = self.distance_to_sun * math.cos(self.angle)
        self.position.y = self.distance_to_sun * math.sin(self.angle)
        velocity = self.angular_velocity * self.distance_to_sun
        velocity_angle = self.angle + math.pi / 2
        velocity_normal_vector = Vector(math.cos(velocity_angle),
                                        math.sin(velocity_angle))
        self.velocity = velocity_normal_vector * velocity




class Satellite:
    def __init__(self, start_planet: Planet, cpu: Cpu, destination_planet: Planet):
        self.start_planet = start_planet
        self.destination_planet = destination_planet
        self.cpu = cpu
        self.velocity = Vector()
        self.position = Vector()
        self.mass = 1  # mass can be small
        self.force = Vector()
        self.cut_down = self.cpu.time
        self.fly = False
        self.position = self.start_planet.position + Vector(0, 5)
        self.velocity = self.start_planet.velocity
        self.fly_time = 0
        self.closest_encounter = 10e10

    def launch(self):
        self.fly = True
        self.velocity = self.velocity + Vector(math.cos(self.cpu.angle),
                                               math.sin(
                                                   self.cpu.angle)) * self.cpu.speed

    def set_force(self, force: Vector):
        self.force = force

    def step(self, dt: float):
        if not self.fly:
            self.position = self.start_planet.position + Vector(0, 5)
            self.velocity = self.start_planet.velocity
            self.cut_down -= dt
            if self.cut_down > 0:
                return
            else:
                self.launch()
        dv = self.force * dt
        self.velocity += dv
        dp = self.velocity * dt
        self.position += dp
        self.update_stats(dt)

    def update_stats(self, dt):
        self.fly_time += dt
        distance_to_destination = self.position.distance(self.destination_planet.position)
        if (distance_to_destination < self.closest_encounter):
            self.closest_encounter = distance_to_destination

    def get_score(self):
        return self.closest_encounter + self.fly_time
