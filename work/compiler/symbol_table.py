from collections import defaultdict
from enum import Enum

class Symbol:
    class Kind(Enum):
        STATIC = "static"
        FIELD = "this"
        ARG = "argument"
        VAR = "local"
        CONSTANT = "constant"
        POINTER = "pointer"

        def to_vm_segment(self) -> str:
            return self.value
        
    def __init__(self, name: str, ptype: str, kind: Kind, index: int):
        self.name = name
        self.type = ptype
        self.kind = kind
        self.index = index

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type}, kind={self.kind}, index={self.index})"

    def __repr__(self):
        return self.__str__()

    def get_type(self) -> str:
        return self.type

    def get_kind(self) -> Kind:
        return self.kind

    def get_index(self) -> int:
        return self.index

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
        
    def __getitem__(self, name: str) -> Symbol:
        return self.by_name[name]

    def __contains__(self, key):
        return key in self.by_name

    def get_n_locals(self) -> int:
        return len(self.by_kind[Symbol.Kind.VAR])

    def get_n_fields(self) -> int:
        return len(self.by_kind[Symbol.Kind.FIELD])

    def get_n_args(self) -> int:
        return len(self.by_kind[Symbol.Kind.ARG])
