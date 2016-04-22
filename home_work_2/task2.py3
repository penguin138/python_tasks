#! /usr/bin/env python3
import random
import os
import time


class Ocean_object(object):
    def get_type():
        raise NotImplementedError()


class Fish(Ocean_object):

    def __init__(self, i, j, ocean, breeding_interval, life_time=-1):
        self.i = i
        self.j = j
        self.last_meal_time = ocean.current_iteration
        self.ocean = ocean
        self.get_neighbors()
        self.life_time = life_time
        self.breeding_interval = breeding_interval

    def get_neighbors(self):
        self.free_neighbors = []
        self.prey_neighbors = []
        for delta_x in [-1, 0, 1]:
            for delta_y in [-1, 0, 1]:
                neighbor_type = self.ocean.get_object_type(self.i + delta_x,
                                                           self.j + delta_y)
                if (neighbor_type == self.ocean.EMPTY):
                    self.free_neighbors.append((self.i + delta_x, self.j +
                                                delta_y))
                elif neighbor_type == self.ocean.PREY:
                    self.prey_neighbors.append((self.i + delta_x, self.j +
                                                delta_y))

    def move(self):
        raise NotImplementedError()

    def breed(self):
        raise NotImplementedError()

    def die(self):
        self.ocean.remove_fish(self.i, self.j)


class Predator(Fish):
    def move(self):
        if ((self.ocean.current_iteration - self.last_meal_time) >
                self.life_time):
            self.die()
            return
        self.get_neighbors()
        if (self.ocean.current_iteration % self.breeding_interval == 0 and
                len(self.free_neighbors) > 0):
            self.breed()
        else:
            # eat = random.choice([True, False]) - capricious predator
            eat = True
            if eat and len(self.prey_neighbors) > 0:
                self.last_meal_time = self.ocean.current_iteration
                prey_to_eat = random.choice(self.prey_neighbors)
                self.ocean.objects[prey_to_eat].die()
            elif len(self.free_neighbors) > 0:
                new_place = random.choice(self.free_neighbors)
                self.ocean.relocate(self.i, self.j, new_place[0], new_place[1])
                self.i = new_place[0]
                self.j = new_place[1]

    def breed(self):
        place_for_newborn = random.choice(self.free_neighbors)
        new_predator = Predator(place_for_newborn[0], place_for_newborn[1],
                                self.ocean, self.breeding_interval,
                                self.life_time)
        self.ocean.create_fish(place_for_newborn, new_predator)

    def __str__(self):
        return '@'

    def get_type(self):
        return self.ocean.PREDATOR


class Prey(Fish):
    def move(self):
        self.get_neighbors()
        if (self.ocean.current_iteration % self.breeding_interval == 0 and
                len(self.free_neighbors) > 0):
            self.breed()
        elif len(self.free_neighbors) > 0:
            new_place = random.choice(self.free_neighbors)
            self.ocean.relocate(self.i, self.j, new_place[0], new_place[1])
            self.i = new_place[0]
            self.j = new_place[1]

    def breed(self):
        place_for_newborn = random.choice(self.free_neighbors)
        new_prey = Prey(place_for_newborn[0], place_for_newborn[1],
                        self.ocean, self.breeding_interval)
        self.ocean.create_fish(place_for_newborn, new_prey)

    def __str__(self):
        return '*'

    def get_type(self):
        return self.ocean.PREY


