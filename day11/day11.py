import itertools

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
                return self.output_values[0]

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


class Robot:

    def __init__(self, hull, starting_pos, intcode):
        self.hull = hull[:]
        self.starting_pos = starting_pos
        self.x = self.starting_pos[0]
        self.y = self.starting_pos[1]
        self.intcode = intcode
        self.painted = set()
        self.facing = 0 # 0,1,2,3 - up, right, down, left

    def get_instructions(self):
        current_panel = self.hull[self.x][self.y]
        intcode.send_input(current_panel)
        val1 = intcode.run_all()
        if val1 is None:
            return None
        val2 = intcode.run_all()
        if val2 is None:
            return None
        return val1, val2

    def move_once(self):
        val = self.get_instructions()
        if not val:
            return False
        color, turn_right = val
        self.paint(color)
        self.turn(turn_right)
        self.forward()

        return True
    
    def move_all(self):
        while self.move_once():
            pass

        return self.painted

    def paint(self, color):
        self.hull[self.x][self.y] = color
        self.painted.add((self.x, self.y)) 

    def turn(self, turn_right):
        if turn_right:
            self.facing = self.facing + 1
        else:
            self.facing = self.facing - 1

        self.facing = self.facing % 4

    def forward(self):
        moves = [(0,1),(1,0),(0,-1),(-1,0)]
        move = moves[self.facing]
        self.x += move[0]
        self.y += move[1]

def hull_to_ascii(hull):
    s = ""
    for row in hull:
        for char in row:
            s += "*" if char else "."
        s+="\n"
    return s

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

# 1st
square = (100, 100)
hull = [[0 for x in range(square[0])] for y in range(square[1])]
start_pos = (49, 49)
intcode = Intcode(opcodes, instructions, [])
robot = Robot(hull, start_pos, intcode)
print(len(robot.move_all()))

# 2nd
square = (100, 100)
hull = [[0 for x in range(square[0])] for y in range(square[1])]
start_pos = (49, 49)
hull[start_pos[0]][start_pos[1]] = 1
intcode = Intcode(opcodes, instructions, [])
robot = Robot(hull, start_pos, intcode)
robot.move_all()
print(hull_to_ascii(robot.hull))