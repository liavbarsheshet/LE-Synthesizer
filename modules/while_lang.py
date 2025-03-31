"""
    Module Name: While Lang

    Description:
        An updated version of while lang module that was provided in hw3.

    Author: Liav Barsheshet [312429269] Elshan Getdarov [313735136].
    Date: 09/10/2024.
"""

# Module Imports
from modules.parser.parse_trees import ParseTrees
from modules.parser.silly import SillyLexer
from modules.parser.grammar import Grammar
from modules.parser.parser import Parser
from modules.tree import Tree

# Imports
import typing

# Lexical Tokens
SPECIAL_WORDS = "if|then|else|while|do|skip|assert", r"?![\w\d_]"
BINARY_OPERATORS = "op", r"and|or|\*\*|[!<>=]=|[+\-*/<>\%\/]"
BOOLEAN = "bool", r"True|False"
NUMBER = "num", r"[+\-]?\d+"
SKETCH = "sketch", r"\?\?"
ID = "id", r"(?!(True|False|and|or))[^\W\d]\w*"
ASSIGNMENT = ":="
OTHERS = "[();]"

# TOKENS
PROGRAM_TOKENS = (
    fr"({SPECIAL_WORDS[0]})({SPECIAL_WORDS[1]}) "
    fr"(?P<{BOOLEAN[0]}>{BOOLEAN[1]}) "
    fr"(?P<{NUMBER[0]}>{NUMBER[1]}) "
    fr"(?P<{SKETCH[0]}>{SKETCH[1]}) "
    fr"(?P<{ID[0]}>{ID[1]}) "
    fr"(?P<{BINARY_OPERATORS[0]}>{BINARY_OPERATORS[1]}) "
    fr"{OTHERS} "
    fr"{ASSIGNMENT}".split()
)

# Grammar for expression with no holes
GRAMMAR_SINGLE_EXPRESSION = fr"""
S   ->  E
E   ->  E0  |   E0 {BINARY_OPERATORS[0]} E0 
E0  ->  {BOOLEAN[0]}    |   {ID[0]}   |   {NUMBER[0]} 
E0  ->  ( E )
"""

# Program Grammar
PROGRAM_GRAMMAR = fr"""
S   ->  S1  |   S1 ; S
S1  ->  skip    |   id := E |   assert E  | if E then S else S1 |   while E do S1
S1  ->  ( S )
E   ->  E0  |   E0 {BINARY_OPERATORS[0]} E0
E0  ->  {BOOLEAN[0]}    |   {ID[0]}  |   {NUMBER[0]}     |   {SKETCH[0]}
E0  ->  ( E )
"""


class WhileLangParser:
    """
        Represents a while lang parser.
    """

    def __init__(self, tokens: list[str], grammar: str) -> None:
        """
            Initializes a new instance of the While language parser.
            :param tokens: A list of tokens representing the language's syntax elements.
            :param grammar: A string that defines the grammar rules for parsing.
        """
        self.grammar = Grammar.from_string(grammar)
        self.tokenizer = SillyLexer(tokens)

    def __call__(self, program_text: str) -> typing.Optional[Tree]:
        """
            Parses the given program text and returns the corresponding syntax tree.
            :param program_text: The text of the program to be parsed.
            :return: The parsed syntax tree, or None if parsing fails.
        """
        tokens = list(self.tokenizer(program_text))

        earley = Parser(grammar=self.grammar, sentence=tokens, debug=False)
        earley.parse()

        if earley.is_valid_sentence():
            trees = ParseTrees(earley)
            assert len(trees) == 1
            return self.postprocess(trees.nodes[0])
        else:
            return None

    def postprocess(self, t: Tree) -> Tree:
        """
            Applies post-processing to the given syntax tree.
            :param t: The syntax tree to post-process.
            :return: The post-processed syntax tree.
        """
        if t.root in ["γ", "S", "S1", "E", "E0"] and len(t.subtrees) == 1:
            return self.postprocess(t.subtrees[0])
        elif (
                t.root in ["S", "S1", "E"]
                and len(t.subtrees) == 3
                and t.subtrees[1].root in [":=", ";", "op"]
        ):
            return Tree(
                t.subtrees[1].subtrees[0].root,
                [self.postprocess(s) for s in [t.subtrees[0], t.subtrees[2]]],
            )
        elif len(t.subtrees) == 3 and t.subtrees[0].root == "(":
            return self.postprocess(t.subtrees[1])
        elif t.root == "S1" and t.subtrees[0].root in ["if", "while"]:
            return self.postprocess(Tree(t.subtrees[0].root, t.subtrees[1::2]))
        elif t.root == "S1" and t.subtrees[0].root in ["assert"]:
            return self.postprocess(Tree(t.subtrees[0].root, t.subtrees[1::2]))
        elif t.root == "num":
            return Tree(t.root, [Tree(int(t.subtrees[0].root))])  # parse ints

        return Tree(t.root, [self.postprocess(s) for s in t.subtrees])


def parse(program: str) -> typing.Optional[Tree]:
    """
        Parses a program written in the While language.
        :param program: The program text to be parsed.
        :return: The parsed syntax tree, or None if parsing fails.
    """
    return WhileLangParser(PROGRAM_TOKENS, PROGRAM_GRAMMAR)(program)


def parse_expression(expression: str) -> typing.Optional[Tree]:
    """
        Parses an expression written in the While language.
        :param expression: The expression text to be parsed.
        :return: The parsed syntax tree, or None if parsing fails.
    """
    return WhileLangParser(PROGRAM_TOKENS, GRAMMAR_SINGLE_EXPRESSION)(expression)
