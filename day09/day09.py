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
                return self.output_values[-1]
            elif ret_val == 2:
                return None


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
intcode = Intcode(opcodes, instructions, [1])
print("First part:", intcode.run_all())

# 2nd
intcode = Intcode(opcodes, instructions, [2])
print("Second part:", intcode.run_all())