"""
simulation visualization using pygame
"""
import random

import pygame
import math

from math2d import Vector
from objects import Satellite, Planet, Cpu
from simulation import Simulation


def draw(screen, simulation: Simulation):
    for planet in simulation.planets:
        screen_position = planet.position + Vector(400, 300)
        pygame.draw.circle(screen, (255, 255, 255),
                           screen_position.get_int_tuple(), planet.mass)
    pygame.draw.circle(screen, (255, 255, 0),
                       (400, 300), 10)


pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

done = False

planets = []

for i in range(10):
    planets.append(Planet((i + 1) * 10, 1, 2 * random.random()))

satellite = Satellite(planets[0], Cpu(1, 2, 3))
simulation = Simulation(planets=planets, satellite=satellite)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    delta = clock.tick(60)
    simulation.step(delta * 0.01)
    draw(screen=screen, simulation=simulation)
    pygame.display.flip()
