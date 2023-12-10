import ast

import os

from renamer.entry import rename, move

current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, 'fixtures') + '/'


def test_rename_function():
    ast_tree = ast.parse("def old_function():\n    pass")
    new_ast_tree = rename(ast_tree, "old_function", "new_function")
    assert new_ast_tree.body[0].name == "new_function"


def test_rename_class_fun():
    with open(path + 'source.py', 'r') as before:
        with open(path + 'expected.py', 'r') as after:
            rename_class = rename(ast.parse(before.read()), "Test", "HardTest")
            rename_function = rename(rename_class, "magic_number", "function_return_magic")
            assert after.read() == ast.unparse(rename_function)


def test_move_class():
    with open(path + 'file1.py', 'r') as file1:
        with open(path + 'file2.py', 'r') as file2:
            (new_ast_one, new_ast_two) = move(ast.parse(file1.read()), ast.parse(file2.read()),
                                              "Test1", "Test2", None, None)

    file1_after = \
        """class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False

def magic_number():
    return 134

class Test2:
    balue: float"""

    file2_after = \
        """class Test1:
    value: int"""

    assert file1_after == ast.unparse(new_ast_one)
    assert file2_after == ast.unparse(new_ast_two)


def test_move_fun_one():
    with open(path + 'file1.py', 'r') as file1:
        with open(path + 'file2.py', 'r') as file2:
            (new_ast_one, new_ast_two) = move(ast.parse(file1.read()), ast.parse(file2.read()),
                                              "magic_number", None, None, None)

    file1_after = \
        """class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False

class Test1:
    value: int"""

    file2_after = \
        """class Test2:
    balue: float

def magic_number():
    return 134"""

    assert file1_after == ast.unparse(new_ast_one)
    assert file2_after == ast.unparse(new_ast_two)


def test_move_fun_two():
    with open(path + 'file1.py', 'r') as file1:
        with open(path + 'file2.py', 'r') as file2:
            (new_ast_one, new_ast_two) = move(ast.parse(file2.read()), ast.parse(file1.read()),
                                              None, "magic_number", None, None)

    file1_after = \
        """class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False

class Test1:
    value: int"""

    file2_after = \
        """class Test2:
    balue: float

def magic_number():
    return 134"""

    assert file2_after == ast.unparse(new_ast_one)
    assert file1_after == ast.unparse(new_ast_two)


def test_move_with_import_one():
    with open(path + 'file3.py', 'r') as file1:
        with open(path + 'file4.py', 'r') as file2:
            (new_ast_one, new_ast_two) = move(ast.parse(file1.read()), ast.parse(file2.read()),
                                              "Test", None, None, "test2")

    file1_after = \
        """import test2

def magic_function():
    test = test2.Test()
    if test.is_test():
        return 42
    else:
        return 11

class Test1:
    value: int"""

    file2_after = \
        """class Test2:
    balue: float

class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False"""

    assert file1_after == ast.unparse(new_ast_one)
    assert file2_after == ast.unparse(new_ast_two)


def test_move_with_import_two():
    with open(path + 'file3.py', 'r') as file1:
        with open(path + 'file4.py', 'r') as file2:
            (new_ast_one, new_ast_two) = move(ast.parse(file2.read()), ast.parse(file1.read()),
                                              None, "Test", "test2", None)

    file1_after = \
        """import test2

def magic_function():
    test = test2.Test()
    if test.is_test():
        return 42
    else:
        return 11

class Test1:
    value: int"""

    file2_after = \
        """class Test2:
    balue: float

class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False"""

    assert file2_after == ast.unparse(new_ast_one)
    assert file1_after == ast.unparse(new_ast_two)


def test_with_none():
    with open(path + 'file3.py', 'r') as file3:
        with open(path + 'file4.py', 'r') as file4:
            file3_text = file3.read()
            file4_text = file4.read()
            ast_one = ast.parse(file3_text)
            ast_two = ast.parse(file4_text)
            (new_ast_one, new_ast_two) = move(ast.parse(file3_text), ast.parse(file4_text),
                                              None, None, None, None)
    assert ast.unparse(ast_one) == ast.unparse(new_ast_one)
    assert ast.unparse(ast_two) == ast.unparse(new_ast_two)


def test_with_none_move_and_with_imports_one():
    with open(path + 'file3.py', 'r') as file3:
        with open(path + 'file4.py', 'r') as file4:
            file3_text = file3.read()
            file4_text = file4.read()
            ast_one = ast.parse(file3_text)
            ast_two = ast.parse(file4_text)
            (new_ast_one, new_ast_two) = move(ast.parse(file3_text), ast.parse(file4_text),
                                              None, None, "test1", "test2")
    assert ast.unparse(ast_one) == ast.unparse(new_ast_one)
    assert ast.unparse(ast_two) == ast.unparse(new_ast_two)


def test_is_nothing_one():
    with open(path + 'file3.py', 'r') as file3:
        with open(path + 'file4.py', 'r') as file4:
            file3_text = file3.read()
            file4_text = file4.read()
            ast_one = ast.parse(file3_text)
            ast_two = ast.parse(file4_text)
            (new_ast_one, new_ast_two) = move(ast.parse(file3_text), ast.parse(file4_text),
                                              None, "Test42", None, None)
    assert ast.unparse(ast_one) == ast.unparse(new_ast_one)
    assert ast.unparse(ast_two) == ast.unparse(new_ast_two)


def test_is_nothing_found_two():
    with open(path + 'file3.py', 'r') as file3:
        with open(path + 'file4.py', 'r') as file4:
            file3_text = file3.read()
            file4_text = file4.read()
            ast_one = ast.parse(file3_text)
            ast_two = ast.parse(file4_text)
            (new_ast_one, new_ast_two) = move(ast.parse(file3_text), ast.parse(file4_text),
                                              "Test32", None, None, "test2")
    assert ast.unparse(ast_one) == ast.unparse(new_ast_one)
    assert ast.unparse(ast_two) == ast.unparse(new_ast_two)
