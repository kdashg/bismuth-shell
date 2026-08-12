#! /usr/bin/env python3

from pathlib import Path
from typing import Iterable, Callable, Any, TypeVar

import math
import os
import json

from pprint import pp, pformat, isrecursive, saferepr

import reprlib

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


def cp(cps: list[tuple[Path,Path]], dryrun:bool=False) -> None:
   n = len(cps)

   def info(i:int):
      if n > 1000:
         return f'{i}/{n} {i/n:7.2%}' # Percent of a percent is enough.
      if n > 100:
         return f'{i}/{n} {i/n:6.1%}'

      return f'{i}/{n} {i/n:4.0%}'

   prev_choice = ''

   failed = list[tuple[int,Path,Path]]()

   max_info_len = len(info(n))
   for i,(src,dest) in enumerate(cps):
      info_padded = ' '*30 + info(i)
      info_padded = info_padded[-max_info_len:]


      def msg(*, dest):
        return f'[{info_padded}] `{src} -> {dest}`...'


      def fn_cp(*, dest: Path|None):
         print(msg(dest=dest))
         if dest and not dryrun:
            try:
               shutil.copy(src, dest)
            except OSError:
               failed.append((i,src,dest))


      if dest.exists():
         print(msg(dest=dest))

         for i in range(2,1000):
            dest_i = dest.with_stem(f'{dest.stem}({i})')
            if not dest_i.exists():
               break

         print(
            '\n'.join([
               f'Conflict: dest:{dest} already exists! Choose:',
               f'   1. Overwrite',
               f'   2. Skip',
               f'   3. Write instead to {dest_i.name}',
            ])
         )
         while True:
            choice = input('Choose 1/2/3: ')
            if choice == '':
               choice = prev_choice
            try:
               choice = int(choice)
            except ValueError:
               continue

            if choice == 1:
               print('Overwriting...')
               dest = dest
            elif choice == 2:
               print('Skipping...')
               dest = None
            elif choice == 3:
               print('Writing instead...')
               dest = dest_i
            else:
               continue
            prev_choice = choice
            break

      fn_cp(dest=dest)

   print(f'[{info(n)}] Done!')

   if failed:
      print('Failed:', pformat(failed))


# -

def input_choose_lower(chars: str):
   # Defaults?
   uppers = [c for c in chars if c.isupper()]
   assert len(uppers) <= 1, (uppers,chars)

   default:Any = None
   if len(uppers):
      (default,) = uppers

   lchars = chars.lower()

   while True:
      c = input(f'Choose [{chars}]: ')[:1]
      if c == '':
         c = default
      c = c.lower()
      if c in lchars:
         return c

# -

def cp_ask(cps: list[tuple[Path,Path]]) -> None:
   print(f'cps: [len({len(cps)})]')
   for (src,dest) in cps:
      print(f'   {src} -> {dest}')

   if input_choose_lower('Yn') == 'y':
      return cp(cps)

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
