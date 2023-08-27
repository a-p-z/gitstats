import sys
from random import randint


def an_interface() -> str:
    return f"interface-{randint(0, sys.maxsize)}"


def an_instance() -> str:
    return f"instance-{randint(0, sys.maxsize)}"
