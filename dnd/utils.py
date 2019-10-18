#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""General methods"""
import ast
import functools
import operator as op


def eval_(node):
    if isinstance(node, ast.Num):
        # <number>
        return node.n
    elif isinstance(node, ast.BinOp):
        # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


def limit(max_=None):
    """Return decorator that limits allowed returned values."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            try:
                mag = abs(ret)
            except TypeError:
                # Not applicable
                pass
            else:
                if mag > max_:
                    raise ValueError(ret)
            return ret
        return wrapper
    return decorator


eval_ = limit(max_=10**100)(eval_)


def power(a, b):
    """Limit the use of exponential calculations"""
    if any(abs(n) > 100 for n in [a, b]):
        raise ValueError((a, b))
    return op.pow(a, b)


# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: power,
    ast.BitXor: op.xor,
    ast.USub: op.neg
}


def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)


