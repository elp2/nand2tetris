from collections import defaultdict
from enum import Enum

class Symbol:
    class Kind(Enum):
        STATIC = "STATIC"
        FIELD = "FIELD" 
        ARG = "ARG"
        VAR = "VAR"
        
    def __init__(self, name: str, ptype: str, kind: Kind, index: int):
        self.name = name
        self.type = ptype
        self.kind = kind
        self.index = index

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type}, kind={self.kind}, index={self.index})"

    def __repr__(self):
        return self.__str__()


class SymbolTable:
    def __init__(self):
        self.by_name = {}
        self.by_kind = defaultdict(list)
        
    def define(self, name: str, ptype: str, kind: Symbol.Kind):
        if name in self.by_name:
            raise ValueError(f"Symbol {name} already defined")
        symbol = Symbol(name, ptype, kind, len(self.by_kind[kind]))
        self.by_name[name] = symbol
        self.by_kind[kind].append(symbol)

    def var_count(self, kind: Symbol.Kind) -> int:
        return len(self.by_kind[kind])
    