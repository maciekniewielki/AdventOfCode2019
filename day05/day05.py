class Param:
    def __init__(self, val, mode):
        self.val = val
        self.mode = mode

    def get_input_val(self, opcodes):
        if self.mode == 0:
            return opcodes[self.val]
        return self.val

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
        self.opcodes = self.starting_values[:]
        self.pos = 0

    def reset(self):
        self.opcodes = self.starting_values[:]
        self.pos = 0

    def run_all(self):
        while True:
            ret_val = self.run()
            if ret_val:
                break

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
        
        if ret_val:
            return self.opcodes[0]

        if not instruction.modifies_address:
            self.pos += 1+instruction.n_params

        return ret_val

# IO
opcodes = list(map(int, open("input.txt").read().split(",")))

# Config
def add(intcode, in1, in2, out1):
        intcode.opcodes[out1.val] = in1.get_input_val(intcode.opcodes) + in2.get_input_val(intcode.opcodes)
        return 0

def mult(intcode, in1, in2, out1):
        intcode.opcodes[out1.val] = in1.get_input_val(intcode.opcodes) * in2.get_input_val(intcode.opcodes)
        return 0

def rd(intcode, dest):
    val = intcode.input_values.pop()
    intcode.opcodes[dest.val] = val

def wt(intcode, source):
    print("Output: ", source.get_input_val(intcode.opcodes))

def je(intcode, in1, in2):
    val = in1.get_input_val(intcode.opcodes)
    if val != 0:
        intcode.pos = in2.get_input_val(intcode.opcodes)
    else:
        intcode.pos += 3

def jne(intcode, in1, in2):
    val = in1.get_input_val(intcode.opcodes)
    if val == 0:
        intcode.pos = in2.get_input_val(intcode.opcodes)
    else:
        intcode.pos += 3

def le(intcode, in1, in2, dest):
    val1 = in1.get_input_val(intcode.opcodes)
    val2 = in2.get_input_val(intcode.opcodes)
    intcode.opcodes[dest.val] = int(val1 < val2)

def eq(intcode, in1, in2, dest):
    val1 = in1.get_input_val(intcode.opcodes)
    val2 = in2.get_input_val(intcode.opcodes)
    intcode.opcodes[dest.val] = int(val1 == val2)

instruction_list = [
    Instruction(1, 3, add),
    Instruction(2, 3, mult),
    Instruction(3, 1, rd),
    Instruction(4, 1, wt),
    Instruction(5, 2, je, True),
    Instruction(6, 2, jne, True),
    Instruction(7, 3, le),
    Instruction(8, 3, eq),
    Instruction(99, 0, lambda _ : 1)
]
instructions = {i.opcode : i for i in instruction_list}

# 1st
print("First part:")
intcode = Intcode(opcodes, instructions, [1])
intcode.run_all()

# 2nd
print("Second part:")
intcode = Intcode(opcodes, instructions, [5])
intcode.run_all()