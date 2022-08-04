from email.policy import strict
import string
import sys
from Parser import Parser
from enum import Enum


class VmCodeType(Enum):
  PUSH = 1
  POP  = 2
  OP   = 3 

class VmParser(Parser):
  def __init__(self, source_file) -> None:
    super().__init__(source_file)
    self.code_type_dic = {
      "push" : VmCodeType.PUSH,
      "pop"  : VmCodeType.POP,
      "op"   : VmCodeType.OP
    }

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


