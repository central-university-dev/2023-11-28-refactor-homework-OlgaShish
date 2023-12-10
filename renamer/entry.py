import ast
from copy import copy
from typing import Optional, Any


def rename(ast_tree: ast.AST, old_name: str, new_name: str) -> ast.AST:
    nodes = ast.walk(ast_tree)
    for node in nodes:
        if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
            if node.name == old_name:
                node.name = new_name
                break
    return ast_tree


def find_node(ast_tree: ast.AST, name: str) -> Optional[Any]:
    nodes = ast.walk(ast_tree)
    for node in nodes:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def delete_node(ast_tree: Any, name: str) -> ast.AST:
    nodes = ast_tree.body
    for node in nodes:
        if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
            if node.name == name:
                ast_tree.body.remove(node)
                return ast_tree
            else:
                delete_node(node, name)
    return ast_tree


def set_node(ast_tree: ast.AST, new_node: ast.AST, name: str) -> ast.AST:
    nodes = ast.walk(ast_tree)
    for node in nodes:
        if isinstance(node, ast.ClassDef) and isinstance(new_node, ast.ClassDef) and node.name == name:
            node.name = new_node.name
            node.body = new_node.body
            return ast_tree
        elif isinstance(node, ast.FunctionDef) and isinstance(new_node, ast.FunctionDef) and node.name == name:
            node.name = new_node.name
            node.body = new_node.body
    return ast_tree


def add_import(ast_tree: ast.AST, name: str, file_name: str) -> ast.AST:
    nodes = ast.walk(ast_tree)
    check = False
    for node in nodes:
        if hasattr(node, "id") and node.id == name:
            node.id = file_name + "." + name
            check = True
    if check:
        ast_tree.body.insert(0, (ast.Import(names=[ast.alias(name=file_name)])))
    return ast_tree


def move(ast_tree_one: ast.AST,
         ast_tree_two: ast.AST,
         name_node_one: Optional[str],
         name_node_two: Optional[str],
         file_name_one: Optional[str],
         file_name_two: Optional[str]
         ) -> (ast.AST, ast.AST):
    if name_node_one is not None and name_node_two is not None:
        node_one = copy(find_node(ast_tree_one, name_node_one))
        node_two = copy(find_node(ast_tree_two, name_node_two))
        if node_one is not None and node_two is not None:
            ast_tree_one = set_node(ast_tree_one, node_two, name_node_one)
            ast_tree_one = add_import(ast_tree_one, name_node_one, file_name_two)
            ast_tree_two = set_node(ast_tree_two, node_one, name_node_two)
            ast_tree_two = add_import(ast_tree_two, node_two, file_name_one)
        return ast_tree_one, ast_tree_two
    elif name_node_one is None and name_node_two is not None:
        node_two = copy(find_node(ast_tree_two, name_node_two))
        if node_two is not None:
            ast_tree_one.body.append(node_two)
            ast_tree_two = add_import(ast_tree_two, name_node_two, file_name_one)
            return ast_tree_one, delete_node(ast_tree_two, name_node_two)
        else:
            return ast_tree_one, ast_tree_two
    elif name_node_one is not None and name_node_two is None:
        node_one = copy(find_node(ast_tree_one, name_node_one))
        if node_one is not None:
            ast_tree_two.body.append(node_one)
            ast_tree_one = add_import(ast_tree_one, name_node_one, file_name_two)
            return delete_node(ast_tree_one, name_node_one), ast_tree_two
        else:
            return ast_tree_one, ast_tree_two
    else:
        return ast_tree_one, ast_tree_two
