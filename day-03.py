#!/usr/bin/env python3

import numpy as np


# def add(ip, memory):
#
#     a = memory[memory[ip]]
#     ip += 1
#     b = memory[memory[ip]]
#     ip += 1
#     destination = memory[ip]
#     ip += 1
#     memory[destination] = a + b
#
#     return ip
#
#
# def multiply(ip, memory):
#
#     a = memory[memory[ip]]
#     ip += 1
#     b = memory[memory[ip]]
#     ip += 1
#     destination = memory[ip]
#     ip += 1
#     memory[destination] = a * b
#
#     return ip
#
#
# opcodes = {
#     1: add,
#     2: multiply
# }
#
#
# def process(opcode, ip, memory):
#
#     if opcode in opcodes:
#         ip = opcodes[opcode](ip, memory)
#     else:
#         raise RuntimeError(f'Unknown opcode {opcode} at ip {ip}.')
#
#     return ip
#
#
# def execute(memory):
#
#     ip = 0
#     while memory[ip] != 99:
#         opcode = memory[ip]
#         ip += 1
#         ip = process(opcode, ip, memory)
#
#     return memory


def main(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    # lines = [
    #     "R8,U5,L5,D3",
    #     "U7,R6,D4,L4"
    # ]

    # lines = [
    #     "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    #     "U62,R66,U55,R34,D71,R55,D58,R83"
    # ]

    # lines = [
    #     "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    #     "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # ]

    line1 = lines[0].split(',')
    line2 = lines[1].split(',')

    compass = {
        'R': (1, 0),
        'D': (0, 1),
        'L': (-1, 0),
        'U': (0, -1)
    }

    # part 1

    x = 0
    y = 0
    min_x1 = 1 << 31
    min_y1 = 1 << 31
    max_x1 = -min_x1
    max_y1 = -min_y1
    for entry in line1:
        direction = entry[0]
        distance = int(entry[1:])
        x += compass[direction][0] * distance
        y += compass[direction][1] * distance
        min_x1 = min(min_x1, x)
        min_y1 = min(min_y1, y)
        max_x1 = max(max_x1, x)
        max_y1 = max(max_y1, y)

    x = 0
    y = 0
    min_x2 = 1 << 31
    min_y2 = 1 << 31
    max_x2 = -min_x2
    max_y2 = -min_y2
    for entry in line2:
        direction = entry[0]
        distance = int(entry[1:])
        x += compass[direction][0] * distance
        y += compass[direction][1] * distance
        min_x2 = min(min_x2, x)
        min_y2 = min(min_y2, y)
        max_x2 = max(max_x2, x)
        max_y2 = max(max_y2, y)

    min_x = min(min_x1, min_x2)
    min_y = min(min_y1, min_y2)
    max_x = max(max_x1, max_x2)
    max_y = max(max_y1, max_y2)

    board = np.zeros((max_x-min_x+1, max_y-min_y+1), dtype=np.uint32)

    x = 0
    y = 0
    for entry in line1:
        direction = entry[0]
        distance = int(entry[1:])
        for _ in range(distance):
            x += compass[direction][0]
            y += compass[direction][1]
            board[x-min_x, y-min_y] |= 1

    crossings = set()
    x = 0
    y = 0
    for entry in line2:
        direction = entry[0]
        distance = int(entry[1:])
        for _ in range(distance):
            x += compass[direction][0]
            y += compass[direction][1]
            board[x-min_x, y-min_y] |= 2
            if board[x-min_x, y-min_y] == 3:
                crossings.add((x, y))

    minimum = 1 << 31
    for entry in crossings:
        distance = abs(entry[0]) + abs(entry[1])
        if distance > 0:
            minimum = min(minimum, distance)

    print(f"Minimum distance is {minimum}.")

    # part 2

    board = np.zeros_like(board)
    visits = np.zeros_like(board)

    x = 0
    y = 0
    count = 0
    for entry in line1:
        direction = entry[0]
        distance = int(entry[1:])
        for _ in range(distance):
            x += compass[direction][0]
            y += compass[direction][1]
            count += 1
            if (visits[x-min_x, y-min_y] & 1) == 0:
                board[x-min_x, y-min_y] = count
                visits[x-min_x, y-min_y] |= 1

    crossings = set()
    x = 0
    y = 0
    count = 0
    for entry in line2:
        direction = entry[0]
        distance = int(entry[1:])
        for _ in range(distance):
            x += compass[direction][0]
            y += compass[direction][1]
            count += 1
            if (visits[x-min_x, y-min_y] & 2) == 0:
                board[x-min_x, y-min_y] += count
                visits[x - min_x, y - min_y] |= 2
                if visits[x-min_x, y-min_y] == 3:
                    crossings.add((x, y))

    minimum = 1 << 31
    for entry in crossings:
        steps = board[entry[0]-min_x, entry[1]-min_y]
        if steps > 0:
            minimum = min(minimum, steps)

    print(f"Minimum steps is {minimum}.")

    return


if __name__ == '__main__':
    main('day-03.txt')
