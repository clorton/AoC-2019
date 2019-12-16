#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from math import ceil

Reactant = namedtuple("Reactant", ["qty", "name"])
Product = namedtuple("Product", ["qty", "name"])
Reaction = namedtuple("Reaction", ["reactants", "product"])

ORE = "ORE"
FUEL = "FUEL"


def main():

    with open("day-14.txt", "r") as file:
        inputs = [line.strip() for line in file.readlines()]

    # # Test 1
    # inputs = [
    #     "10 ORE => 10 A",
    #     "1 ORE => 1 B",
    #     "7 A, 1 B => 1 C",
    #     "7 A, 1 C => 1 D",
    #     "7 A, 1 D => 1 E",
    #     "7 A, 1 E => 1 FUEL"
    # ] # 31

    # # Test 2
    # inputs = [
    #     "9 ORE => 2 A",
    #     "8 ORE => 3 B",
    #     "7 ORE => 5 C",
    #     "3 A, 4 B => 1 AB",
    #     "5 B, 7 C => 1 BC",
    #     "4 C, 1 A => 1 CA",
    #     "2 AB, 3 BC, 4 CA => 1 FUEL"
    # ] # 165

    # # Test 3
    # inputs = [
    #     "157 ORE => 5 NZVS",
    #     "165 ORE => 6 DCFZ",
    #     "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
    #     "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
    #     "179 ORE => 7 PSHF",
    #     "177 ORE => 5 HKGWZ",
    #     "7 DCFZ, 7 PSHF => 2 XJWVT",
    #     "165 ORE => 2 GPVTF",
    #     "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
    # ]   # 13312

    # # Test 4
    # inputs = [
    #     "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
    #     "17 NVRVD, 3 JNWZP => 8 VPVL",
    #     "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
    #     "22 VJHF, 37 MNCFX => 5 FWMGM",
    #     "139 ORE => 4 NVRVD",
    #     "144 ORE => 7 JNWZP",
    #     "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
    #     "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
    #     "145 ORE => 6 MNCFX",
    #     "1 NVRVD => 8 CXFTF",
    #     "1 VJHF, 6 MNCFX => 4 RFSQX",
    #     "176 ORE => 6 VJHF"
    # ]   # 180697

    # # Test 5
    # inputs = [
    #     "171 ORE => 8 CNZTR",
    #     "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
    #     "114 ORE => 4 BHXH",
    #     "14 VRPVC => 6 BMBT",
    #     "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
    #     "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
    #     "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
    #     "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
    #     "5 BMBT => 4 WPTQ",
    #     "189 ORE => 9 KTJDG",
    #     "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
    #     "12 VRPVC, 27 CNZTR => 2 XDBXC",
    #     "15 KTJDG, 12 BHXH => 5 XCVML",
    #     "3 BHXH, 2 VRPVC => 7 MZWV",
    #     "121 ORE => 7 VRPVC",
    #     "7 XCVML => 6 RJRHP",
    #     "5 BHXH, 4 VRPVC => 5 LTCX"
    # ]   # 2210736

    reactions = []
    for line in inputs:
        reactants, product = [component.strip() for component in line.split("=>")]
        reactants = [reactant.strip() for reactant in reactants.split(",")]
        reactants = [reactant.split(" ") for reactant in reactants]
        reactants = [Reactant(int(reactant[0]), reactant[1]) for reactant in reactants]
        qty, name = product.split(" ")
        product = Product(int(qty), name)
        reactions.append(Reaction(reactants, product))

    goals = [Product(1, FUEL)]
    ore = 0
    available = defaultdict(lambda: 0)
    while len(goals) > 0:
        goal = goals.pop(0)
        if available[goal.name] >= goal.qty:
            available[goal.name] -= goal.qty
        else:
            needed = goal.qty - available[goal.name]
            available[goal.name] = 0
            reaction = list(filter(lambda r: r.product.name == goal.name, reactions))[0]
            multiplier = int(ceil(float(needed)/reaction.product.qty))
            for reactant in reaction.reactants:
                if reactant.name != ORE:
                    goals.append(Product(reactant.qty*multiplier, reactant.name))
                else:
                    ore += reactant.qty*multiplier
            available[goal.name] += (reaction.product.qty * multiplier) - needed

    print(f"Need {ore} units of ore.")

    # Part 2

    ONETRILLION = 1000000000000
    ore = ONETRILLION
    available = defaultdict(lambda: 0)
    fuel = 0
    while ore > 0:
        goals = [Product(1, FUEL)]
        while len(goals) > 0:
            goal = goals.pop(0)
            if available[goal.name] >= goal.qty:
                available[goal.name] -= goal.qty
            else:
                needed = goal.qty - available[goal.name]
                available[goal.name] = 0
                reaction = list(filter(lambda r: r.product.name == goal.name, reactions))[0]
                multiplier = int(ceil(float(needed)/reaction.product.qty))
                for reactant in reaction.reactants:
                    if reactant.name != ORE:
                        goals.append(Product(reactant.qty*multiplier, reactant.name))
                    else:
                        # if (reactant.qty*multiplier) > ore:
                        #     seed = list(filter(lambda r: r.product.name == FUEL, reactions))[0]
                        #     undo = [_.name for _ in seed.reactants]
                        #     while len(undo) > 0:
                        #         prod = undo.pop(0)
                        #         rxn = list(filter(lambda r: r.product.name == prod, reactions))[0]
                        #         x = available[prod] // rxn.product.qty
                        #         if x > 0:
                        #             available[prod] -= rxn.product.qty * x
                        #             for react in rxn.reactants:
                        #                 if react.name != ORE:
                        #                     available[react.name] += react.qty * x
                        #                     undo.append(react.name)
                        #                 else:
                        #                     ore += react.qty * x

                        ore -= reactant.qty*multiplier
                        if ore <= 0:
                            break
                available[goal.name] += (reaction.product.qty * multiplier) - needed
            if ore <= 0:
                break
        if ore <= 0:
            break
        fuel += 1
        cost = ONETRILLION - ore
        cycles = ore // cost
        if cycles > 0:
            print(f"Produced {fuel} units of fuel with {cost} units of ore.")
            print(f"Skipping ahead {cycles} cycles.")
            fuel *= (cycles + 1)
            ore -= (cost * cycles)
            print(f"{fuel} fuel produced, {ore} ore remaining after skip.")
            for key, value in available.items():
                available[key] *= cycles

    print(f"Produced {fuel} units of fuel.")
    # ONETRILLION // 443537 = 2254603 is too little
    # 2271734 :( - too low

    return


if __name__ == "__main__":
    main()
