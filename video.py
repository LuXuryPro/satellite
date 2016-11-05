"""
simulation visualization using pygame
"""
import random

import pygame
import math

from math2d import Vector
from objects import Satellite, Planet, Cpu
from simulation import Simulation


def draw(screen: pygame.Surface, simulation: Simulation):
    for planet in simulation.planets:
        screen_position = planet.position + Vector(400, 300)
        pygame.draw.circle(screen, (255, 255, 255),
                           screen_position.get_int_tuple(), planet.mass)
    pygame.draw.circle(screen, (255, 255, 0),
                       (400, 300), 10)

    satellite_screen_pos = simulation.satellite.position + Vector(400, 300)
    rect = (satellite_screen_pos.x - 2, satellite_screen_pos.y - 2, 4, 4)
    pygame.draw.rect(screen, (0, 0, 255), rect)


pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

done = False

planets = []

for i in range(10):
    planets.append(Planet((i + 1) * 40, 10, 2 * random.random()))

satellite = Satellite(planets[0], Cpu(20, 2, 5))
simulation = Simulation(planets=planets, satellite=satellite)
total = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    pygame.transform.scale2x(screen)
    delta = clock.tick(60)
    total += delta
    simulation.step(delta * 0.01)
    draw(screen=screen, simulation=simulation)
    font = pygame.font.Font(None, 36)
    label = font.render(str(total), 1, (255,255,0))
    screen.blit(label, (100, 100))
    label = font.render(str(satellite.velocity.length()), 1, (255,255,0))
    screen.blit(label, (200, 100))
    label = font.render(str(satellite.force.length()), 1, (255,255,0))
    screen.blit(label, (100, 200))
    screen_satelite_pos = satellite.position + Vector(400, 300)
    pygame.draw.line(screen, (0,255,0), screen_satelite_pos.get_int_tuple(), (satellite.velocity * 10 + screen_satelite_pos).get_int_tuple(), 2)
    pygame.draw.line(screen, (0,255,255), screen_satelite_pos.get_int_tuple(), (satellite.force * 100 + screen_satelite_pos).get_int_tuple(), 2)
    pygame.display.flip()
