import code
import sys
from Parser import Parser
from Coder import Coder


if __name__=="__main__":
  if (len(sys.argv) != 3):
    print("Usage: Python assembler.py inputFile.asm outputFile.hack")
    sys.exit(-1)
  parser = Parser(sys.argv[1], sys.argv[2])
  parser.pre_process()
  coder = Coder()
  while (parser.get_next_cmd()):
    if (parser.get_current_cmd_type()):
      dst, cmp, jmp = parser.parse_c_command()
      if "M" in cmp:
        op = "1"
        cmp = cmp.replace("M", "A")
      else:
        op = "0"

      out_cmd = "111" + op + coder.code_cmp(cmp) + coder.code_dst(dst) + coder.code_jmp(jmp)
    else:
      address = parser.parse_a_command()
      out_cmd = coder.code_address(address)
    parser.write(out_cmd)
  parser.close()
