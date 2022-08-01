import os
import pathlib
from contextlib import contextmanager


@contextmanager
def present_working_directory(path: pathlib.Path):
    original = os.getcwd()
    os.chdir(path)

    try:
        yield

    finally:
        os.chdir(original)
