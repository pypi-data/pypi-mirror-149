"""
util.py : provides aditional utilities
that come in handy during the development
"""
from collections import defaultdict
from .data import (
    GdsTable,
    GdsLayerPurpose,
)
from itertools import starmap

def timer(func):
    """_summary_
    Decorator to time a function
    Args:
        func (function): function to be timed
    Returns:
        function: the same function, but with a time attribute
    """
    import time
    from loguru import logger
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        result = func(*args, **kwargs)
        end = time.time_ns()
        delta = end - start
        func.runtime_ns = delta
        delta_mu = (delta * 1e-3) # obtain time in microseconds 
        mu_symbol = "μ"
        logger.info(f"\nFunction: {func.__name__}\tRuntime: {delta_mu:.3f} {mu_symbol}s.")
        return result
    return wrapper