class Block(Ocean_object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return '#'

    def get_type(self):
        return self.type


class Ocean(object):
    EMPTY = 0
    PREDATOR = 1
    PREY = 2
    BLOCK = 3
    MAX_DRAWING_SIZE = 20

    def __init__(self, filename="ocean.txt", width=-1, height=-1,
                 distribution=[0.25, 0.25, 0.25, 0.25], predator_life_time=3,
                 prey_breeding_interval=1, predator_breeding_interval=5):
        ocean_mask = []
        if (width > 0 and height > 0):
            ocean_mask = self._generate_ocean(width, height, distribution)
        else:
            ocean_mask = self._read_ocean(filename)
        self.current_iteration = 0
        self.height = len(ocean_mask)
        self.width = 0
        if (self.height > 0):
            self.width = len(ocean_mask[0])
        self.num_of_predators = 0
        self.num_of_preys = 0
        self.predator_life_time = predator_life_time
        self.prey_breeding_interval = prey_breeding_interval
        self.predator_breeding_interval = predator_breeding_interval
        self.create_objects(ocean_mask)

    def _read_ocean(self, filename):
        new_ocean = []
        with open(filename, 'r') as ocean_file:
            line_counter = 0
            for line in ocean_file:
                ocean_line = []
                line_symbols = line.split()
                for j in range(len(line_symbols)):
                    symbol = line_symbols[j]
                    ocean_line.append(int(symbol))
                new_ocean.append(ocean_line)
                line_counter += 1
            return new_ocean

    def _generate_ocean(self, width, height, distribution):
        new_ocean = []
        objects = [self.EMPTY, self.BLOCK, self.PREDATOR, self.PREY]
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(self._get_random_object(objects, distribution))
            new_ocean.append(new_line)
        return new_ocean

    def _get_random_object(self, objects, distribution):
        num_of_objects = len(objects)
        if len(distribution) != num_of_objects:
            raise ValueError("""Distribution should consist of {}
                             probabilities - one for each object type""".
                             format(num_of_objects))
        elif sum(distribution) != 1:
            raise ValueError("Sum of p_i should be equal 1")
        random_number = random.random()
        left_sum = 0
        right_sum = 0
        for i in range(num_of_objects):
            right_sum += distribution[i]
            if (random_number >= left_sum and random_number < right_sum):
                return objects[i]
            left_sum = right_sum

    def create_objects(self, ocean_mask):
        self.objects = {}
        for i in range(self.height):
            for j in range(self.width):
                obj = ocean_mask[i][j]
                if obj == self.PREDATOR:
                    predator = Predator(i, j, self,
                                        self.predator_breeding_interval,
                                        self.predator_life_time)
                    self.objects[(i, j)] = predator
                    self.num_of_predators += 1
                elif obj == self.PREY:
                    prey = Prey(i, j, self, self.prey_breeding_interval)
                    self.objects[(i, j)] = prey
                    self.num_of_preys += 1
                elif obj == self.BLOCK:
                    block = Block(self.BLOCK)
                    self.objects[(i, j)] = block

    def draw_ocean(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.objects:
                    print(self.objects[(i, j)], end=' ')
                else:
                    print(' ', end=' ')
            print('\n')
        print('num_of_iterations: {}'.format(self.current_iteration))
        print('num_of_predators: {}'.format(self.num_of_predators))
        print('num_of_preys: {}'.format(self.num_of_preys))

    def get_object_type(self, i, j):
        if i >= self.height or i < 0 or j >= self.width or j < 0:
            return self.BLOCK
        if (i, j) in self.objects:
            return self.objects[(i, j)].get_type()
        else:
            return self.EMPTY

    def remove_fish(self, i, j):
        if (i, j) in self.objects:
            fish_type = self.objects[(i, j)].get_type()
            if fish_type == self.PREDATOR:
                self.num_of_predators -= 1
            elif fish_type == self.PREY:
                self.num_of_preys -= 1
            else:
                raise ValueError("There is no fish!")
            self.objects.pop((i, j))

    def relocate(self, old_i, old_j, new_i, new_j):
        fish = self.objects[(old_i, old_j)]
        fish_type = fish.get_type()
        if fish_type not in [self.PREDATOR, self.PREY]:
            raise ValueError("Can't relocate: not a fish.")
        self.objects.pop((old_i, old_j))
        self.objects[(new_i, new_j)] = fish

    def create_fish(self, new_location, new_fish):
        self.objects[new_location] = new_fish
        fish_type = new_fish.get_type()
        if fish_type == self.PREDATOR:
            self.num_of_predators += 1
        elif fish_type == self.PREY:
            self.num_of_preys += 1

    def run_simulation(self, num_of_iterations=100, report_file="report.csv",
                       draw=True, log=True):
        if (self.width > self.MAX_DRAWING_SIZE or
                self.height > self.MAX_DRAWING_SIZE):
            draw = False
        if log:
            report = open(report_file, 'w')
            report.write("current_iteration num_of_predators num_of_preys\n")
        while (self.current_iteration < num_of_iterations and
               self.num_of_predators > 0 and self.num_of_preys > 0):
            for object_key in list(self.objects.keys()):
                if object_key in self.objects:
                    obj = self.objects[object_key]
                    if obj.get_type() in [self.PREDATOR, self.PREY]:
                        obj.move()
            self.current_iteration += 1
            if (draw):
                time.sleep(0.1)
                os.system('clear')
                self.draw_ocean()
            if (log):
                report.write("{0} {1} {2}\n".format(self.current_iteration,
                                                    self.num_of_predators,
                                                    self.num_of_preys))
        if log:
            report.close()

ocean = Ocean(width=20, height=20)
# num_of_iterations = int(input())
ocean.run_simulation(1, draw=False, log=False)
