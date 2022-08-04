from CodeWriter import CodeWriter


class VmCodeWriter(CodeWriter):
  BASE_TMP_REG = 13
  TEMP_START = 5
  STATIC_VAR = "sta"
  def __init__(self, dest_file:str) -> None:
    super().__init__(dest_file)
    self.seg2pointer = {
      "local"    : "LCL",
      "argument" : "ARG",
      "this"     : "THIS",
      "that"     : "THAT",
    }
    self.tmp_reg_used = 0
    self.logical_op_num = 0

  def write_comment(self, code:str) -> None:
    self.write_code("// " + code)

  def write_push(self, code:list) -> None:
    _, seg, num = code
    if seg == "constant": # load constant num to D
      self.write_load_constant_to_D(num)
    elif seg == "pointer": # load THIS or THAT to D
      if num == "0":
        self.write_load_register_value_to_D("THIS")
      elif num == "1":
        self.write_load_register_value_to_D("THAT")
      else:
        print("Syntax error, pointer num out of range, num:", num)
    elif seg == "static": # create new variable in assembly language
      reg = VmCodeWriter.STATIC_VAR + num
      self.write_load_register_value_to_D(reg)
    elif seg == "temp": # tmp map from R5
      reg = str(VmCodeWriter.TEMP_START + int(num))
      self.write_load_register_value_to_D(reg)
    elif seg in self.seg2pointer: # load seg[num] to D
      reg = self.seg2pointer[seg]
      self.write_load_register_value_to_D(reg)
      self.write_code("@" + num)
      self.write_code("A=D+A")
      self.write_code("D=M")
    else:
      print("Syntax error:", code)
    self.write_push_D_to_stack()

  def write_pop(self, code:list) -> None:
    _, seg, num = code
    if seg == "pointer":
      if num == "0":
        self.write_pop_stack_to_D()
        self.write_code("@THIS")
        self.write_code("M=D")
      elif num == "1":
        self.write_pop_stack_to_D()
        self.write_code("@THAT")
        self.write_code("M=D")
      else:
        print("Syntax error, pointer num out of range, num:", num)
    elif seg == "static":
      

  def write_load_constant_to_D(self, num:str) -> None:
    self.write_code("@" + num)
    self.write_code("D=A")

  def write_push_D_to_stack(self) -> None:
    self.write_code("@SP")
    self.write_code("A=M")
    self.write_code("M=D")
    self.write_code("@SP")
    self.write_code("M=M+1")
  
  def write_load_register_value_to_D(self, reg:str) -> None:
    self.write_code("@" + reg)
    self.write_code("D=M")

  def write_pop_stack_to_D(self) -> None:
    self.write_code("@SP")
    self.write_code("AM=M-1")
    self.write_code("D=M")

  def write_addr_to_tmp(self, reg:str, num:str) -> None:
    self.write_code("@" + reg)
    self.write_code("D=M")
    self.write_code("@" + num)
    self.write_code("D=D+A")
    self.write_code("@R" + str(VmCodeWriter.BASE_TMP_REG + self.tmp_reg_used))
    self.write_code("M=D")




