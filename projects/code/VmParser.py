from email.policy import strict
import string
import sys
from Parser import Parser
from enum import Enum


class VmCodeType(Enum):
  PUSH     = 1
  POP      = 2
  OP       = 3
  LABEL    = 4
  GOTO     = 5
  IF_GOTO  = 6
  FUNCTION = 7
  CALL     = 8
  RETURN   = 9 

class VmParser(Parser):
  def __init__(self, source_file) -> None:
    super().__init__(source_file)
    self.code_type_dic = {
      "push"     : VmCodeType.PUSH,
      "pop"      : VmCodeType.POP,
      "op"       : VmCodeType.OP,
      "label"    : VmCodeType.LABEL,
      "goto"     : VmCodeType.GOTO,
      "if-goto"  : VmCodeType.IF_GOTO,
      "function" : VmCodeType.FUNCTION,
      "call"     : VmCodeType.CALL,
      "return"   : VmCodeType.RETURN
    }
    self.source_file_name = ""

  def set_source_file_name(self, source_file_name:str) -> None:
    self.source_file_name = source_file_name

  def get_source_file_name(self) -> str:
    return self.source_file_name

  def get_code_type(self) -> VmCodeType:
    keyword = self.current_code.strip().split(" ")[0]
    if keyword in self.code_type_dic:
      return self.code_type_dic[keyword]
    else:
      return self.code_type_dic["op"]
  
  def parse_data_op(self) -> list:
    LEN_DATA_OP = 3
    keywords = self.current_code.strip().split(" ")
    if len(keywords) != LEN_DATA_OP:
      print("Syntax error: ", self.current_code)
      sys.exit(1)
    op, seg, num = keywords
    return op, seg, num

  def parse_arithmetic_logic_op(self) -> string:
    op = self.current_code.strip()
    return op

  def parse_label_op(self) -> string:
    label = self.current_code.strip().split(" ")[1]
    return label
  
  def parse_function_op(self) -> list:
    LEN_FUNC_OP = 3
    keywords = self.current_code.strip().split(" ")
    if len(keywords) != LEN_FUNC_OP:
      print("Syntax error: ", self.current_code)
      sys.exit(1)
    _, func_name, func_vars_num = keywords
    return func_name, func_vars_num
  
  def parse_call_op(self) -> list:
    LEN_CALL_OP = 3
    keywords = self.current_code.strip().split(" ")
    if len(keywords) != LEN_CALL_OP:
      print("Syntax error: ", self.current_code)
      sys.exit(1)
    _, func_name, func_args_num = keywords
    return func_name, func_args_num


