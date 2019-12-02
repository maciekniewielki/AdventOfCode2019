class Instruction:
    
    def __init__(self, opcode, n_params, fun):
        self.opcode = opcode
        self.n_params = n_params
        self.fun = fun

    def __call__(self, *args):
        return self.fun(*args)


class Intcode:
    
    def __init__(self, opcodes, instructions):
        self.starting_values = opcodes[:]
        self.instructions = instructions        
        self.opcodes = self.starting_values[:]
        self.pos = 0

    def reset(self):
        self.opcodes = self.starting_values[:]
        self.pos = 0

    def set_input(self, in1, in2):
        self.opcodes[1] = in1
        self.opcodes[2] = in2

    def run(self):
        # Read
        val = self.opcodes[self.pos]

        # Decode
        instruction = self.instructions[val]

        # Execute
        params = self.opcodes[self.pos+1:self.pos+1+instruction.n_params]
        ret_val = instruction(self.opcodes, *params)
        
        if ret_val:
            return self.opcodes[0]

        self.pos += 1+instruction.n_params
        return self.run()

# IO
opcodes = list(map(int, open("input.txt").read().split(",")))

# Config
def add(opcodes, in1, in2, out1):
        opcodes[out1] = opcodes[in1] + opcodes[in2]
        return 0

def mult(opcodes, in1, in2, out1):
        opcodes[out1] = opcodes[in1] * opcodes[in2]
        return 0

instruction_list = [
    Instruction(1, 3, add),
    Instruction(2, 3, mult),
    Instruction(99, 0, lambda _ : 1)
]
instructions = {i.opcode : i for i in instruction_list}

# 1st
intcode = Intcode(opcodes, instructions)
intcode.set_input(12, 2)
print(intcode.run())

# 2nd
def double_for(*args):
    for i in range(*args):
        for j in range(*args):
            yield (i, j)

for noun, verb in double_for(100):
    intcode.reset()
    intcode.set_input(noun, verb)
    ret = intcode.run()
    if ret == 19690720:
        print(100 * noun + verb)
        break
