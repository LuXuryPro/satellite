from multiprocessing import Pool
from objects import Satellite
from simulation import Simulation


def one_satellite(cpu):
    (planets, start_planet, destination_planet, sun_mass) = Simulation.load_from_file("config.json")
    satellite = Satellite(start_planet, cpu, destination_planet)
    simulation = Simulation(planets=planets, satellite=satellite,
                            sun_mass=sun_mass)
    simulation_time = 1000
    delta = 0.06
    for i in range(simulation_time):
        simulation.step(delta)
    cpu.score = satellite.get_score()
    cpu.closest_encounter = satellite.closest_encounter
    cpu.closest_encounter_time = satellite.closest_encounter_time
    return cpu

def process_parallel(population, args):
    with Pool(4) as p:
        return p.map(one_satellite, population)

if __name__ == "__main__":
    from evolution import Cpu
    population = Cpu.init_population(10)
    population = process_parallel(population)
    population.sort(key = lambda c: c.score)


