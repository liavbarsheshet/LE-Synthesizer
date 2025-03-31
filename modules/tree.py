"""
Traditional tree walks:
- Pre-order walk
- Post-order walk [not implemented yet]
- In-order walk - for binary trees [not implemented yet]
"""


class TreeWalk:
    class Visitor:
        def visit_node(self, tree_node):
            pass

        def done(self):
            return None

    def __init__(self, tree):
        self.tree = tree

    def __call__(self, visitor):
        for x in self:
            visitor.visit_node(x)
        return visitor.done()

    def __iter__(self):
        raise NotImplementedError


class PreorderWalk(TreeWalk):

    def __iter__(self):
        stack = [self.tree]
        while stack:
            top = stack[0]
            yield top
            stack[:1] = top.subtrees


class PostorderWalk(TreeWalk):

    def __iter__(self):
        DOWN, UP = 0, 1
        stack = [(DOWN, self.tree)]
        while stack:
            direction, top = stack.pop()
            if direction == UP:
                yield top
            else:
                stack += [(UP, top)] + [(DOWN, x) for x in top.subtrees]


class Tree:
    def __init__(self, root, subtrees=None):
        self.root = root
        if subtrees is None:
            self.subtrees = []
        else:
            self.subtrees = subtrees

    def __eq__(self, other):
        if not isinstance(other, Tree):
            return NotImplemented
        return type(self) == type(other) and (self.root, self.subtrees) == (
            other.root,
            other.subtrees,
        )

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.root, tuple(self.subtrees)))

    def repr(self, leaf_fmt):
        if self.subtrees:
            subreprs = ", ".join(x.repr(leaf_fmt) for x in self.subtrees)
            return "%s{%s}" % (leaf_fmt(self.root), subreprs)
        else:
            return leaf_fmt(self.root)

    def __repr__(self):
        return self.repr(repr)

    def __str__(self):
        return self.repr(str)

    def clone(self):
        return self.reconstruct(self)

    @classmethod
    def reconstruct(cls, t):
        return cls(t.root, [cls.reconstruct(s) for s in t.subtrees])

    @property
    def nodes(self):
        return list(PreorderWalk(self))

    @property
    def leaves(self):
        return [n for n in PreorderWalk(self) if not n.subtrees]

    @property
    def terminals(self):
        """@return a list of the values located at the leaf nodes."""
        return [n.root for n in self.leaves]

    @property
    def depth(self):
        """Computes length of longest branch (iterative version)."""
        stack = [(0, self)]
        max_depth = 0
        while stack:
            depth, top = stack[0]
            max_depth = max(depth, max_depth)
            stack[:1] = [(depth + 1, x) for x in top.subtrees]
        return max_depth

    def split(self, separator=None):
        if separator is None:
            separator = self.root
        if self.root == separator:
            return [item for s in self.subtrees for item in s.split(separator)]
        else:
            return [self]
