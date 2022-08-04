import sys
from VmParser import VmParser, VmCodeType
from VmCoderWriter import VmCodeWriter

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: Python vmTranslator.py source.vm.")
    sys.exit(1)
  
  vmParser = VmParser(sys.argv[1])
  vmCodeWriter = VmCodeWriter(sys.argv[1].replace(".vm", ".asm"))
  while vmParser.get_next_code():
    vmCodeWriter.write_comment(vmParser.get_current_code())
    if vmParser.get_code_type() == VmCodeType.PUSH:
      code_list = vmParser.parse_data_op()
      vmCodeWriter.write_push(code_list)
    elif vmParser.get_code_type() == VmCodeType.POP:
      code_list = vmParser.parse_data_op()
      vmCodeWriter.write_pop(code_list)
    else:
      op = vmParser.parse_arithmetic_logic_op()
      vmCodeWriter.write_ari_log_code(op)
  vmCodeWriter.close()