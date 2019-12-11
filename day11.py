#!/usr/bin/env python3


from collections import namedtuple


ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
BASE = 9
HALT = 99

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

Microcode = namedtuple('Microcode', ['function', 'count'])


class Computer(object):

    def __init__(self, memory, inputs):
        self.memory = list(memory)
        self.inputs = list(inputs)
        self.ip = 0
        self.index = 0
        self.output = None
        self.base = 0

        return

    def reset(self):
        self.ip = 0

    @classmethod
    def mode(cls, modes, index):
        # modes(1002, 1) => 0
        # modes(1002, 2) => 1
        # modes(1002, 3) => 0
        return (modes // (10**(index+1))) % 10

    def load(self, mode, arg):

        if mode == POSITION:
            while arg >= len(self.memory):
                self.memory.append(0)
            return self.memory[arg]
        elif mode == RELATIVE:
            while (self.base + arg) >= len(self.memory):
                self.memory.append(0)
            return self.memory[self.base + arg]
        elif mode == IMMEDIATE:
            return arg
        else:
            assert False, f"Unknown addressing mode {mode}"

    def store(self, value, mode, location):

        if mode == POSITION:
            while location >= len(self.memory):
                self.memory.append(0)
            self.memory[location] = value
        elif mode == RELATIVE:
            while (self.base + location) >= len(self.memory):
                self.memory.append(0)
            self.memory[self.base + location] = value
        else:
            assert False, f"Cannot store with mode {mode}"

        return

    def add(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        # assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(first + second, Computer.mode(modes, 3), self.memory[self.ip+3])

        return False

    def multiply(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        # assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(first * second, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def input(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.inputs[self.index]
        self.index += 1
        # assert Computer.mode(modes, 1) == POSITION, 'Cannot store with immediate mode.'
        self.store(value, Computer.mode(modes, 1), self.memory[self.ip + 1])

        return False

    def output(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        value = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        self.output = value
        # print(f"value")

        return False

    def jump_if_true(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first != 0:
            self.ip = second
            return True

        return False

    def jump_if_false(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        if first == 0:
            self.ip = second
            return True

        return False

    def less(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        # assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(1 if first < second else 0, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def equals(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        second = self.load(Computer.mode(modes, 2), self.memory[self.ip + 2])
        # assert Computer.mode(modes, 3) == POSITION, 'Cannot store with immediate mode.'
        self.store(1 if first == second else 0, Computer.mode(modes, 3), self.memory[self.ip + 3])

        return False

    def rebase(self):

        modes = self.memory[self.ip] - (self.memory[self.ip] % 10)
        first = self.load(Computer.mode(modes, 1), self.memory[self.ip + 1])
        self.base += first

        return False

    instructions = {
        ADD: Microcode(add, 4),
        MULTIPLY: Microcode(multiply, 4),
        INPUT: Microcode(input, 2),
        OUTPUT: Microcode(output, 2),
        JUMP_IF_TRUE: Microcode(jump_if_true, 3),
        JUMP_IF_FALSE: Microcode(jump_if_false, 3),
        LESS_THAN: Microcode(less, 4),
        EQUALS: Microcode(equals, 4),
        BASE: Microcode(rebase, 2)
    }

    def run(self, inputs=None) -> int:

        if inputs is not None:
            self.inputs.extend(inputs)
        self.output = None
        while self.memory[self.ip] != HALT:
            opcode = self.memory[self.ip] % 10
            if not Computer.instructions[opcode].function(self):
                self.ip += Computer.instructions[opcode].count
            if opcode == OUTPUT:
                break

        # noinspection PyTypeChecker
        return self.output


Point = namedtuple("Point", ["x", "y"])
BLACK = 0
WHITE = 1
LEFT = 0
RIGHT = 1


def main():

    with open('day11.txt', 'r') as file:
        inputs = file.read()

    program = [int(entry) for entry in inputs.split(',')]

    directions = [
        Point(0, -1),
        Point(1, 0),
        Point(0, 1),
        Point(-1, 0)
    ]

    robot_x = 0
    robot_y = 0
    direction = 0
    computer = Computer(program, [])
    hull = {}
    painted = set()
    while True:
        location = Point(robot_x, robot_y)
        color = WHITE if location in hull and hull[location] == WHITE else BLACK
        paint = computer.run([color])
        if paint is None:
            break
        turn = computer.run()
        if turn is None:
            break
        hull[location] = paint
        painted.add(location)
        if turn == LEFT:
            direction -= 1
        else:   # turn == RIGHT
            direction += 1
        direction %= len(directions)
        robot_x += directions[direction].x
        robot_y += directions[direction].y

    print(f"# of panels painted = {len(painted)}")

    # Part 2
    robot_x = 0
    robot_y = 0
    direction = 0
    computer = Computer(program, [])
    hull = {Point(robot_x, robot_y): WHITE}
    painted = set()
    while True:
        location = Point(robot_x, robot_y)
        color = WHITE if location in hull and hull[location] == WHITE else BLACK
        paint = computer.run([color])
        if paint is None:
            break
        turn = computer.run()
        if turn is None:
            break
        hull[location] = paint
        painted.add(location)
        if turn == LEFT:
            direction -= 1
        else:   # turn == RIGHT
            direction += 1
        direction %= len(directions)
        robot_x += directions[direction].x
        robot_y += directions[direction].y

    min_x = 1 << 31
    max_x = -min_x
    min_y = min_x
    max_y = max_x
    for point in painted:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    pixels = [[' ' for _ in range(width)] for __ in range(height)]
    for point in hull:
        if hull[point] == WHITE:
            pixels[point.y-min_y][point.x-min_x] = "#"

    for y in range(height):
        print(''.join(pixels[y]))

    return


if __name__ == "__main__":
    main()
