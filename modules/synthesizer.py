"""
    Module Name: Synthesizer

    Description:
        A program synthesizer tool.

    Author: Liav Barsheshet [312429269] Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""
import typing

# Modules Imports
from modules.while_lang import parse, parse_expression
from modules.wp import WeakestPrecondition
from modules.response import Response
from modules.sketch import Sketch
from modules.tree import Tree

# Imports
from typing import Tuple


class Synthesizer:
    """
        A class that represents a program synthesizer tool.
    """

    def __init__(self, data):
        # HTTP Response Object
        self.response = Response()

        # Synthesizer Environment.
        self.env = {
            "program": data['program'],
            "linv": data['linv'],
            "p": data['p'],
            "q": data['q'],
        }

        # AST Program
        self.program: typing.Optional[Tree] = None

        # Logs
        self.logs: list[str] = []

        # Global Error Flag
        self.error = False

    def log(self, msg: str, toggle_error: bool = False, highlight: bool = False) -> None:
        """
            Logs a message to the output stream.
            :param msg: The message to log.
            :param toggle_error: If True, sets the env to error, otherwise logs as info.
            :param highlight: If True, add highlight style to the log, otherwise logs as a regular info.
            :return: None
        """
        if highlight:
            self.logs.append(f'<span data-highlight="true">{msg}</span>')
        else:
            self.logs.append(msg)

        # Toggle Error
        if toggle_error:
            self.error = True

    def log_error(self, msg: str) -> None:
        """
            Logs a message to the output stream and changing the env to contain error.
            :param msg: The error message to log.
            :return: None
        """
        self.log(msg, True)

    def highlight(self, msg: str) -> None:
        """
            Logs a highlight message to the output stream.
            :param msg: The message to log.
            :return: None
        """
        self.log(msg, False, True)

    def data_validation(self) -> bool:
        """
            Validates the user input used in the environment.
            :return: True if the input is valid, otherwise False.
        """
        return len(self.env["p"]) == len(self.env["q"]) and self.env["program"] and self.env["linv"] and len(
            self.env["p"]) > 0

    def evaluate_env(self, name: str) -> bool:
        """
            Evaluates a single environment variable.
            :param name: The name of the environment variable.
            :return: True if the evaluation succeeds, False otherwise.
        """

        self.env[name] = parse_expression(self.env[name])

        if not self.env[name]:
            self.log_error(f"{name} is invalid.")
            return False

        self.env[name] = WeakestPrecondition.parse_expression_as_invariant(self.env[name])

    def evaluate_inputs(self) -> bool:
        """
            Evaluates the input invariants.
            :return: True if the evaluation succeeds, False otherwise.
        """
        for index, (p, q) in enumerate(zip(self.env["p"], self.env["q"])):
            # Parses inputs
            self.env["p"][index] = parse_expression(p)
            self.env["q"][index] = parse_expression(q)

            # Parsing failed
            if not self.env["p"][index]:
                self.log_error(f"P[{index + 1}]: '{p}' is invalid.")

            if not self.env["q"][index]:
                self.log_error(f"Q[{index + 1}]: '{q}' is invalid.")

        # Force quit if an error occurred.
        if self.error:
            return False

        # Convert p and q into invariants.
        for index, (p, q) in enumerate(zip(self.env["p"], self.env["q"])):
            self.env["p"][index] = WeakestPrecondition.parse_expression_as_invariant(p)
            self.env["q"][index] = WeakestPrecondition.parse_expression_as_invariant(q)

        # Evaluating was successful.
        return True

    def program_parsing(self, modify: bool = False) -> None:
        """
             Parses the program into an Abstract Syntax Tree (AST) to validate its syntax.
             :param modify: If True, updates the global program property.
             :return: None
         """
        syntax = parse(self.env['program'])

        # Validating
        if not syntax:
            self.log_error('Program syntax invalid while_lang program.')
            return

        if modify:
            self.program = syntax

    def program_verifying(self) -> None:
        """
             Verifies the program using the weakest precondition method,
             as implemented in Homework 3.

             :return: None
         """
        verifier = WeakestPrecondition(self.program, self.env["p"], self.env["q"], self.env["linv"])

        verification, counter_example = verifier.verify()

        if not verification:
            if not counter_example:
                self.log_error(f"Program is invalid for all inputs.")
                return

            self.log_error(f"Program is invalid, counter example: {counter_example}.")

    def sketch_synthesis(self) -> str:
        """
            Detects holes in the program and attempts to fill them.
            If no holes are present, the verification procedure continues normally.
            :return: A program without holes or assertions.
        """
        # Detects if there is holes
        if not ("??" in self.env["program"]):
            self.log("No holes were found.")
            return self.env["program"]

        # Create a new instance of the Sketch tool.
        sketch = Sketch(self.env)

        # Starts the procedure of filling holes.
        result, new_program, new_program_without_assert = sketch.fill_holes()

        if not result:
            self.error = True
            return new_program

        # Updates to new program code.
        self.env["program"] = new_program

        # Returns an updated version of the code.
        return new_program_without_assert

    def synthesize(self, bench_mode: bool = False) -> Tuple[any, int] | Tuple[bool, bool, bool]:
        """
            Core function of the tool, performing all synthesis steps.
            :param bench_mode: If True, returns a simplified result as Tuple[bool, bool, bool].
                               Otherwise, returns the result as an HTTP response.
            :return: A tuple containing either synthesis results or benchmarking data.
        """
        # Step 0 - Data Validation
        if not self.data_validation():
            if bench_mode:
                return False, False, False

            return self.response.failed('Data is not valid...', self.logs)

        # Step 1 - Evaluating Parameters
        self.evaluate_env('linv')

        # Step 1.5 - Evaluating Inputs
        self.evaluate_inputs()

        if self.error:
            if bench_mode:
                return False, False, False

            return self.response.failed('Evaluation Failed!', self.logs)

        # Step 1 - Completed
        self.log(f'Evaluation succeeded! [{(self.response.delta_seconds())}s]')

        # Step 2 - Validate the program syntax
        self.program_parsing()

        if self.error:
            if bench_mode:
                return False, False, False

            return self.response.failed('Program syntax is invalid!', self.logs)

        # Step 2 - Completed
        self.log(f'Program syntax is valid! [{(self.response.delta_seconds())}s]')

        # Step 3 - Sketch Synthesis
        program = self.sketch_synthesis()

        if self.error:
            if bench_mode:
                return True, False, False
            return self.response.failed('Program could not be synthesized!', self.logs)

        self.highlight(program)

        # Step 3 - Completed
        self.log(f'Program sketch synthesis succeeded! [{(self.response.delta_seconds())}s]')

        # Step 4 - Parsing program into AST Tree
        self.program_parsing(True)

        # Step 5 - Verifying
        self.program_verifying()
        if self.error:
            if bench_mode:
                return True, True, False

            return self.response.failed('Program verification failed!', self.logs)

        # Step 5 - Completed
        self.log(f'Program verification succeeded! [{(self.response.delta_seconds())}s]')

        # Success
        self.log('Finished!')

        # Exit section
        if bench_mode:
            return True, True, True

        return self.response.success('Synthesis has been completed!', self.logs)
