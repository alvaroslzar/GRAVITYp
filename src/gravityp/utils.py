"""This module contains some utility functions
"""
__all__ = ["to_tuple", "to_list"]

def to_tuple(var) -> tuple:
    if var.__class__ != tuple:
        return (var,)
    else:
        return var
    
def to_list(var) -> list:
    if var.__class__ != list:
        return [var]
    else:
        return var