"""
simulation visualization using pygame
"""
import json
import sys
import random

import pygame
import math
import argparse

from math2d import Vector
from objects import Satellite, Planet
from simulation import Simulation
from evolution import Cpu


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

parser = argparse.ArgumentParser(description='Simulation visualization')
parser.add_argument("-c", help="config file name", type=str, dest="config",
                    required=True)
parser.add_argument("--speed", type=float, required=True)
parser.add_argument("--angle", type=float, required=True)
parser.add_argument("--time", type=float, required=True)
args = parser.parse_args()

pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

done = False


(planets, start_planet, destination_planet, sun_mass) = Simulation.load_from_file(args.config)
time_factor = 0.001

satellite = Satellite(start_planet, Cpu(args.speed, args.angle, args.time), destination_planet)

simulation = Simulation(planets=planets, satellite=satellite, sun_mass=sun_mass)
total = 0

sat_p = []


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                time_factor += 0.0001
            elif event.key == pygame.K_DOWN:
                time_factor -= 0.0001
    screen.fill((0, 0, 0))
    pygame.transform.scale2x(screen)
    delta = clock.tick(60)
    total += delta*time_factor
    simulation.step(delta * time_factor)
    draw(screen=screen, simulation=simulation)
    font = pygame.font.Font(None, 36)
    label = font.render(str(total), 1, (255, 255, 0))
    screen.blit(label, (100, 100))
    label = font.render(str(time_factor), 1, (255, 255, 0))
    screen.blit(label, (100, 200))
    label = font.render(str("CE: " + str(satellite.closest_encounter)), 1, (255,255,0))
    screen.blit(label, (100, 300))
    label = font.render(("CET: " + str(satellite.closest_encounter_time)), 1, (255,255,0))
    screen.blit(label, (100, 400))
    screen_satellite_pos = satellite.position + Vector(400, 300)
    pygame.draw.line(screen, (0, 255, 0), screen_satellite_pos.get_int_tuple(), (satellite.velocity * 10 + screen_satellite_pos).get_int_tuple(), 2)
    pygame.draw.line(screen, (0, 255, 255), screen_satellite_pos.get_int_tuple(), (satellite.force * 100 + screen_satellite_pos).get_int_tuple(), 2)
    if len(sat_p) > 5000:
        sat_p.pop(0)
    sat_p.append(satellite.position + Vector(400, 300))
    if len(sat_p) >= 2:
        for i, p in enumerate(sat_p[0:-1]):
            pygame.draw.line(screen, (255, 100, 0), sat_p[i].get_int_tuple(), sat_p[i+1].get_int_tuple(), 2)
    try:
        pygame.draw.circle(screen, (255, 0, 0), (satellite.closest_encounter_position + Vector(400,300)).get_int_tuple(), 10)
    except:
        pass

    pygame.display.flip()
