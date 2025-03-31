"""
    Module Name: Weakest Precondition

    Description:
        A Weakest Precondition handler, built over the HW3 implementation.

    Author: Liav Barsheshet [312429269], Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""

# Modules Imports
from modules.constants import SKETCH_HOLE_VAR
from modules.tree import Tree

# Imports
from z3 import *
import z3
import operator
import typing

# Type Declaration
Formula: typing.TypeAlias = Ast | bool
PVar: typing.TypeAlias = str

Env: typing.TypeAlias = dict[PVar, Formula]

Invariant: typing.TypeAlias = typing.Callable[[Env], Formula]
InvariantExpression: Invariant | typing.Callable[[Env], int]

# Operators methods
BINARY_OP = {
    "/": lambda x, y: int(x / y) if isinstance(x, int) and isinstance(y, int) else operator.truediv(x, y),
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "%": operator.mod,
    "**": operator.pow,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "and": z3.And,
    "or": z3.Or,
}


class WeakestPrecondition:
    """
        Represents a handler for computing the weakest precondition.
    """

    @staticmethod
    def get_variables(program: Tree) -> list[str]:
        """
            Extracts and registers all variables within the given program.
            :param program: The AST of the program.
            :return: A list of variable names used in the program.
        """
        result = []

        # Looking for id's in the program
        for var in filter(lambda node: node.root == "id", program.nodes):
            var_name = var.subtrees[0].root
            if var_name in result:
                continue
            result.append(var_name)

        return result

    @staticmethod
    def make_env(program: Tree) -> Env:
        """
            Creates an environment dictionary for variables based on the weakest precondition.
            :param program: The AST of the program.
            :return: The environment dictionary (Env) for the program variables.
        """
        env = dict()

        # Creating Z3 obj for each of the program variables.
        for variable in WeakestPrecondition.get_variables(program):
            if variable in env:
                continue
            env[variable] = Int(variable)
        return env

    @staticmethod
    def update_env(env: Env, var: PVar, formula: Formula) -> Env:
        """
            Updates the environment in case of an assignment.
            :param env: The current environment.
            :param var: The variable to update.
            :param formula: The formula representing the new value.
            :return: The updated environment.
        """
        env = env.copy()
        env[var] = formula
        return env

    @staticmethod
    def parse_expression_as_invariant(expression: Tree):
        """
            Parses an expression as invariant.
            :param expression: Expression.
            :return: Invariant.
        """
        cur_node = expression.root

        if cur_node in BINARY_OP:
            left_arg = WeakestPrecondition.parse_expression_as_invariant(expression.subtrees[0])
            right_arg = WeakestPrecondition.parse_expression_as_invariant(expression.subtrees[1])
            return lambda d: BINARY_OP[cur_node](left_arg(d), right_arg(d))

        if cur_node == "id":
            return lambda d: d[expression.subtrees[0].root]

        if cur_node == "num":
            return lambda d: int(expression.subtrees[0].root)

        if cur_node == "bool":
            return lambda d: bool(expression.subtrees[0].root)

    @staticmethod
    def parse_expression(expression: Tree, env: Env) -> Formula | int:
        """
            Parses the given expression within the current environment.
            :param expression: A tree representing the expression.
            :param env: The current environment.
            :return: A parsed formula or an integer constant.
        """
        return WeakestPrecondition.parse_expression_as_invariant(expression)(env)

    def __init__(self, program: Tree, p: list[Invariant], q: list[Invariant], linv: Invariant) -> None:
        """
            Initializes the weakest precondition handler for the given program.
            :param program: An AST representing the program.
            :param p: The pre-condition list.
            :param q: The post-condition list.
            :param linv: The loop invariant.
        """
        # Sets the synthesizer properties.
        self.program = program
        self.linv = linv

        # Inputs outputs.
        self.p = p
        self.q = q

        # Sets the global env properties.
        self.env = WeakestPrecondition.make_env(self.program)

    def unroll_while_loop(self, cond: Tree, body: Tree, q: Invariant, linv: Invariant, is_sketching: bool = False,
                          rolls: int = 8) -> Invariant:
        """
            Unrolls a while loop a specified number of times to analyze loop behaviors.

            cond (Invariant): Loop continuation condition.
            body (Tree): AST for the while loop body.
            while_inv (Invariant): Invariant maintained through each loop iteration.
            linv (Invariant): Local invariant maintained within the loop.
            rolls (int): Number of times to unroll the loop; defaults to 8.

            Returns: Invariant: State of the invariant after unrolling.
        """
        # Handles Chains.
        if rolls == 0:
            return q

        new_q = self.unroll_while_loop(cond, body, q, linv, is_sketching, rolls - 1)

        post_then = self.weakest_precondition(body, new_q, linv, is_sketching)
        post_else = new_q

        return lambda env: Or(And(WeakestPrecondition.parse_expression(cond, env), post_then(env)), (
            And(Not(WeakestPrecondition.parse_expression(cond, env)), post_else(env))))

    def weakest_precondition(self, program: Tree, q: Invariant, linv: Invariant, is_sketching: bool = False,
                             unroll: bool = False) -> Invariant:
        """
            [Recursive] Core function for finding the weakest precondition while traversing the AST.
            :param program: The AST of the program.
            :param q: The post-condition.
            :param linv: The loop invariant.
            :param is_sketching: Detects if its sketch mode.
            :param unroll: Detects if unroll is needed.
            :return: The computed weakest precondition.
        """
        # Handles skipping.
        if program.root == 'skip':
            return q

        # Handles Assignment
        elif program.root == ':=':
            var_raw, expr = program.subtrees
            var = var_raw.subtrees[0].root
            # Performing substitute
            return lambda env: q(
                WeakestPrecondition.update_env(env, var, WeakestPrecondition.parse_expression(expr, env)))

        # Handles Chains.
        elif program.root == ';':
            c1, c2 = program.subtrees

            # Condition for unrolling while loops.
            unroll_needed_c1 = (c1.root == "while" and (
                    any(leaf for leaf in c1.subtrees[1].leaves if SKETCH_HOLE_VAR in str(leaf) or str(leaf) == "assert")
                    or any(leaf for leaf in c2.leaves if SKETCH_HOLE_VAR in str(leaf) or str(leaf) == "assert")
            )) and is_sketching

            unroll_needed_c2 = (c2.root == "while" and (
                any(leaf for leaf in c2.subtrees[1].leaves if SKETCH_HOLE_VAR in str(leaf) or str(leaf) == "assert")
            )) and is_sketching

            return self.weakest_precondition(c1, self.weakest_precondition(c2, q, linv, is_sketching, unroll_needed_c2),
                                             linv,
                                             is_sketching,
                                             unroll_needed_c1)

        # Handles If Condition.
        elif program.root == 'if':
            cond, then_branch, else_branch = program.subtrees
            post_then = self.weakest_precondition(then_branch, q, linv, is_sketching)
            post_else = self.weakest_precondition(else_branch, q, linv, is_sketching)
            return lambda env: Or(And(WeakestPrecondition.parse_expression(cond, env), post_then(env)), (
                And(Not(WeakestPrecondition.parse_expression(cond, env)), post_else(env))))

        # Handles Assert
        elif program.root == 'assert':
            cond = program.subtrees[0]
            return lambda env: And(WeakestPrecondition.parse_expression(cond, env), q(env))

        # Handles While loops
        elif program.root == 'while':
            cond, body = program.subtrees

            # Generates While Environment.
            while_env = {key: Int(key) for index, (key, value) in enumerate(self.env.items())}

            # Creating Formulas
            forall_variables = [val for key, val in while_env.items() if key in body.terminals]

            # WP while body
            body_wp = self.weakest_precondition(body, linv, linv)

            # Parsing b
            b = WeakestPrecondition.parse_expression(cond, while_env)

            # Create While Formula
            def while_wp(env):
                return And(
                    linv(env),
                    ForAll(forall_variables,
                           And(
                               Implies(
                                   And(linv(while_env), b),
                                   body_wp(while_env)),
                               Implies(
                                   And(linv(while_env), Not(b)),
                                   q(while_env))
                           ))
                )

            # Unrolling While loop
            new_wp = self.unroll_while_loop(cond, body, q, linv) if unroll else while_wp

            return new_wp

    def verify(self):
        """
            Verifies weakest precondition program.
            :return: Verification or counter example.
        """
        # Creating new solver Instance.
        solver = Solver()
        # Checks P => WP
        solver.add(Not(And(
            [Implies(p(self.env), self.weakest_precondition(self.program, q, self.linv)(self.env)) for p, q in
             zip(self.p, self.q)])))

        if solver.check() == sat:
            return False, solver.model()

        return True, None

    def solve(self, hole_constraints: typing.Optional[Invariant]) -> (
            typing.Tuple)[bool, typing.Optional[dict[str, int]]]:
        """
            Solves a program sketch .
            :return: Tuple indicating whether a solution was found and the final model (if found).
        """
        # Initialize hole values
        new_env = {key: value for key, value in self.env.items()}

        solver = Solver()
        solver.add(ForAll([value for key, value in new_env.items() if not (SKETCH_HOLE_VAR in key)],
                          And([Implies(p(new_env), self.weakest_precondition(self.program, q, self.linv, True)(new_env))
                               for
                               p, q in zip(self.p, self.q)])))
        if hole_constraints:
            solver.add(hole_constraints(new_env))

        if solver.check() == sat:
            # Creating Solution
            solution = solver.model()

            result = {}

            # Parsing Holes
            for var in solution.decls():
                var_name = var.name()
                if not (SKETCH_HOLE_VAR in var_name):
                    continue
                result[var_name] = solution[var].as_long()

            # Exit Section
            return True, result

        return False, None
