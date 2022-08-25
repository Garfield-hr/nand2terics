from CodeWriter import CodeWriter

class VmVarKind:
    argument = "argument"
    local = "local"
    static = "static"
    constant = "constant"
    this = "this"
    that = "that"
    pointer = "pointer"
    temp = "temp"

class jackCodeWriter(CodeWriter):
    def __init__(self, dest_file: str) -> None:
        super().__init__(dest_file)

    def write_function(self, function_name: str, arg_num: int) -> None:
        self.write_code("function " + function_name + " " + str(arg_num))
    
    def write_push(self, var_kind: str, var_ind: int) -> None:
        self.write_code("push " + var_kind + " " + str(var_ind))

    def write_pop(self, var_kind: str, var_ind: int) -> None:
        self.write_code("pop " + var_kind + " " + str(var_ind))

    def write_call(self, function_name: str, arg_num: int) -> None:
        self.write_code("call " + function_name + " " + str(arg_num))

    def write_arithmetic(self, op: str) -> None:
        if op == "+":
            self.write_code("add")
        elif op == "-":
            self.write_code("sub")
        elif op == "*":
            self.write_call("Math.multiply", 2)
        elif op == "/":
            self.write_call("Math.divide", 2)
        elif op == "&":
            self.write_code("and")
        elif op == "|":
            self.write_code("or")
        elif op == ">":
            self.write_code("gt")
        elif op == "<":
            self.write_code("lt")
        elif op == "=":
            self.write_code("eq")
        elif op == "~":
            self.write_code("not")
        elif op == "neg":
            self.write_code("neg")
        elif op == "not":
            self.write_push(VmVarKind.constant, 0)
            self.write_arithmetic("=")
        else:
            raise RuntimeError("Unknown operator.")

    def write_if(self, label: str) -> None:
        self.write_code("if-goto " + label)
    
    def write_goto(self, label: str) -> None:
        self.write_code("goto " + label)

    def write_label(self, label: str) -> None:
        self.write_code("label " + label)

    def write_return(self) -> None:
        self.write_code("return")