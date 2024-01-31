#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

import io
import platform

import pytest

from pyboy import PyBoy

is_pypy = platform.python_implementation() == "PyPy"


def test_breakpoints_basic(default_rom, monkeypatch):
    pyboy = PyBoy(default_rom, window_type="dummy", breakpoints="0:0100,1:4200,-1:0", debug=False)
    pyboy.set_emulation_speed(0)

    monkeypatch.setattr("sys.stdin", io.StringIO("n\nc"))
    pyboy.tick()

    pyboy.stop(save=False)
