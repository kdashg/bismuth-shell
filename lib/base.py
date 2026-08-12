#! /usr/bin/env python3

from pathlib import Path
from typing import Iterable, Callable, Any, TypeVar

import math
import os
import json

# -

tau = math.tau
pi = math.pi
inf = math.inf
nan = math.nan
E = math.e
C = 299792458 # m/s

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')
V = TypeVar('V')

# -

def sqrt(v: float):
    return v ** 0.5

# Inverse of sum of inverses: 1 / (1/v[0] + 1/v[1] + ...)
def isumi(vs: Iterable[float]) -> float:
   return 1 / sum([1/v for v in vs])


def from_line_col(src: str, line_no: int, col_no: int) -> int:
   pos = 0
   for _ in range(line_no-1):
      pos = src.index('\n', pos)
   pos += col_no-1
   return pos

# -

def Y(body: str) -> Callable[[Any], Any]:
   full = f'lambda x: {body}'
   return eval(full)

def Z(body: str) -> Callable[[Any,Any], Any]:
   full = f'lambda x,y: {body}'
   return eval(full)

def W(body: str) -> Callable[[Any,Any,Any], Any]:
   full = f'lambda x,y,z: {body}'
   return eval(full)

# -

def lsi(path_or_glob: str|Path = Path()) -> Iterable[Path]:
   if isinstance(path_or_glob, str) and '*' in path_or_glob:
      glob = path_or_glob
      return list(Path().glob(glob))

   p = Path(path_or_glob)
   return list(p.iterdir())

def ls(path_or_glob: str|Path = Path()) -> list[Path]:
   return list(lsi(path_or_glob))

# -

import shutil

def cp(cmds: list[tuple[Path,Path]], dry=False) -> None:
   n = len(cmds)

   def info(i:int):
      if n > 1000:
         return f'{i}/{n} {i/n:7.2%}' # Percent of a percent is enough.
      if n > 100:
         return f'{i}/{n} {i/n:6.1%}'

      return f'{i}/{n} {i/n:4.0%}'

   max_info_len = len(info(n))
   for i,(src,dst) in enumerate(cmds):
      info_padded = ' '*30 + info(i)
      info_padded = info_padded[-max_info_len:]
      print(f'[{info_padded}] `{src} -> {dst}`...')
      if not dry:
         shutil.copy(src, dst)

   print(f'[{info(n)}] Done!')

# -

def cd(p: Path|str=Path()) -> Path:
   p = Path(p)
   was = Path()
   os.chdir(p)
   return was

# -

_pushds_ = list[Path]()
def pushd(p: Path|str) -> list[Path]:
   p = Path(p)
   _pushds_.append(cd(p))
   return _pushds_[:]


def popd() -> list[Path]:
   cd(_pushds_.pop())
   return _pushds_[:]

# -

'''
class RustyIterator[T](Iterable[T]):
   raw: Iterable[T]

   def map(self, fn_body: str):


'''

# -

def show(v, /) -> None:
   print(repr(v))

# -

from pprint import pp, pformat, isrecursive, saferepr

import reprlib
def rep(v, *, maxlevel=6, maxtuple=6, maxlist=6, maxarray=5, maxdict=4,
          maxset=6, maxfrozenset=6, maxdeque=6, maxstring=30, maxlong=40,
          maxother=30, fillvalue='...', indent=None) -> str:
   assert reprlib.Repr.__init__.__kwdefaults__
   kwargs = {k:v for k,v in locals().items() if k in reprlib.Repr.__init__.__kwdefaults__.keys()}
   r = reprlib.Repr(**kwargs)
   s = r.repr(v)
   return s


def sho(v, *, maxlevel=6, maxtuple=6, maxlist=6, maxarray=5, maxdict=4,
          maxset=6, maxfrozenset=6, maxdeque=6, maxstring=30, maxlong=40,
          maxother=30, fillvalue='...', indent=None) -> None:
   assert rep.__kwdefaults__
   kwargs = {k:v for k,v in locals().items() if k in rep.__kwdefaults__.keys()}
   print(rep(v, **kwargs))

# -
