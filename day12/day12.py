import math
import itertools
import re

class Moon:

    def __init__(self, starting_pos, starting_vel):
        self.starting_pos = starting_pos
        self.starting_vel = starting_vel
        self.pos = self.starting_pos[:]
        self.vel = self.starting_vel[:]
        self.acceleration = [0,0,0]

    def step(self):
        for i in range(3):
            self.pos[i] += self.vel[i]
        
    def get_total_energy(self):
        return self.get_potential_energy()*self.get_kinetic_energy()

    def get_kinetic_energy(self):
        return sum(abs(x) for x in self.vel)

    def get_potential_energy(self):
        return sum(abs(x) for x in self.pos)
        
    def print_moon(self):
        print("Pos:", self.pos, "Vel: ", self.vel)

def apply_gravity(moons):
    for pair in itertools.combinations(moons, 2):
        for i in range(3):
            if pair[0].pos[i] < pair[1].pos[i]:
                pair[0].vel[i] += 1
                pair[1].vel[i] += -1
            elif pair[1].pos[i] < pair[0].pos[i]:
                pair[1].vel[i] += 1
                pair[0].vel[i] += -1
        

def all_step(moons):
    apply_gravity(moons)
    for moon in moons:
        moon.step()


def build_state_for_axis(moons, axis):
    data = []
    for moon in moons:
        data += [moon.pos[axis]]
        data += [moon.vel[axis]]
    return tuple(data)


def steps_to_repeat(moons, axis):
    steps = 0 
    first_state = build_state_for_axis(moons, axis)
    while True:
        all_step(moons)
        steps += 1
        if build_state_for_axis(moons, axis) == first_state:
            break

    return steps


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

# IO 
moons_starting = [Moon(list(map(int, re.findall(r"-?\d+", line))), [0,0,0]) for line in open("input.txt").readlines()]

# 1st
moons = moons_starting[:]
for _ in range(1000):
    all_step(moons)
print(sum(moon.get_total_energy() for moon in moons))

# 2nd
steps = [steps_to_repeat(moons_starting[:], axis) for axis in range(3)]
print(lcm(lcm(steps[0], steps[1]), steps[2]))
