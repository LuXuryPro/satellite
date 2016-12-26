"""
simulation visualization using pygame
"""
import json
import sys
import random

import pygame
import math

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


pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

done = False

# try:
#     with open('simulation.json') as data_file:
#         data = json.load(data_file)
#
# except FileNotFoundError:
#     print("File simulation.json was not found. Please provide it using readme as guide.")
#     sys.exit(0)
# except Exception:
#     print("Your simulation.json is not valid. Please check readme for examples.")
#     sys.exit(0)
#
# planetsJSON = data["simulation"]["planets"]
# planets = []
#
# for i in range(len(planetsJSON)):
#     planetJSON = planetsJSON[i]
#     planets.append(Planet(int(planetJSON["distance-to-sun"]), int(planetJSON["mass"]),
#                           float(planetJSON["start-angle"])))
#
# start_planet = planets[int(data["simulation"]["start-planet"])]
# destination_planet = planets[int(data["simulation"]["destination-planet"])]

(planets, start_planet, destination_planet) = Simulation.load_from_file()
time_factor = 0.001

satellite = Satellite(start_planet, Cpu(0.1036, 1.12345, 7.679484), destination_planet)

simulation = Simulation(planets=planets, satellite=satellite)
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
    label = font.render(str(total), 1, (255,255,0))
    screen.blit(label, (100, 100))
    label = font.render(str(time_factor), 1, (255,255,0))
    screen.blit(label, (100, 200))
    label = font.render(str(satellite.closest_encounter), 1, (255,255,0))
    screen.blit(label, (100, 300))
    label = font.render(str(satellite.closest_encounter_time), 1, (255,255,0))
    screen.blit(label, (100, 400))
    screen_satelite_pos = satellite.position + Vector(400, 300)
    pygame.draw.line(screen, (0,255,0), screen_satelite_pos.get_int_tuple(), (satellite.velocity * 10 + screen_satelite_pos).get_int_tuple(), 2)
    pygame.draw.line(screen, (0,255,255), screen_satelite_pos.get_int_tuple(), (satellite.force * 100 + screen_satelite_pos).get_int_tuple(), 2)
    if (len(sat_p) > 500):
        sat_p.pop(0)
    sat_p.append(satellite.position + Vector(400,300))
    if len(sat_p) >= 2:
        for i, p in enumerate(sat_p[0:-1]):
            pygame.draw.line(screen, (255,100,0), sat_p[i].get_int_tuple(), sat_p[i+1].get_int_tuple(), 2)
    try:
        pygame.draw.circle(screen, (255, 0, 0), (satellite.closest_encounter_position + Vector(400,300)).get_int_tuple(), 10)
    except:
        pass

    pygame.display.flip()
