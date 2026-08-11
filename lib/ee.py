#! /usr/bin/env -S python3 -i

from typing import Iterable

def isumi(vs: Iterable[float]) -> float:
    return 1 / sum([1/v for v in vs])

def sqrt(v: float):
    return v ** 0.5

def lc_hz(L: float, C: float):
    return 1 / 2 / 3.1416 / sqrt(L * C)

def xtal_pull_df(C0_shunt: float, C1: float, CL: float, f: float = 1) -> float:
    return f * C1 / 2 / (C0_shunt + CL)


