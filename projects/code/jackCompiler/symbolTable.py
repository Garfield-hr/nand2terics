class SymbolVal:
    def __init__(self, type, kind, ind) -> None:
        self.type = type
        self.kind = kind
        self.ind = ind

class SymbolTable:
    def __init__(self) -> None:
        self.symbolLinkedList = []

    def construct_next_symbol_table(self) -> None:
        self.next_dict = {}
        self.symbolLinkedList.append(self.next_dict)

    def pop_last_symbol_table(self) -> None:
        self.symbolLinkedList.pop()

    def add_symbol(self, symbol:str, type:str, kind:str, ind:int) -> None:
        curr_dict = self.symbolLinkedList[-1]
        curr_dict[symbol] = SymbolVal(type, kind, ind)

    def get_symbol_val(self, symbol:str) -> SymbolVal:
        if not self.symbolLinkedList:
            raise RuntimeError("Query symbol when symbol table is null.")
        curr_dict = self.symbolLinkedList[-1]
        if symbol in curr_dict:
            return curr_dict[symbol]
        else:
            return self.get_symbol_val_help(symbol, len(self.symbolLinkedList) - 2)

    def get_symbol_val_help(self, symbol:str, ind):
        if ind < 0:
            return False
        curr_dict = self.symbolLinkedList[ind]
        if symbol in curr_dict:
            return curr_dict[symbol]
        else:
            return self.get_symbol_val_help(symbol, ind - 1)