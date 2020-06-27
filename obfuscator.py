#!/bin/env python3

import ast
import astunparse
import random
import inspect
import sys

builtins = [name for name, function in sorted(
    vars(__builtins__).items())] + ["__builtins__"]

seen = {}
constants = []


class Obfuscator(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if not node.name.startswith("_"):
            node.name = assign_name(node.name)
        for a in node.args.args:
            a.arg = assign_name(a.arg)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = assign_name(node.name)
        return self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            alias.asname = assign_name(alias.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in builtins:
            node.id = add_to_constants(node.id)
        else:
            node.id = assign_name(node.id)
        return self.generic_visit(node)

    def visit_Constant(self, node):
        new_node = ast.Name()
        new_node.id = add_to_constants(node.value, convert=True)
        return new_node


def add_to_constants(constant, convert=False):
    if convert:
        if isinstance(constant, str):
            constant = "\"{}\"".format(constant)
        elif isinstance(constant, int) or isinstance(constant, float):
            constant = str(constant)
        else:
            return constant

    if constant in constants:
        return "𝒙[{}]".format(constants.index(constant))
    else:
        constants.append(constant)
        return "𝒙[{}]".format(len(constants) - 1)


letters = ["Ꭓ", "𝑿"]


def get_variable_name(i):
    letter = letters[i % len(letters)]
    if i >= len(letters):
        return letter + get_variable_name(i // len(letters))
    else:
        return letter


def assign_name(oldName):
    if oldName in seen:
        return seen[oldName]
    else:
        newName = get_variable_name(len(seen))
        seen[oldName] = newName
        return newName


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        tree = ast.parse(f.read())

    Obfuscator().visit(tree)

    random.seed('𝒙')
    shuffled = list(range(len(constants)))
    random.shuffle(shuffled)

    shuffled_constants = [
        constants[shuffled.index(i)] for i in range(len(constants))]

    out = """
import random as X
X.seed('𝒙')
𝒙 = [""" + ",".join(shuffled_constants) + """]
X.shuffle(𝒙)
""" + astunparse.unparse(tree)

    with open(sys.argv[2], "w") as f:
        f.write(out)
