"""
simulation visualization using pygame
"""
import json
import sys
import random
import pygame
import math
import argparse

from pygame.locals import *


from math2d import Vector
from objects import Satellite, Planet
from simulation import Simulation
from evolution import Cpu



parser = argparse.ArgumentParser(description='Simulation visualization')
parser.add_argument("-c", help="config file name", type=str, dest="config",
                    required=True)
parser.add_argument("--speed", type=float, required=True)
parser.add_argument("--angle", type=float, required=True)
parser.add_argument("--time", type=float, required=True)
args = parser.parse_args()

pygame.init()
screen_width = 800
screen_height = 600
vector_mid = Vector(float(screen_width / 2.0), float(screen_height / 2.0))
screen = pygame.display.set_mode((screen_width, screen_height), HWSURFACE|DOUBLEBUF|RESIZABLE)

clock = pygame.time.Clock()

done = False


(planets, start_planet, destination_planet, sun_mass) = Simulation.load_from_file(args.config)
time_factor = 0.001
cpu = Cpu(args.speed, args.angle, args.time)

satellite = Satellite(start_planet,
        cpu,
        destination_planet)

simulation = Simulation(planets=planets, satellite=satellite, sun_mass=sun_mass)

def draw(screen: pygame.Surface, simulation: Simulation):
    for planet in simulation.planets:
        screen_position = planet.position + vector_mid
        pygame.draw.circle(screen, (255, 255, 255),
                           screen_position.get_int_tuple(), planet.mass)
        planet_screen_pos = planet.position + vector_mid
        if planet == start_planet:
            font = pygame.font.Font(None, 36)
            label = font.render("Start", 1, (255,255, 255))
            screen.blit(label, (planet_screen_pos.x, planet_screen_pos.y))
        elif planet == destination_planet:
            font = pygame.font.Font(None, 36)
            label = font.render("Destination", 1, (255,255, 255))
            screen.blit(label, (planet_screen_pos.x, planet_screen_pos.y))
    pygame.draw.circle(screen, (255, 255, 0),
                       vector_mid.get_int_tuple(), 10)

    satellite_screen_pos = simulation.satellite.position + vector_mid
    rect = (satellite_screen_pos.x - 2, satellite_screen_pos.y - 2, 4, 4)
    pygame.draw.rect(screen, (0, 0, 255), rect)

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
        elif event.type==VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'],
                    HWSURFACE|DOUBLEBUF|RESIZABLE)
            screen_width = event.dict['size'][0]
            screen_height = event.dict['size'][1]
            vector_mid = Vector(float(screen_width / 2.0), float(screen_height / 2.0))
    screen.fill((0, 0, 0))
    delta = clock.tick(60)
    total += delta * time_factor
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
    screen_satellite_pos = satellite.position + vector_mid
    pygame.draw.line(screen, (0, 255, 0), screen_satellite_pos.get_int_tuple(), (satellite.velocity * 10 + screen_satellite_pos).get_int_tuple(), 2)
    pygame.draw.line(screen, (0, 255, 255), screen_satellite_pos.get_int_tuple(), (satellite.force * 100 + screen_satellite_pos).get_int_tuple(), 2)
    pygame.draw.line(screen, (255, 0, 255),
            screen_satellite_pos.get_int_tuple(), (cpu.get_velocity_vector() * 100 + screen_satellite_pos).get_int_tuple(), 2)
    if len(sat_p) > 5000:
        sat_p.pop(0)
    sat_p.append(satellite.position.clone())
    try:
        pygame.draw.circle(screen, (255, 0, 0), (satellite.closest_encounter_position + vector_mid).get_int_tuple(), 10)
    except:
        pass
    if len(sat_p) >= 2:
        pygame.draw.lines(screen, (255, 100, 0), False, list(map(lambda x: (x + vector_mid).get_int_tuple(), sat_p)), 2)
    pygame.display.flip()
