#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser, Namespace
from importlib import import_module
from time import time

from tqdm import tqdm

from day import Day


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")

    parser.add_argument("-d", "--day", type=int)
    parser.add_argument("-1", "--part-1", action="store_true")
    parser.add_argument("-2", "--part-2", action="store_true")

    return parser.parse_args()


def run_tests() -> None:
    directories = [name for name in os.listdir(".") if os.path.isdir(name) and name.startswith("day_")]
    for directory in directories:
        import_module("{name}.{name}".format(name=directory))
    for day_class in tqdm(sorted(Day.__subclasses__(), key=lambda cls: cls.__name__)):
        day = day_class()
        if day.part_1_solution is None:
            tqdm.write("Part 1 of {} is not implemented!".format(day_class.__name__))
        else:
            assert day.part_1() == day.part_1_solution, "Part 1 is broken"
        if day.part_2_solution is None:
            tqdm.write("Part 2 of {} is not implemented!".format(day_class.__name__))
        else:
            assert day.part_2() == day.part_2_solution, "Part 2 is broken"

        if day.part_1_solution is not None and day.part_2_solution is not None:
            tqdm.write("{} is ok!".format(day_class.__name__))


def main() -> None:
    args = parse_arguments()

    if args.test:
        run_tests()
        return

    assert args.day, "Need to specify day"

    directories = [name for name in os.listdir(".") if os.path.isdir(name) and name == "day_{:02d}".format(args.day)]
    assert len(directories) == 1
    import_module("{name}.{name}".format(name=directories[0]))
    assert len(Day.__subclasses__()) == 1

    day = Day.__subclasses__()[0]()

    if args.part_1:
        print("Solution part 1:", day.part_1())

    if args.part_2:
        print("Solution part 2:", day.part_2())


if __name__ == "__main__":
    START_TIME = time()
    main()
    print("Evaluation time {:.1f}s".format((time() - START_TIME)))
