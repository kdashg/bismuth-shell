#! /usr/bin/env -S python3 -i

from typing import (
   Iterable,
   TypedDict,
   Literal,
   NamedTuple,
   Callable,
   TypeVar,
   Any
)
from pathlib import Path
import json

# -

type Hex[N] = str


class OfflineIndex:
   type Guid = Hex[Literal[64]]
   type VPath = str
   type Uri = str


   DEFAULT_DIR = Path.home() / 'AppData/Local/Plexamp/Plexamp/Offline'


   class Stream(TypedDict):
      id: int
      streamType: int
      channels: int
      bitrate: int
      samplingRate: int
      selected: bool
      displayTitle: str


   class Part(TypedDict):
      streams: list['OfflineIndex.Stream']
      id: int
      duration: int
      size: int
      key: 'OfflineIndex.VPath'
      container: str


   class Media(TypedDict):
      parts: list['OfflineIndex.Part']
      container: str
      bitrate: int
      audioCodec: str
      duration: int
      offline: bool


   class Item(TypedDict):
      genres: list
      moods: list
      styles: list
      media: list['OfflineIndex.Media']
      related: list
      stations: list
      users: list
      source: Hex[Literal[40]]
      guid: 'OfflineIndex.Guid'
      key: 'OfflineIndex.VPath'
      parentKey: 'OfflineIndex.VPath'
      grandparentKey: 'OfflineIndex.VPath'
      ratingKey: str
      parentRatingKey: str
      grandparentRatingKey: str
      type: Literal['track']
      summary: str
      title: str
      parentTitle: str # ~album
      grandparentTitle: str # ~artist
      parentIndex: int
      viewCount: int
      originalTitle: str
      thumb: 'OfflineIndex.VPath'
      parentThumb: 'OfflineIndex.VPath'
      grandparentThumb: 'OfflineIndex.VPath'
      duration: int # = 7291088
      lastViewedAt: int|None
      addedAt: int # = 1060904914
      librarySectionKey: 'OfflineIndex.VPath' # = '/library/sections/3'
      librarySectionID: int # = 3
      parentGuid: 'OfflineIndex.Uri' # = 'local://30382'
      grandparentGuid: 'OfflineIndex.Uri' # = 'local://32633'


   type HexColor = str # = '#rrggbb'


   class Json(TypedDict):
      items: list['OfflineIndex.Item']
      colormap: dict['OfflineIndex.VPath', list['OfflineIndex.HexColor']]

   # -

   p_json: Path
   raw: Json


   def __init__(self, p_json: Path):
      self.p_json = p_json

      s = self.p_json.read_text()
      self.raw = json.loads(s)


   def track_guid_by_title(self) -> dict[str, str]:
      return {item['title']: item['guid'] for item in self.raw['items']}

   # -

   @staticmethod
   def format_item(item: Item, s: str) -> str:
      (media,) = item['media']
      return s.format(
         artist=item['grandparentTitle'],
         album=item['parentTitle'],
         title=item['title'],
         container=media['container'],
         bitrate=media['bitrate'],
      )

   # -

   def path_from_item(self, t: Item) -> Path:
      stem = t['guid']
      return self.p_json.parent / stem

   # -

   def archive_tracks_cp_args(self, dst: Path, *,
                              format: str|None = None,
                              artist=True,
                              bitrate=True,
                              ) -> list[tuple[Path,Path]]:
      if not format:
         format = ''
         if artist:
            format += '{artist} - '
         format += '{title}'
         if bitrate:
            format += '.{bitrate}'
         format += '.{container}'

      return [
         (
            self.path_from_item(t),
            dst / OfflineIndex.format_item(t, format),
         )
         for t in self.raw['items']
      ]

# -

def archive_offline_cps(dest_dir: Path|str, **kwargs):
   from lib import base

   dest_dir = Path(dest_dir)
   dest_dir.mkdir(parents=True, exist_ok=True)

   playlist_dirs = base.ls(OfflineIndex.DEFAULT_DIR)
   inds = [OfflineIndex(playlist/'index.json') for playlist in playlist_dirs]

   cps = [
      cp
      for ind in inds
         for cp in ind.archive_tracks_cp_args(dest_dir, **kwargs)
   ]
   return cps


def archive_offline(dest_dir: Path|str, **kwargs):
   from lib import base
   cps = archive_offline_cps(dest_dir, **kwargs)
   base.cp_ask(cps)
