"""
    Module Name: Sketch

    Description:
        An algorithm for filling sketches.

    Author: Liav Barsheshet [312429269] Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""
import typing

# Module Imports
from modules.constants import SKETCH_HOLE_VAR
from modules.wp import WeakestPrecondition
from modules.while_lang import parse

# Imports
from typing import Tuple
from z3 import *
import re


class Sketch:
    """
        Represents a handler for program sketching.
    """

    def __init__(self, synth_env):
        # Synthesis Environment Properties
        self.program = synth_env["program"]
        self.linv = synth_env["linv"]
        self.p = synth_env["p"]
        self.q = synth_env["q"]

    def parse_holes(self) -> str:
        """
            Replaces the program holes with fresh variables.
            :return: A string representing the modified program with fresh variables.
        """

        def replacer(match) -> str:
            """
                [Auxiliary] Helper function to replace matched patterns.
                :param match: The matched pattern to replace.
                :return: The replacement string.
            """

            replacer.counter += 1
            return f"{SKETCH_HOLE_VAR}{replacer.counter - 1}"

        # Set static counter.
        replacer.counter = 0

        # Replacing holes.
        return re.sub(r"\?\?", replacer, self.program)

    def create_hole_constraints(self) -> typing.Optional[typing.Callable]:
        positive_pow = re.compile(r"(?:\*\*|%)\s*(hole\d)")
        non_zero = re.compile(r"[/%]\s*(hole\d)")

        # Find all occurrences of the pattern
        positive_constraints = positive_pow.findall(self.program)
        nonzero_constraints = non_zero.findall(self.program)

        if not positive_constraints and not nonzero_constraints:
            return None
        return lambda env: [env[hole] >= 0 for hole in positive_constraints] + [env[hole] != 0 for hole in
                                                                                nonzero_constraints]

    def fill_holes(self) -> Tuple[bool, str, str]:
        """
            Core method that uses the solver to fill program holes.
            Returns a tuple indicating whether the operation was successful and the filled program.
            :return: A tuple (success: bool, filled_program: str).
        """
        # Filling holes with temporary variables
        self.program = self.parse_holes()

        # Creating Constraints
        hole_constraints = self.create_hole_constraints()

        # Parsing the new program without sketches (??).
        parsed_program = parse(self.program)

        # The program is invalid should not happen.
        if not parsed_program:
            return False, "Invalid program after replacing holes...", ""

        # Creating WeakestPrecondition instance
        wp = WeakestPrecondition(parsed_program, self.p, self.q, self.linv)

        # Solving Constraints.
        result, solution = wp.solve(hole_constraints)

        # Failed
        if not result:
            return False, "Invalid program after replacing holes...", "Invalid program after replacing holes..."

        # Filling Holes
        for key, value in solution.items():
            self.program = self.program.replace(key, str(value))

        # Cleaning Asserts
        tmp = []
        for statement in self.program.split(';'):
            if not ("assert" in statement):
                tmp.append(statement)

        return True, self.program, ';'.join(tmp)
