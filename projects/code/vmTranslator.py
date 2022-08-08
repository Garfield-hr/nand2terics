from genericpath import isfile
import sys, os
from VmParser import VmParser, VmCodeType
from VmCoderWriter import VmCodeWriter

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: Python vmTranslator.py source .")
    sys.exit(1)

  vmParserList = []
  if os.path.isfile(sys.argv[1]):
    vmParserList.append(VmParser(sys.argv[1]))
    vmCodeWriter = VmCodeWriter(sys.argv[1].replace(".vm", ".asm"))
  else:
    file_name = sys.argv[1].split("\\")[-1]
    vmCodeWriter = VmCodeWriter(sys.argv[1] + "\\" + file_name + ".asm")
    f_list = os.listdir(sys.argv[1])
    for file in f_list:
      if os.path.splitext(file)[1] == ".vm":
        vmParserList.append(VmParser(sys.argv[1] + "\\" + file))
        vmParserList[-1].set_source_file_name(file)

  vmCodeWriter.write_init_op()
  for vmParser in vmParserList:
    vmCodeWriter.set_source_file_name(vmParser.get_source_file_name())
    while vmParser.get_next_code():
      vmCodeWriter.write_comment(vmParser.get_current_code())
      if vmParser.get_code_type() == VmCodeType.PUSH:
        code_list = vmParser.parse_data_op()
        vmCodeWriter.write_push(code_list)
      elif vmParser.get_code_type() == VmCodeType.POP:
        code_list = vmParser.parse_data_op()
        vmCodeWriter.write_pop(code_list)
      elif vmParser.get_code_type() == VmCodeType.OP:
        op = vmParser.parse_arithmetic_logic_op()
        vmCodeWriter.write_ari_log_code(op)
      elif vmParser.get_code_type() == VmCodeType.LABEL:
        label = vmParser.parse_label_op()
        vmCodeWriter.write_label_code(label)
      elif vmParser.get_code_type() == VmCodeType.GOTO:
        label = vmParser.parse_label_op()
        vmCodeWriter.write_goto_code(label)
      elif vmParser.get_code_type() == VmCodeType.IF_GOTO:
        label = vmParser.parse_label_op()
        vmCodeWriter.write_if_goto_code(label)
      elif vmParser.get_code_type() == VmCodeType.CALL:
        code_list = vmParser.parse_call_op()
        vmCodeWriter.write_call_op(code_list)
      elif vmParser.get_code_type() == VmCodeType.FUNCTION:
        code_list = vmParser.parse_function_op()
        vmCodeWriter.write_function_op(code_list)
      elif vmParser.get_code_type() == VmCodeType.RETURN:
        vmCodeWriter.write_return_op()
      else:
        print("ERROR: parser wrong result.")
         
  vmCodeWriter.close()