global terminal
global PRETTY
global FPS

# If you have asciimatics installed, you can set PRETTY to True to turn on the ascii graphics
PRETTY = False
FPS = 360
terminal = None

if PRETTY:
    from asciimatics.screen import Screen, ManagedScreen
    from time import sleep

class Opcodes(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return Opcodes(list.__getitem__(self, index))

        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        return list.__getitem__(self, index)

class Param:
    def __init__(self, val, mode):
        self.val = val
        self.mode = mode

    def get_input_val(self, intcode):
        if self.mode == 0:
            return intcode.opcodes[self.val]
        elif self.mode == 1:
            return self.val
        
        return intcode.opcodes[intcode.rel_base+self.val]

    def get_output_val(self, intcode):
        if self.mode == 0:
            return self.val
        elif self.mode == 1:
            return self.val
        
        return intcode.rel_base+self.val
        


class Instruction:
    
    def __init__(self, opcode, n_params, fun, modifies_address=False):
        self.opcode = opcode
        self.n_params = n_params
        self.fun = fun
        self.modifies_address = modifies_address

    def __call__(self, *args):
        return self.fun(*args)


class Intcode:
    
    def __init__(self, opcodes, instructions, input_values):
        self.starting_values = opcodes[:]
        self.instructions = instructions        
        self.input_values = input_values[::-1]
        self.output_values = []
        self.opcodes = self.starting_values[:]
        self.pos = 0
        self.rel_base = 0
        self.halted = False

    def reset(self):
        self.opcodes = self.starting_values[:]
        self.pos = 0

    def send_input(self, val):
        self.input_values.insert(0, val)

    def run_all(self):
        while True:
            ret_val = self.run()
            if ret_val == 1:
                self.halted = True
                return None
            elif ret_val == 2:
                return None
            elif ret_val == 3:
                return self.output_values.pop()

    def run(self):
        # Read
        val = self.opcodes[self.pos]

        # Decode
        op = val%100
        instruction = self.instructions[op]
        modes = list(map(int, str(val//100).zfill(3)[::-1]))

        # Execute
        params = [Param(val, mode) for val, mode in zip(self.opcodes[self.pos+1:self.pos+1+instruction.n_params], modes)]
        ret_val = instruction(self, *params)

        if not instruction.modifies_address:
            self.pos += 1+instruction.n_params
        
        return ret_val


class Maze:

    def __init__(self, screen, intcode):
        self.screen = screen
        self.intcode = intcode
        self.x = len(screen[0]) // 2
        self.y = len(screen) // 2
        self.starting_pos = self.y, self.x
        self.screen[self.y][self.x] = 2
        self.oxygen_pos = None
        self.visited = set()
        self.bad_paths = set()
        self.dirs = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}
        self.reverse_move = {1:2, 2:1, 3:4, 4:3}
        self.flood_step = -1
        self.flooded_start_pos_step = 0

    def try_move(self, direction):
        self.intcode.send_input(direction)
        status = self.intcode.run_all()
        vect = self.dirs[direction]
        dest = self.y+vect[0], self.x+vect[1]
        if status == 2:
            self.oxygen_pos = dest
        if status != 0:
            self.screen[dest[0]][dest[1]] = 4
            self.intcode.send_input(self.reverse_move[direction])
            self.intcode.run_all()
            return True, dest
        self.screen[dest[0]][dest[1]] = 1
        return False, dest


    def probe_near(self):
        movable = set()
        for d in self.dirs:
            move, dest = self.try_move(d)
            if move:
                movable.add((d, dest))
        return movable

    def move(self, direction):
        self.visited.add((self.y, self.x))
        self.intcode.send_input(direction[0])
        self.intcode.run_all()
        self.screen[self.y][self.x] = 4
        self.x = direction[1][1]
        self.y = direction[1][0]
        self.screen[self.y][self.x] = 2

    def traverse(self):
        while True:
            self.render_screen()
            possible_moves = set(x for x in self.probe_near() if x[1] not in self.bad_paths)
            if not len(possible_moves):
                return
            if len(possible_moves) == 1:
                self.bad_paths.add((self.y, self.x))
            best_moves = set(x for x in possible_moves if x[1] not in self.visited)
            if len(best_moves):
                possible_moves = best_moves
            self.move(list(possible_moves)[0])

    def flood_cycle(self, places_to_flood):
        new_places_to_flood = []
        self.render_screen()
        while len(places_to_flood):
            place = places_to_flood.pop()
            new_places = self.flood(*place)
            new_places_to_flood.extend(new_places)
        return new_places_to_flood

    def get_neighbours(self, y, x):
        return [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]

    def flood(self, y, x):
        if self.screen[y][x] != 4:
            return []
        self.screen[y][x] = 3
        if (y, x) == self.starting_pos:
            self.flooded_start_pos_step = self.flood_step
        return self.get_neighbours(y, x)

    def flood_from_oxygen(self):
        to_flood = self.get_neighbours(*self.oxygen_pos)
        self.flood_step = -1
        while len(to_flood):
            to_flood = self.flood_cycle(to_flood)
            self.flood_step += 1


    def render_screen(self):
        global PRETTY
        if not PRETTY:
            return
        global terminal
        global FPS
        tiles = {0:'.', 1:'#', 2:'X', 3:'O', 4:' '}
        if self.oxygen_pos is not None:
            self.screen[self.oxygen_pos[0]][self.oxygen_pos[1]] = 3
        for i, row in enumerate(self.screen):
            s = ""
            for char in row:
                s += tiles[char]
            terminal.print_at(s, 0, i)
        terminal.refresh()
        sleep(1/FPS)


# IO
opcodes = Opcodes(map(int, open("input.txt").read().split(",")))

# Config
def add(intcode, in1, in2, out1):
    intcode.opcodes[out1.get_output_val(intcode)] = in1.get_input_val(intcode) + in2.get_input_val(intcode)

def mult(intcode, in1, in2, out1):
    intcode.opcodes[out1.get_output_val(intcode)] = in1.get_input_val(intcode) * in2.get_input_val(intcode)

def rd(intcode, dest):
    if intcode.input_values:
        val = intcode.input_values.pop()
        intcode.opcodes[dest.get_output_val(intcode)] = val
    else:
        return 2

def wt(intcode, source):
    intcode.output_values.insert(0, source.get_input_val(intcode))
    return 3

def je(intcode, in1, in2):
    val = in1.get_input_val(intcode)
    if val != 0:
        intcode.pos = in2.get_input_val(intcode)
    else:
        intcode.pos += 3

def jne(intcode, in1, in2):
    val = in1.get_input_val(intcode)
    if val == 0:
        intcode.pos = in2.get_input_val(intcode)
    else:
        intcode.pos += 3

def le(intcode, in1, in2, dest):
    val1 = in1.get_input_val(intcode)
    val2 = in2.get_input_val(intcode)
    intcode.opcodes[dest.get_output_val(intcode)] = int(val1 < val2)

def eq(intcode, in1, in2, dest):
    val1 = in1.get_input_val(intcode)
    val2 = in2.get_input_val(intcode)
    intcode.opcodes[dest.get_output_val(intcode)] = int(val1 == val2)

def rel(intcode, in1):
    intcode.rel_base += in1.get_input_val(intcode)


instruction_list = [
    Instruction(1, 3, add),
    Instruction(2, 3, mult),
    Instruction(3, 1, rd),
    Instruction(4, 1, wt),
    Instruction(5, 2, je, True),
    Instruction(6, 2, jne, True),
    Instruction(7, 3, le),
    Instruction(8, 3, eq),
    Instruction(9, 1, rel),
    Instruction(99, 0, lambda _ : 1)
]
instructions = {i.opcode : i for i in instruction_list}

def setup():
    intcode = Intcode(opcodes, instructions, [])
    screen = [[0 for x in range(50)] for y in range(50)]
    maze = Maze(screen, intcode)
    maze.traverse()
    # delete robot from screen
    maze.screen[maze.y][maze.x] = 4
    maze.flood_from_oxygen()
    return maze

if PRETTY:
    with ManagedScreen() as term:
        terminal = term
        terminal.clear()
        maze = setup()
        sleep(3)
else:
    maze = setup()

# 1st
print(maze.flooded_start_pos_step+2)

# 2nd
print(maze.flood_step)