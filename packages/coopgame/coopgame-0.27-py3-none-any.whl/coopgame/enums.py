from enum import Enum

def add_succ_and_pred_maps(cls):
    succ_map = {}
    pred_map = {}
    first = None
    cur = None
    nxt = None
    last = None
    for val in cls.__members__.values():
        if first is None:
            first = val

        if cur is None:
            cur = val
        elif nxt is None:
            nxt = val

        last = val

        if cur is not None and nxt is not None and cur != nxt:
            succ_map[cur] = nxt
            pred_map[nxt] = cur
            cur = nxt
            nxt = None

    # add wrap arounds
    succ_map[last] = first
    pred_map[first] = last

    cls._succ_map = succ_map
    cls._pred_map = pred_map

    def succ(self):
        return self._succ_map[self]

    def pred(self):
        return self._pred_map[self]

    cls.succ = succ
    cls.pred = pred
    return cls



@add_succ_and_pred_maps
class Orientation(Enum):
    UP=1
    RIGHT=2
    DOWN=3
    LEFT=4

@add_succ_and_pred_maps
class ConnectionType(Enum):
    ARC = 1
    LINE = 2
    BEZIER = 3

@add_succ_and_pred_maps
class EntryType(Enum):
    CRAWLER = 1
    GRIDCLICK = 2

@add_succ_and_pred_maps
class GridDrawType(Enum):
    BOXES = 1
    LINES = 2