from CodeWriter import CodeWriter


class VmCodeWriter(CodeWriter):
  BASE_TMP_REG = 13
  TEMP_START = 5
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
    self.current_function = ""
    self.ret_num = 0
    self.source_file_name = ""

  def set_source_file_name(self, source_file_name:str) -> None:
    self.source_file_name = source_file_name
    
  def get_source_file_name(self) -> str:
    return self.source_file_name

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
      reg = self.source_file_name + num
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
    ## set A to address, D to value
    if seg == "pointer":
      if num == "0":
        self.write_pop_stack_to_D()
        self.write_code("@THIS")
      elif num == "1":
        self.write_pop_stack_to_D()
        self.write_code("@THAT")
      else:
        print("Syntax error, pointer num out of range, num:", num)

    elif seg == "static":
      reg = self.source_file_name + num
      self.write_pop_stack_to_D()
      self.write_code("@" + reg)
    elif seg == "temp":
      reg = str(VmCodeWriter.TEMP_START + int(num))
      self.write_pop_stack_to_D()
      self.write_code("@" + reg)
    elif seg in self.seg2pointer:
      reg = self.seg2pointer[seg]
      tmp_reg = self.write_addr_to_tmp(reg, num)
      self.write_pop_stack_to_D()
      self.write_code("@" + tmp_reg)
      self.write_code("A=M")
      
    self.write_code("M=D")

  def write_ari_log_code(self, op:str) -> None:
    # get result and store in D register
    if op == "neg":
      self.write_pop_stack_to_D()
      self.write_code("D=-D")
    elif op == "not":
      self.write_pop_stack_to_D()
      self.write_code("D=!D")
    else:
      tmp_reg = str(VmCodeWriter.BASE_TMP_REG + self.tmp_reg_used)
      # pop to tmp register
      self.write_pop_stack_to_D()
      self.write_code("@" + tmp_reg)
      self.write_code("M=D")
      self.write_pop_stack_to_D()
      self.write_code("@" + tmp_reg)
      if op == "add":
        self.write_code("D=D+M")
      elif op == "sub":
        self.write_code("D=D-M")
      elif op == "and":
        self.write_code("D=D&M")
      elif op == "or":
        self.write_code("D=D|M")
      else: 
        # for logical operation, branching is necessary, template is as below
        # D=D-M
        # @LOGICAL_OP_TRUE_NUM
        # D;JEQ / JGT / JLT
        # @LOGICAL_OP_OUTSIDE_NUM
        # D=0;JMP
        # (LOGICAL_OP_TRUE_NUM)
        # D=1
        # (LOGICAL_OP_OUTSIDE_NUM) 
        self.write_code("D=D-M")
        self.write_code("@LOGICAL_OP_TRUE_" + str(self.logical_op_num))
        if op == "eq":
          self.write_code("D;JEQ")
        elif op == "gt":
          self.write_code("D;JGT")
        elif op == "lt":
          self.write_code("D;JLT")

        self.write_code("@LOGICAL_OP_OUTSIDE_" + str(self.logical_op_num))
        self.write_code("D=0;JMP")
        self.write_code("(LOGICAL_OP_TRUE_" + str(self.logical_op_num) + ")")
        self.write_code("D=-1") #0xFFFF
        self.write_code("(LOGICAL_OP_OUTSIDE_" + str(self.logical_op_num) + ")") 
        self.logical_op_num += 1

    # push the result into stack
    self.write_push_D_to_stack()
      
  def write_label_code(self, label:str) -> None:
    if not self.current_function:
      self.write_code("(" + label + ")")
    else:
      self.write_code("(" + self.current_function + "$" + label + ")")
  
  def write_goto_code(self, label:str) -> None:
    if not self.current_function:
      self.write_code("@" + label)
    else:
      self.write_code("@" + self.current_function + "$" + label)
    self.write_code("0;JMP")

  def write_if_goto_code(self, label:str) -> None:
    self.write_pop_stack_to_D()
    if not self.current_function:
      self.write_code("@" + label)
    else:
      self.write_code("@" + self.current_function + "$" + label)
    self.write_code("D;JNE")

  def write_call_op(self, code:list) -> None:
    func_name, arg_nums = code
    # push return address
    ret_label = "RET_LABEL_" + str(self.ret_num)
    self.write_code("@" + ret_label)
    self.write_code("D=A")
    self.write_push_D_to_stack()
    # push LCL
    self.write_code("@LCL")
    self.write_code("D=M")
    self.write_push_D_to_stack()
    # push ARG
    self.write_code("@ARG")
    self.write_code("D=M")
    self.write_push_D_to_stack()
    # push THIS
    self.write_code("@THIS")
    self.write_code("D=M")
    self.write_push_D_to_stack()
    # push THAT
    self.write_code("@THAT")
    self.write_code("D=M")
    self.write_push_D_to_stack()
    # ARG = SP - n -5
    self.write_code("@SP")
    self.write_code("D=M")
    self.write_code("@5")
    self.write_code("D=D-A")
    self.write_code("@" + arg_nums)
    self.write_code("D=D-A")
    self.write_code("@ARG")
    self.write_code("M=D")
    # LCL = SP
    self.write_code("@SP")
    self.write_code("D=M")
    self.write_code("@LCL")
    self.write_code("M=D")
    # goto func_name
    self.write_code("@" + func_name)
    self.write_code("0;JMP")
    self.write_code("(" + ret_label + ")")
    self.ret_num += 1

  def write_function_op(self, code:list) -> None:
    func_name, var_nums = code
    self.current_function = func_name
    # (func_name)
    self.write_code("(" + func_name + ")")
    # push constant 0 * var_nums
    for i in range(int(var_nums)):
      self.write_push(["push", "constant", "0"])
    
  def write_return_op(self) -> None:
    # FRAME = LCL , in tmp_reg1
    self.write_code("@LCL")
    self.write_code("D=M")
    tmp_reg1 = str(VmCodeWriter.BASE_TMP_REG + self.tmp_reg_used)
    self.tmp_reg_used += 1
    self.write_code("@R" + tmp_reg1)
    self.write_code("M=D")
    # RET = *(FRAME-5)
    self.write_code("@5")
    self.write_code("A=D-A")
    self.write_code("D=M")
    tmp_reg2 = str(VmCodeWriter.BASE_TMP_REG + self.tmp_reg_used)
    self.tmp_reg_used += 1
    self.write_code("@R" + tmp_reg2)
    self.write_code("M=D")
    # *ARG = pop()
    self.write_pop_stack_to_D()
    self.write_code("@ARG")
    self.write_code("A=M")
    self.write_code("M=D")
    #  SP = ARG + 1
    self.write_code("@ARG")
    self.write_code("D=M+1")
    self.write_code("@SP")
    self.write_code("M=D")
    # THAT = *(FRAME - 1) & *FRAME = *(FRAME - 1)
    self.write_code("@R" + tmp_reg1)
    self.write_code("AM=M-1")
    self.write_code("D=M")
    self.write_code("@THAT")
    self.write_code("M=D")
    # THIS = *(FRAME - 1) & *FRAME = *(FRAME - 1)
    self.write_code("@R" + tmp_reg1)
    self.write_code("AM=M-1")
    self.write_code("D=M")
    self.write_code("@THIS")
    self.write_code("M=D")
    # ARG = *(FRAME - 1) & *FRAME = *(FRAME - 1)
    self.write_code("@R" + tmp_reg1)
    self.write_code("AM=M-1")
    self.write_code("D=M")
    self.write_code("@ARG")
    self.write_code("M=D")
    # LCL = *(FRAME - 1) & *FRAME = *(FRAME - 1)
    self.write_code("@R" + tmp_reg1)
    self.write_code("AM=M-1")
    self.write_code("D=M")
    self.write_code("@LCL")
    self.write_code("M=D")
    # goto RET
    self.write_code("@R" + tmp_reg2)
    self.write_code("A=M")
    self.write_code("0;JMP")
    self.tmp_reg_used -= 2
    
  def write_init_op(self) -> None:
    # SP = 256
    self.write_code("@256")
    self.write_code("D=A")
    self.write_code("@SP")
    self.write_code("M=D")
    # Call Sys.init
    self.write_call_op(["Sys.init", "0"])

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

  def write_addr_to_tmp(self, reg:str, num:str) -> str:
    self.write_code("@" + reg)
    self.write_code("D=M")
    self.write_code("@" + num)
    self.write_code("D=D+A")
    tmp_reg = str(VmCodeWriter.BASE_TMP_REG + self.tmp_reg_used)
    self.write_code("@R" + tmp_reg)
    self.write_code("M=D")
    return tmp_reg